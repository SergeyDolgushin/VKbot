import sqlalchemy

class VKdatabase():

    def __init__(self, db = 'postgresql://postgres:1234@localhost:5432/postgres'):
        self._db = db
    
    def connect_db(self):
        engine = sqlalchemy.create_engine(self._db)
        connection = engine.connect() 

        return connection
        
    def insert_user_info(self, connection, name_table = 'user_vk', **kwarg):
    
        request_sql = f"INSERT INTO {name_table}(user_id_vk, user_firstname, user_surname, user_city, user_age, user_sex, user_marriage) VALUES('{kwarg['id']}', '{kwarg['first_name']}', '{kwarg['last_name']}', '{kwarg['city']['title']}', '{kwarg['bdate']}', {kwarg['sex']}, {kwarg['relation']});"
        connection.execute(request_sql)

        return 1

    def insert_matched_pair_info(self, connection, user_id, name_table = 'matched_pair', **kwarg):
        relation = 0
        
        relation = -1 if 'relation' not in kwarg else  kwarg['relation']
        city = 'None' if 'city' not in kwarg else  kwarg['city']['title']

        request_sql = f"INSERT INTO {name_table}(user_id_vk, match_user_id_vk, match_user_firstname, match_user_surname, match_user_city, match_user_age, match_user_sex, match_user_marriage) VALUES('{user_id}', '{kwarg['id']}', '{kwarg['first_name']}', '{kwarg['last_name']}', '{city}', '{kwarg['bdate']}', {kwarg['sex']}, {relation});"
        connection.execute(request_sql)

        return 1

    def insert_profile_photos(self, connection, match_user_id_vk, photo, likes, name_table = 'photos'):
        
        request_sql = f"INSERT INTO {name_table}(match_user_id_vk, photo_link, likes) VALUES('{match_user_id_vk}', '{photo}', '{likes}');"
        connection.execute(request_sql)

        return 1

    def find_user(self, connection, user_id = "1584850"):
        sel = connection.execute(f"SELECT user_id_vk, user_surname FROM user_vk WHERE user_id_vk = '{user_id}';").fetchmany(10)
        
        return sel

    def find_matched_user(self, connection, table = 'matched_pair', user_id_vk = 'match_user_id_vk', user_id = "43860665"):
        sel = connection.execute(f"SELECT {user_id_vk} FROM {table} WHERE {user_id_vk} = '{user_id}';").fetchmany(10)
        
        return sel

    def find_max_likes(self, connection):
        sel = connection.execute("""
                        SELECT matched_pair.match_user_id_vk, match_user_surname, photos.likes, photos.photo_link FROM matched_pair
                        JOIN photos ON matched_pair.match_user_id_vk = photos.match_user_id_vk
                        WHERE photos.likes = (SELECT MAX(likes) FROM photos)
                        ;
                        """).fetchmany(1)
        return sel


if __name__ == '__main__':
    
    db = VKdatabase()
    connect = db.connect_db()
    result = db.find_user(connect)
    result = db.find_matched_user(connect)
    print(result, len(result))
    print('*' * 50)
    # print(getattr(result[0], 'match_user_id_vk'))

    sel = connect.execute("""
        SELECT matched_pair.match_user_id_vk, match_user_surname, photos.likes, photos.photo_link FROM matched_pair
        JOIN photos ON matched_pair.match_user_id_vk = photos.match_user_id_vk
        WHERE photos.likes = (SELECT MAX(likes) FROM photos)
        ;
        """).fetchmany(100)
    print(sel)
    print(getattr(sel[0], 'match_user_surname'))
    print(getattr(sel[0], 'photo_link'))
    