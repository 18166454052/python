create table `cartoon_item` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `cartoon_title` varchar(100) NOT NULL,
     `cartoon_url` varchar(255) NOT NULL,
     `cartoon_image` varchar(255) NOT NULL,
     `cartoon_all` varchar(10) NOT NULL,
     `cartoon_caption` varchar(255) default NULL,
     `cartoon_desc` varchar(255) default NULL ,
     `offset`  varchar(255)  NOT NULL,
     `itype` varchar(100) default NULL,
     `iarea` varchar(100) default NULL,
     `plot_aspect` varchar(100) default NULL,
     `language` varchar(100) default NULL,
     `iyear` varchar(100) default NULL,
     `ipay` varchar(100) default NULL,
     `type` char(20) default 'cartoon',
     `source` char(20) default 'tencent',
      `order`  varchar(10) default '0',
     `create_time`  DATE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;