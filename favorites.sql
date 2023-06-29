CREATE DATABASE IF NOT EXISTS engine;

CREATE TABLE favorites ( 
    id INT(8) UNSIGNED NOT NULL auto_increment, 
    title VARCHAR(255) default NULL, 
    artist VARCHAR(255) default NULL, 
    PRIMARY KEY (id)  
) AUTO_INCREMENT=1;

