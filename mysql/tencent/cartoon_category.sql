create table `cartoon_category` (
     `id`  int NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `name` varchar(20) NOT NULL,
     `url` varchar(50) NOT NULL,
     `key` varchar(30) NOT NULL,
     `key_val` varchar(50) NOT NULL,
     `label` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;