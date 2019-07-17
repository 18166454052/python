drop table tv_item;
create table `tv_item` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `tv_title` varchar(100) NOT NULL,
     `tv_url` varchar(255) NOT NULL,
     `tv_image` varchar(255) NOT NULL,
     `tv_all` varchar(10) NOT NULL,
     `tv_caption` varchar(255) default NULL,
     `tv_desc` varchar(255) default NULL ,
     `offset`  varchar(255)  NOT NULL,
     `feature` varchar(100) default NULL,
     `iarea` varchar(100) default NULL,
     `year` varchar(100) default NULL,
     `pay` varchar(100) default NULL,
     `type` char(20) default 'tv',
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;