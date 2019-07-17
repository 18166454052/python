drop table variety_item;
create table `variety_item` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `variety_title` varchar(100) NOT NULL,
     `variety_url` varchar(255) NOT NULL,
     `variety_image` varchar(255) NOT NULL,
     `variety_desc` varchar(255) default NULL ,
     `offset`  varchar(255)  NOT NULL,
     `exclusive` varchar(100) default NULL,
     `iarea` varchar(100) default NULL,
     `itype` varchar(100) default NULL,
     `iyear` varchar(100) default NULL,
     `ipay` varchar(100) default NULL,
     `type` char(20)  default 'variety',
     `order`  varchar(10) default '0',
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;