import json
from operator import itemgetter
import re

# status - 1:не замужем/женат
# city - 2: СПб
search_fields = {
    'count': '10',
    'fields': 'bdate, sex, city, relation, photo_100',
    'hometown': 'Петербург',
    'sex': '1',
    'status': '1',
    'age_from': '23',
    'age_to': '25',
    'city': 2
}


def get_config(conf_file='conf.json'):
    
    with open(conf_file, encoding="utf-8") as file:
        config = json.load(file)
    
    return config

def sort_list(data, key = 'likes'):
    data = data[0:-1]
    data.sort(key = itemgetter(key))
    return data[-3:]

def check_answer(answer):

    answer = answer.split(', ')
    if len(answer) != 4:

        return False

    else:
        if (re.fullmatch(r"[А-Яа-я]*", answer[2]) != None and re.fullmatch(r"[0-9]{2}", answer[0]) != None and re.fullmatch(r"[0-2]{1}", answer[1]) and re.fullmatch(r"[1-8]{1}", answer[3])):

            return True
        else:

            return False


if __name__ == '__main__':

    array = [{'img': 'https://sun9-33.userapi.com/c10847/u1987317/-6/s_91e4c600.jpg', 'likes': 8, 'id': 204910557, 'owner_id': 1987317}, 
    {'img': 'https://sun9-15.userapi.com/c10042/u1987317/-6/s_e4aab2f6.jpg', 'likes': 6, 'id': 190142977, 'owner_id': 1987317}, 
    {'img': 'https://sun9-49.userapi.com/c10847/u1987317/-6/s_acc60bdb.jpg', 'likes': 13, 'id': 204909723, 'owner_id': 1987317}, 
    {'img': 'https://sun9-20.userapi.com/c10847/u1987317/5810430/s_1945789c.jpg', 'likes': 11, 'id': 204921275, 'owner_id': 1987317}, 
    {'img': 'https://sun9-43.userapi.com/c10194/u1987317/-6/s_c4a64273.jpg', 'likes': 0, 'id': 240185757, 'owner_id': 1987317}, 
    {'img': 'https://sun9-23.userapi.com/c9743/u1987317/134868938/s_3735a3d4.jpg', 'likes': 2, 'id': 262246921, 'owner_id': 1987317}, 
    {'img': 'https://sun9-20.userapi.com/c4148/u1987317/-6/s_f74d7e61.jpg', 'likes': 11, 'id': 264487499, 'owner_id': 1987317}, 
    {'img': 'https://sun9-15.userapi.com/c11486/u1987317/-6/s_f9838e54.jpg', 'likes': 16, 'id': 268788163, 'owner_id': 1987317}, 
    {'img': 'https://sun9-48.userapi.com/c10847/u1987317/-6/s_89a8ce6a.jpg', 'likes': 16, 'id': 204911565, 'owner_id': 1987317}, 
    {'img': 'https://sun9-22.userapi.com/c9639/u1987317/-6/s_1ba45dc0.jpg', 'likes': 14, 'id': 276781463, 'owner_id': 1987317}, 
    {'img': 'https://sun9-34.userapi.com/impf/VdkVu5jTy-YHCtZHSs5rrLYmbVecKr6SNV9tIQ/bb8LacL7YkI.jpg?size=130x97&quality=96&sign=1cdc8d57bada5bea036fc0350bed746d&c_uniq_tag=u4nJ7cQARhai4aEcP5B1BZvJq9UdDpBZuoOzv7oPTnY&type=album', 'likes': 9, 'id': 288138582, 'owner_id': 1987317}, 
    {'img': 'https://sun9-13.userapi.com/impf/xibN3PrSCQD8yfy9KmFtDx3RInEdCh-0zBBSAw/er6JgjQOlww.jpg?size=130x97&quality=96&sign=80619a535189ef0883a6adffe06c5dfe&c_uniq_tag=NiX7yAIVWtXyaI6wxI7He4q-LZPc4mk0RoP1pilHOZ4&type=album', 'likes': 26, 'id': 285718744, 'owner_id': 1987317}, 
    {'img': 'https://sun9-39.userapi.com/c11486/u1987317/144430009/s_6513ffa1.jpg', 'likes': 24, 'id': 282485226, 'owner_id': 1987317}, 
    {'img': 'https://sun9-26.userapi.com/c9863/u1987317/-6/s_08f056ec.jpg', 'likes': 68, 'id': 270504041, 'owner_id': 1987317}, 
    {'img': 'https://sun9-83.userapi.com/impf/LrVHUkomJ5cF_u7tMqIK7FxpWGx_GTfEZU7Lmw/wcaj-lIVfnM.jpg?size=102x130&quality=96&sign=ec669566dc706627fa39f20bddaffc5c&c_uniq_tag=GqinKKUvoivsiy4NwnvVvhgVdxXXgtQ4JYMpBY_wkG8&type=album', 'likes': 32, 'id': 313595770, 'owner_id': 1987317}, 
    {'img': 'https://sun9-47.userapi.com/impf/e0mjA3lFxLiHFjR-v2slk-Ggti1KEeShw6MImg/lpiEviijYVE.jpg?size=97x130&quality=96&sign=de31c173178055d60546ddc87494111e&c_uniq_tag=cTqFarb6iQiKohaj-nOlHIXkInlZwIaEPGZJ_vN5fGs&type=album', 'likes': 59, 'id': 313602786, 'owner_id': 1987317}, {'img': 'https://sun9-85.userapi.com/impf/c624027/v624027181/2cde/Cjw_OvJHIFQ.jpg?size=130x130&quality=96&sign=b898b3f2fb604d9097417feaaf0b573b&c_uniq_tag=QVY8cNFZIxYxeQd8LXFTluc0Yh-kSzPK_LaJSgNmxRA&type=album', 'likes': 52, 'id': 341188431, 'owner_id': 1987317}, {'img': 'https://sun9-62.userapi.com/impf/c625226/v625226317/12721/7zvpojS7LKw.jpg?size=95x130&quality=96&sign=bc4747a2b4af1f6670516a29b9802aa2&c_uniq_tag=1Gp7DWdtz-MTx8XtlYoBRPHA2C6jwuMMPqTRnWsehK0&type=album', 'likes': 27, 'id': 347845811, 'owner_id': 1987317}, {'img': 'https://sun9-34.userapi.com/impf/Jt2Uv8CMQxTimW1OSG0_gOE47sgCOGz3OVqIuA/BMGwuYTHa0Y.jpg?size=130x130&quality=96&sign=9d21f88075cac69fe4763f51eb7c7973&c_uniq_tag=JVI7EItpHzO3mTNELQp0MgTD81-miRtwGKiRi6r45W8&type=album', 'likes': 92, 'id': 328445816, 'owner_id': 1987317}, {'img': 'https://sun9-4.userapi.com/impf/c624027/v624027317/37bb9/mJWTJqNDrfY.jpg?size=59x130&quality=96&sign=8be8e4f87aaf6b1946e72450bd0baf7f&c_uniq_tag=Uu7ZhBMxRIlwh7idEys67a5BxovssXbaSx0MFvApNMc&type=album', 'likes': 40, 'id': 362108159, 'owner_id': 1987317}, {'img': 'https://sun9-52.userapi.com/impf/c621927/v621927317/2388c/2iKvVz4f3OQ.jpg?size=130x97&quality=96&sign=afb1ab15bc56d3a06f9541441f553535&c_uniq_tag=4Om6pj3PuZ-gV2cVOskgldvEXQN4-ApSDfsCeMhYKLw&type=album', 'likes': 35, 'id': 363359805, 'owner_id': 1987317}, {'img': 'https://sun9-58.userapi.com/impf/c625218/v625218317/37ea5/B7d1HK83pT0.jpg?size=97x130&quality=96&sign=df3e09bc6e051afb90858974b75ad819&c_uniq_tag=4WqbXg61A7-tuo9fiQNk-iUohC8m9mFTM8lL95GRwFk&type=album', 'likes': 35, 'id': 367365867, 
    'owner_id': 1987317}, 
    {'img': 'https://sun9-49.userapi.com/impf/c625218/v625218317/3b4d6/Meu9j2Voc3Y.jpg?size=73x130&quality=96&sign=5780db3515f691bfc74711d8d81f0c93&c_uniq_tag=tIgiK2FRtQ2sjvjYO44A0mnffpTaBNK9ePHo6K1yI64&type=album', 'likes': 37, 'id': 370242651, 'owner_id': 1987317}, {'img': 'https://sun9-51.userapi.com/impf/c625218/v625218317/3bdd3/toFVYljUh7A.jpg?size=73x130&quality=96&sign=5566f4ef0bfce9d7dcc366ed888fda33&c_uniq_tag=qb1S0HdW7NTimPxnB5U83Q_5fPX3C9ATsTQ1WcKlFW8&type=album', 'likes': 39, 'id': 371625695, 'owner_id': 1987317}, {'img': 'https://sun9-86.userapi.com/impf/c629403/v629403317/46e16/xZsrTynKx0E.jpg?size=73x130&quality=96&sign=b930d2a6dffce1f397e8a54ccb0077dc&c_uniq_tag=1yKo6L_7FQB7Sl8TVpMQCN2hRlKSMgGrjsr8Pbd5MSc&type=album', 'likes': 75, 'id': 377513225, 'owner_id': 1987317}, {'img': 'https://sun9-6.userapi.com/impf/c627619/v627619317/36233/hhGep3REzdM.jpg?size=130x97&quality=96&sign=a2b5a29352c8839c7490e0300c80f764&c_uniq_tag=ylvaNZRt9uUcMh-oMABAIlry9zY-7dWVcGm1Jr-OtnU&type=album', 'likes': 89, 'id': 395534842, 'owner_id': 1987317}, {'img': 'https://sun9-82.userapi.com/impf/c633718/v633718317/3b6ca/Qh4x8V8OGek.jpg?size=130x87&quality=96&sign=233f1d95f2d5140c4f737e8bd1b97bf5&c_uniq_tag=694wjACR_LoHTK3ja8n4Y-wd-BEUEr6wI9p72ph5-mw&type=album', 'likes': 66, 'id': 415870892, 'owner_id': 1987317}, {'img': 'https://sun9-63.userapi.com/impf/c626227/v626227317/e332/iXNVZYuI9yo.jpg?size=87x130&quality=96&sign=2335c5f677388a22d599e9b7b59568e9&c_uniq_tag=I-hmlk-M2GqnGYIs8cDTMUyONYYf-aBOcNOvw1DpgnA&type=album', 'likes': 111, 'id': 416447251, 'owner_id': 1987317}, {'img': 'https://sun9-76.userapi.com/impf/c626516/v626516317/26025/a1cZ-Ta8fYw.jpg?size=130x130&quality=96&sign=cf5d9875c8910a3f804f78d4c89b3667&c_uniq_tag=zvLddDxKxwCUO3Payk-Ys_UQI7S7iRXb9L0wubHleQo&type=album', 'likes': 481, 'id': 423219742, 'owner_id': 1987317}, {}]

    # print(sort_list(array))

    t = '21'
    t1 = '22, 12, Питер, 2'

    print(re.fullmatch(r"[0-9]{2}", t))
    print(check_answer(t1))


