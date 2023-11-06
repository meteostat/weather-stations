CREATE TABLE `stations` (
  `id` char(5) NOT NULL PRIMARY KEY,
  `country` varchar(2) DEFAULT NULL,
  `region` varchar(5) DEFAULT NULL,
  `latitude` float(8,4) DEFAULT NULL,
  `longitude` float(8,4) DEFAULT NULL,
  `elevation` int(4) DEFAULT NULL,
  `timezone` varchar(30) DEFAULT NULL
);

CREATE TABLE `stations_name` (
  `station` char(5) NOT NULL,
  `language` char(2) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`station`, `language`)
);
   
CREATE TABLE `stations_identifiers` (
  `station` char(5) NOT NULL,
  `key` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  PRIMARY KEY (`station`, `key`)
);