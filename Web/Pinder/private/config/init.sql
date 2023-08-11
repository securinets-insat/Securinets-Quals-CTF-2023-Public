ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '98db257c426ad380e9c36ee7e5343087';
CREATE USER 'web'@'localhost' IDENTIFIED WITH mysql_native_password BY 'b0ab19395161ddea088fe7306fdf567b';
FLUSH PRIVILEGES;

DROP DATABASE IF EXISTS pinder;
CREATE DATABASE  pinder;
USE pinder;

CREATE TABLE  users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE profile (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    profile_picture_link TEXT NOT NULL,
    is_public BOOLEAN NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);



INSERT INTO users (username, password) VALUES ('admin', '98db257c426ad380e9c36ee7e5343087');

INSERT INTO profile (user_id, first_name,last_name,profile_picture_link,is_public) VALUES (1,'securinets{3bcc81811533d70940084c8}','last name','https://i.imgur.com/3ZQ3Z9A.jpg',1);

GRANT INSERT, SELECT ON pinder.users TO 'web'@'localhost';
GRANT INSERT, SELECT ON pinder.profile TO 'web'@'localhost';
FLUSH PRIVILEGES;