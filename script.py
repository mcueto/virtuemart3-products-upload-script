"""
Script to bulk upload virtuemart3 products from csv to mysql...

It's a script intended to be a quick reference in how to construct the insert
statements and define the csv file structure.
"""

# from random import randrange
import csv
import MySQLdb
import toml
import utils

# Open the TOML config file
with open("config.toml") as conffile:
    config = toml.loads(conffile.read())

connection = MySQLdb.connect(
    host=config["database"]["host"],
    user=config["database"]["user"],
    passwd=config["database"]["password"],
    db=config["database"]["db"],
    unix_socket=config["database"]["unix_socket"]
    )

connection_cursor = connection.cursor()

def main():

    with open("input.csv", 'rt') as input:
        reader = csv.reader(input, delimiter=',')

        for k, row in enumerate(reader):
            product = {
                'code': row[1],
                'name': row[2],
                'description': row[3],
                'price': row[4],
                'stock': row[5],
                'category': row[6]
            }

            if(product['code'] and product["name"] and product["price"] and product["stock"] and product["category"]):
                category_id = utils.insert_category(connection, connection_cursor, product, 'es_es')
                baseproduct_id = utils.insert_products(connection, connection_cursor, product)
                if(category_id and baseproduct_id):
                    asoc_id = utils.asociate_product_category(connection, connection_cursor, baseproduct_id, category_id)
                product_id = utils.insert_products_language(connection, connection_cursor, product, baseproduct_id, 'es_es')

    connection.close()

main()

print("Thanks for use :)")
