create database PriceStock;

use PriceStock; 

CREATE TABLE `T_PriceStock` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `site_id` int(11) NOT NULL,
      `price` int(11) NOT NULL,
      `stock` int(11) NOT NULL,
      `update_date` date NOT NULL,
      `update_time` datetime NOT NULL,
      `server_id` int(11) NOT NULL,
      `url_crc` int(11) NOT NULL,
      PRIMARY KEY (`id`),
      KEY `idx` (`site_id`,`update_date`,`server_id`)
)
