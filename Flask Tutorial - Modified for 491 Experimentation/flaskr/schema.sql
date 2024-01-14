CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` text,
  `password` longtext,
  `firstname` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL,
  `usercol` varchar(45) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `country` varchar(45) DEFAULT NULL,
  `mobilenumber` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
)

CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` text NOT NULL,
  `body` longtext,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`)
)

/*
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    email TEXT UNIQUE NOT NULL,
    country TEXT,
    mobilenumber TEXT
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);
*/