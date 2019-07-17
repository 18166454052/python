create table `variety_list` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `variety_title` varchar(100) ,
     `variety_url` varchar(255) NOT NULL,
     `parent_id` varchar(100) NOT NULL,
     `parent_title` varchar(100) NOT NULL,
     `date` varchar(50) NOT NULL,
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;