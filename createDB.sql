USE tracking;

DROP TABLE IF EXISTS `proberequest`;

CREATE TABLE `proberequest` (
  `date` int(10) NOT NULL,
  `source` varchar(17) NOT NULL,
  `firm` varchar(50),
  `rssi` int,
  `ssid` varchar(32),
  PRIMARY KEY (`date`,`source`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
