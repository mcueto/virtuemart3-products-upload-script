"""Script utils."""


def insert_category(connection, connection_cursor, product, language='en_gb'):
    """
    Insert product category if doesn't exists...

    1- Search for category of product in your language
    1a- if exists the category id is returned(joomla_virtuemart_categories)
    1b- if doesn't, the category is created in joomla_virtuemart_categories and
        joomla_virtuemart_categories_xx_xx (your language)
    """
    try:
        sql_input = """SELECT * FROM `joomla_virtuemart_categories_es_es` WHERE `category_name`='{}';"""
        sql_input = sql_input.format(product["category"])
        result_count = connection_cursor.execute(sql_input)

        if(result_count is 0):
            sql_input = """INSERT INTO `joomla_virtuemart_categories` (`published`) VALUES ('1');"""
            connection_cursor.execute(sql_input)
            category_id = connection_cursor.lastrowid

            sql_input = """INSERT INTO `joomla_virtuemart_categories_es_es` (`virtuemart_category_id`, `category_name`, `slug`) VALUES ('{}', '{}', '{}');"""
            sql_input = sql_input.format(category_id, product["category"], product["category"])

            connection_cursor.execute(sql_input)
            return category_id
        else:
            result_set = connection_cursor.fetchall()
            return result_set[0][0]

    except Exception as e:
        connection.rollback()


def insert_products(connection, connection_cursor, product):
    """Insert the base product data into virtuemart mysql database."""
    try:
        sql_input = """INSERT INTO `joomla_virtuemart_products` (`virtuemart_vendor_id`, `product_sku`, `product_in_stock`, `product_special`, `product_params`, `published`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"""
        sql_input = sql_input.format('1', product["code"], product["stock"], '1', '\{\}', '1')
        connection_cursor.execute(sql_input)
        connection.commit()
        return connection_cursor.lastrowid
    except Exception as e:
        connection.rollback()


def insert_products_language(connection, connection_cursor, product,
                             product_id, language="en_gb"):
    """Insert product data specific for your store language."""
    try:
        sql_input = """INSERT INTO `joomla_virtuemart_products_es_es` (`virtuemart_product_id`, `product_s_desc`, `product_desc`, `product_name`, `slug`) VALUES ('{}', '{}', '{}', '{}', '{}');"""
        sql_input = sql_input.format(
            product_id,
            product["description"],
            product["description"],
            product["name"],
            product["name"]
        )
        connection_cursor.execute(sql_input)
        connection.commit()
        return connection_cursor.lastrowid
    except Exception as e:
        connection.rollback()


def asociate_product_category(connection, connection_cursor, product_id, category_id):
    """Associate product with category."""
    try:
        sql_input = """INSERT INTO `joomla_virtuemart_product_categories` (`virtuemart_product_id`, `virtuemart_category_id`) VALUES ('{}', '{}');"""
        sql_input = sql_input.format(
            product_id,
            category_id
        )
        connection_cursor.execute(sql_input)
        connection.commit()
        return connection_cursor.lastrowid
    except Exception as e:
        connection.rollback()
