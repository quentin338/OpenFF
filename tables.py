TABLES = {}

TABLES['Categories'] = (
    "CREATE TABLE IF NOT EXISTS `Categories` ("
    "  `id` int(2) unsigned NOT NULL AUTO_INCREMENT,"
    "  `category_name` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['Products'] = (
    "CREATE TABLE IF NOT EXISTS `products` ("
    "  `id` int(5) unsigned NOT NULL AUTO_INCREMENT,"
    "  `category_product` int(2) unsigned NOT NULL,"
    "  `name_product` varchar(100) NOT NULL,"
    "  `note_product` int(2) NOT NULL,"
    "  `shops` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `fk_category_name` FOREIGN KEY (`category_product`) "
    "     REFERENCES `Categories` (`id`) "
    ") ENGINE=InnoDB")

TABLES['History'] = (
    "CREATE TABLE IF NOT EXISTS `History` ("
    "  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,"
    "  `id_initial_product` int(5) unsigned NOT NULL,"
    "  `id_new_product` int(5) unsigned NOT NULL,"
    "  `date` date NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `fk_history_id_initial_product` FOREIGN KEY (`id_initial_product`) "
    "     REFERENCES `Products` (`id`) ,"
    "  CONSTRAINT `fk_history_id_new_product` FOREIGN KEY (`id_new_product`) "
    "     REFERENCES `Products` (`id`) "
    ") ENGINE=InnoDB")