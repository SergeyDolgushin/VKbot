create table if not exists user_vk (
id serial primary key,
user_id_vk varchar(20) not null,
user_firstname varchar(60) not null,
user_surname varchar(60) not null,
user_city varchar(60) not null,
user_age integer,
user_sex integer,
user_marriage integer
);

create table if not exists matched_pair (
id serial primary key,
user_id_vk varchar(20) not null references user_vk(user_id_vk),
match_user_id_vk varchar(20) not null unique,
match_user_firstname varchar(60) not null,
match_user_surname varchar(60) not null,
match_user_city varchar(60) not null,
match_user_age integer,
match_user_sex integer,
match_user_marriage integer
);

create table if not exists photos (
id serial primary key,
photo_link text,
match_user_id_vk varchar(20) not null references matched_pair(match_user_id_vk),
likes integer
);

