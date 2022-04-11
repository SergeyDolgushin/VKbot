from random import randrange
from util.util import get_config, search_fields, sort_list, check_answer
from vk.interface import commands
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk.vkuser import VkUserSearch
from database.dbvk import VKdatabase
import wget
import os
import time

name = ''
surname = ''

token = get_config()['botID']
user_token = get_config()['tokenVK']

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk_bot = vk_session.get_api()
vk_upload = vk_api.VkUpload(vk_bot) 

def write_msg(user_id, message):

    vk_session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def write_photo(user_id, message, photo):
    
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': photo, 'random_id': randrange(10 ** 7),})

def get_user_info_common(user_id, fields_str):
    
    user_get = vk_bot.users.get(user_id = user_id, fields = fields_str)
    user_get = user_get[0]
    
    return user_get

def start_dialog(cur_user_id, database, coonect):

    current_user = get_user_info_common(user_id = cur_user_id, fields_str = search_fields['fields'])
    name = current_user['first_name']
    surname = current_user['last_name']
    result = database.find_user(coonect, user_id = cur_user_id)
    if len(result) == 0:
        write_msg(cur_user_id, f"{commands['Привет']}{current_user['first_name']}")
        write_msg(cur_user_id, 'Вы здесь впервые, введите свой идентификатор')

        return 0
    
    write_msg(cur_user_id, f"{commands['Привет']}{current_user['first_name']}! Продолжим?")
    vk = VkUserSearch()
    vk_connect = vk.set_connect()

    return vk, vk_connect, name, surname  

def new_user(event, database, coonect):
    user_token = event.text
    vk = VkUserSearch()
    vk_connect = vk.set_connect()
    write_msg(event.user_id, f"Ок, продолжим, токен {user_token}")
    user_info = vk.get_user_info(vk_connect, fields_str = search_fields['fields'])
    database.insert_user_info(coonect, **user_info)

    return vk, vk_connect

def new_search_to_db(vk_obj, vk_connect, user_id_vk, database, coonect, search_params = search_fields):
    result = vk_obj.search_users(vk_connect, search_params)['items']
    for item in result:
        result = database.find_matched_user(coonect, user_id = item['id'])
        if len(result) == 0: 
            database.insert_matched_pair_info(coonect, user_id_vk, **item)
            if item['is_closed'] == False:
                photos_data = get_photos_profile(vk_obj, vk_connect, users_id = item['id'])
                place_photos_to_db(database, coonect, item['id'], photos_data)
        
    return None

def get_user_photos(vk_obj, vk_connect, user_info):
    photos_data = [{'img': '',
            'likes': '0',
            'id': '0',
            'owner_id': '0'}
        ]
    
    if user_info['is_closed'] == False:
        result = vk_obj.search_user_profile_photo(vk_connect, user_info['id'])
        for i, item in enumerate(result['items']):
            photos_data.append({})
            photos_data[i]['img'] = item['sizes'][0]['url']
            photos_data[i]['likes'] = item['likes']['count']
            photos_data[i]['id'] = item['id']
            photos_data[i]['owner_id'] = item['owner_id']
        photos_data = sort_list(photos_data)
    else:
        photos_data[0]['img'] = user_info['photo_100']

    return photos_data

def get_params_for_new_search(vk_obj, vk_connect, event, request, offset, search_params = search_fields):
    user_data = [{
        'user': '',
        'photos': ''
    }]
    
    temp = request.split(', ')
    search_params['sex'] = int(temp[1])
    search_params['status'] = int(temp[3])
    search_params['hometown'] = temp[2]
    search_params['city'] = vk_obj.search_city_id(vk_connect, city_name = search_params['hometown'])['id']
    search_params['age_from'] = int(temp[0])
    search_params['age_to'] = int(search_params['age_from']) + 1
    write_msg(event.user_id, f"Ищем...")
    search_result = vk_obj.search_users(vk_connect, search_params, offset)
    
    for i, item in enumerate(search_result['items']):
        user_data[i]['user'] = item
        user_data[i]['photos'] = (get_user_photos(vk_obj, vk_connect, item))
        user_data.append({})
        time.sleep(0.25)
    return user_data

