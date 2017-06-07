DROP TABLE IF EXISTS `tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracking` (
  `id` int NOT NULL,
  `date` date,
  `mac` varchar(17),
  `organisation` varchar(50),
  `signal` int,
  `ssid` varchar(32)
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
