USE tracking;

DROP TABLE IF EXISTS `tracking`;

CREATE TABLE `tracking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` int(10),
  `mac` varchar(17),
  `organisation` varchar(50),
  `signal` int,
  `ssid` varchar(32),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
