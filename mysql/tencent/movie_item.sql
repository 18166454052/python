drop table movie_item;
create table `movie_item` (
     `id`  INT  NOT NULL  PRIMARY KEY  AUTO_INCREMENT,
     `movie_title` varchar(100) NOT NULL,
     `movie_url` varchar(255) NOT NULL,
     `movie_image` varchar(255) NOT NULL,
     `movie_score` varchar(30) NOT NULL,
     `movie_desc` varchar(255) NOT NULL,
     `offset`  varchar(255)  NOT NULL,
     `itype` varchar(100) default NULL,
     `iarea` varchar(100) default NULL,
     `characteristic` varchar(100) default NULL,
     `year` varchar(100) default NULL,
     `charge` varchar(100) default NULL,
     `type` char(20) default 'movie'

) ENGINE=InnoDB DEFAULT CHARSET=utf8;