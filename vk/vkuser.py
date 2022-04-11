from attr import fields
from util.util import get_config, search_fields
import vk_api
from database.dbvk import VKdatabase

class VkUserSearch():
    
    def __init__(self, token = get_config()['tokenVK'], user_vk_id  = get_config()['myID'] ):
        
        self._token = token
        self._user_id = user_vk_id

    def set_connect(self):

        vk_user = vk_api.VkApi(token = self._token);
        vk_connect = vk_user.get_api()
        
        return vk_connect

    def get_user_info(self, vk_connect, fields_str = search_fields['fields']):
    
        user_get=vk_connect.users.get(user_id = self._user_id, fields = fields_str)
        user_get=user_get[0]
      
        return user_get

    def search_users(self, vk_connect, search_fields, offset = 0):
        
        return vk_connect.users.search(count = search_fields['count'], offset = offset, fields = search_fields['fields'], city = search_fields['city'], sex= search_fields['sex'], status = search_fields['status'], age_from = search_fields['age_to'], age_to = search_fields['age_to'])
         
    def search_user_profile_photo(self, vk_connect, vk_owner_id):
        
        return vk_connect.photos.get(owner_id = vk_owner_id, album_id = 'profile', extended = 1)
    
    def search_city_id(self, vk_connect, city_name = 'Вологда'):
        
        return vk_connect.database.getCities(owner_id = self._user_id, q = city_name, need_all = 0, country_id = 1)['items'][0]

    def search_user_albums(self, vk_connect, users_id):
        
        return vk_connect.photos.getAlbums(owner_id = users_id)
    

if __name__ == '__main__':

    db = VKdatabase()
    connect = db.connect_db()
    vk = VkUserSearch()
    vk_connect = vk.set_connect()
    # info = vk.get_user_info(vk_connect)
    # print(vk.search_city_id(vk_connect)['id'])
    # db.insert_user_info(connect, **info)
    # result = db.find_user(connect)
    # print(result, len(result))
    # result = vk.search_user_profile_photo(vk_connect, '182008724')['items']
    # print(result)
    # for item in result:
    #     print(item)
    #     print('*' * 100)
    #     print(item['likes'])
    #     print('*' * 100)
    #     print(item['sizes'][0])

    print(vk.search_city_id(vk_connect, city_name = 'Вологда'))
    result = vk.search_user_profile_photo(vk_connect, '182008724')
    print(result)