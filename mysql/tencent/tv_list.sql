drop table tv_list;
create table `tv_list` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `tv_num` varchar(100) NOT NULL,
     `tv_title` varchar(100) ,
     `tv_url` varchar(255) NOT NULL,
     `parent_id` varchar(100) NOT NULL,
     `parent_title` varchar(100) NOT NULL,
     `is_trail_notice` varchar(5) default 0,
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;