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
    "  `category` int(2) unsigned NOT NULL,"
    "  `name` varchar(200) NOT NULL,"
    "  `note` int(2) NOT NULL,"
    "  `shops` varchar(50) NOT NULL,"
    "  `url` varchar(150) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `fk_category_name` FOREIGN KEY (`category`) "
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

add_product_category = "INSERT INTO categories (category_name) VALUES (%s)"
add_product = "INSERT INTO products (category, name, note, shops, url) SELECT id, %s, %s, %s, %s \
               FROM categories where category_name = %s"

all_categories = "SELECT id, category_name FROM categories"

best_product_in_category = "SELECT categories.category_name, products.name, products.note, \
                                   products.shops, products.url FROM categories \
                            INNER JOIN products ON categories.id = products.category \
                            WHERE category = %s \
                            ORDER BY note ASC"
