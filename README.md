# Access-Control-Web-UI
## This app is made to run in the Raspberry Pi, usgin Python and the Flask framework
### This is part of the Access Control Desktop App, the app can be found in this Repo : [Access Control Desktop App](https://github.com/medyas/Access-Control-desktop-App)
also, the full database is exported and was added to the desktop app repo, which you can import in the mysql with :
```
gunzip < [dataBase.sql.gz]  | mysql -u [user] -p[password] [databasename] 
```
create the users table in the database, and add users which will have acces to the web app

```
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(30) NOT NULL,
  `lastname` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(50) NOT NULL,
  `edit_per` tinyint(1) NOT NULL,
  `add_per` tinyint(1) NOT NULL,
  `block_per` tinyint(1) NOT NULL,
  `delete_per` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) 

```

create the blocked employee database, which will include the employees from to blocked time

```
CREATE TABLE `blocked_employee` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `user_id` int(8) unsigned DEFAULT NULL,
  `block_start` datetime NOT NULL,
  `block_end` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ub_id` (`user_id`),
  CONSTRAINT `ub_id` FOREIGN KEY (`user_id`) REFERENCES `employees` (`id`)
) 

```