def get_photos_profile(vk_obj, vk_connect, users_id):
    
    return vk_obj.search_user_profile_photo(vk_connect, users_id)['items']

def place_photos_to_db(database, coonect, user_id, photos_data):
    
    for item in photos_data:
        database.insert_profile_photos(coonect, user_id, **item)

    return 1

def show_search_result(event, db, connect, photo_data, command, offset, show_users_quantities = 10):
    
    count_of_records = 0
    end = show_users_quantities

    for item in photo_data[0:-1]:
        if len(db.find_matched_user(connect, user_id = item['user']['id'])) == 0:
            write_msg(event.user_id, f"{item['user']['first_name']}, https://vk.com/id{item['user']['id']}")
            db.insert_matched_pair_info(connect, event.user_id, **item['user'])
            for photo in item['photos']:
                if photo['owner_id'] != '0':
                    result = f"photo{photo['owner_id']}_{photo['id']}"
                    message = ''
                    write_photo(event.user_id, message, result)
                else:
                    result = save_url(event, photo['img'])
                db.insert_profile_photos(connect, item['user']['id'], result, photo['likes'])
                    
            end -= 1
            offset = 0
        else:
            count_of_records += 1
            offset += 1
            if count_of_records == len(photo_data[0:-1]): 
                write_msg(event.user_id, f"{command['next_search']}")
                
                write_msg(event.user_id, f"{offset}{len(photo_data[0:-1])}")
            else:
                write_msg(event.user_id, f"Результат уже в базе")
            if end == 0: break
    return offset

def save_url(event, url):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp.jpg')
    wget.download(url, path)
    upload_image = vk_upload.photo_messages(photos = path, peer_id = event.peer_id)[0]
    photo = f"photo{upload_image['owner_id']}_{upload_image['id']}"
    message = ''
    write_photo(event.user_id, message, photo)
    os.remove(path)

    return photo

def start_bot():

    wait_token = 1
    connect_user = 0
    user_token = 0
    get_data_status = True
    current_name = 'Незнакомец'
    offset = 0

    db = VKdatabase()
    connect = db.connect_db()
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and wait_token:
                request = event.text

                                
                if (request == "привет" or request == "1") and get_data_status:
                    result = start_dialog(event.user_id, db, connect)
                    if result != 0:
                        connect_user = 1
                        vk_connect = result[1]
                        vk_obj = result[0]
                        current_name = result[2]       
                    else:
                        wait_token = 0     

                elif (request == "пока" or request == "2") and get_data_status:
                    write_msg(event.user_id, f"{commands['Пока']}{current_name}")
                    connect_user = 0
                    
                elif (request == "старт" or request == "3" or not get_data_status) and connect_user:

                    if get_data_status:
                        write_msg(event.user_id, f"{current_name}, {commands['старт']}")
                        get_data_status = False
                    else:
                        if check_answer(request) != True:
                            get_data_status = False
                            write_msg(event.user_id, f"{current_name}, {commands['ошибка']}")
                            
                        else:
                            temp = get_params_for_new_search(vk_obj, vk_connect, event, request, offset, search_params = search_fields)
                            offset = show_search_result(event, db, connect, temp, commands, offset)
                            get_data_status = True
                    
                elif request == "Найти фото с максимумом лайков" or request == "6":
                    write_msg(event.user_id, f"Максимум лайков:\r\n")
                    sel = db.find_max_likes(connect)
                    write_msg(event.user_id, f"{getattr(sel[0], 'match_user_surname')}:\r\n")
                    write_photo(event.user_id, '', f"{getattr(sel[0], 'photo_link')}")
                else:
                    write_msg(event.user_id, f"{commands['?']}")
                         
            else:
                if event.to_me and wait_token == 0:
                    wait_token = 1
                    connect_user = 1
                    result = new_user(event, db, connect)
                    vk_connect = result[1]
                    vk_obj = result[0]
                   

    

if __name__ == '__main__':

    start_bot()
    

                    