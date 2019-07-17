create table `user` (
     `id`  int NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `name` varchar(20) NOT NULL,
     `pass` varchar(50) NOT NULL,
     `create_at` varchar(50) NOT NULL,
     `vip_end` varchar(50),
     `vip` int default 0,
     `token` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;