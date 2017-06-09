USE tracking;

DROP TABLE IF EXISTS `proberequest`;

CREATE TABLE `proberequest` (
  `date` int(10) NOT NULL,
  `source` varchar(17) NOT NULL,
  `ap` varchar(17) NOT NULL,
  `organisation` varchar(50),
  `signal` int,
  `ssid` varchar(32),
  PRIMARY KEY (`date`,`source`,`ap`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
