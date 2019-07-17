create table `cartoon_list` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `cartoon_num` varchar(100) NOT NULL,
     `cartoon_title` varchar(100) ,
     `cartoon_url` varchar(255) NOT NULL,
     `parent_id` varchar(100) NOT NULL,
     `parent_title` varchar(100) NOT NULL,
     `is_trail_notice` varchar(5) default 0,
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;