create database dp_idx; 

use dp_idx;

create table idx (
    id int not null auto_increment primary key,
    site_id int not null,
    url_crc bigint not null,
    offset int not null,
    size int not null,
    update_time datetime not null,
    data_file char(40) not null,
    url varchar(128) not null,
    key query (site_id, url_crc, update_time, data_file)
); 

create table data_file (
    id int not null auto_increment primary key,
    data_file char(40) not null,
    site_id int not null,
    gid tinyint default 0,
    compress tinyint not null, 
    status tinyint not null,
    update_time datetime not null,
    key query (site_id, compress, status, update_time, data_file)
);




