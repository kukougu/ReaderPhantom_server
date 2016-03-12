CREATE TABLE users
(
	username char(20),
	password char(20),
	sex char(10),
	phone char(11),
	star char(20),
	primary key(username)
);


CREATE TABLE booksclass
(
	ISBN varchar(13) binary,
	class char(30),
	primary key(ISBN),
	foreign key(ISBN) references `BX-Books`(ISBN)
);


CREATE TABLE friends(
	username char(20),
	friuser char(20),
	primary key(username, friuser),
	foreign key(username) references users(username)
);


CREATE TABLE history(
	username char(20),
	ISBN varchar(13) binary,
	score char(30),
	time char(30),
	primary key(username, ISBN),
	foreign key(username) references users(username),
	foreign key(ISBN) references `BX-Books`(ISBN)
);

CREATE TABLE insterest(
	username char(20),
	ISBN varchar(13) binary,
	primary key(username, ISBN),
	foreign key(username) references users(username),
	foreign key(ISBN) references `BX-Books`(ISBN)
);

CREATE TABLE comment(
	username char(20),
	ISBN varchar(13) binary,
	content char(255),
	time char(30),
	primary key(username, ISBN),
	foreign key(username) references users(username),
	foreign key(ISBN) references `BX-Books`(ISBN)
);