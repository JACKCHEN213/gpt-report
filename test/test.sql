DROP DATABASE IF EXISTS test;

CREATE DATABASE test;

use test;

DROP TABLE IF EXISTS tb_user;
create table tb_user
(
    id          int auto_increment
        primary key,
    name        varchar(60)                        not null,
    sex         tinyint  default 0                 null comment '[0男 1女]',
    birthday    date     default '1970-01-01'      null,
    create_time datetime default CURRENT_TIMESTAMP null,
    update_time datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
) engine InnoDB default character set utf8mb4 COLLATE utf8mb4_0900_ai_ci;