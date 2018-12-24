import requests


### Connecting to OpenFF and getting the first 10 categories ###

get_all_categories = requests.get('https://fr.openfoodfacts.org/categories?json=true')
first_ten_categories = get_all_categories.json()['tags'][:10]

### URL of categories are the names with "-" in between. Loop to work with one category at a time. ###

number_of_products = 20  # Need to make this variable in other file ?

for category in first_ten_categories:
    category_name = category["name"]
    category_name_for_url = category_name.replace(" ", "-")

    full_url = 'https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=' \
               + category_name_for_url + \
               '&sort_by=unique_scans_n&page_size=' \
               + str(number_of_products) + \
               '&json=true'

### GET a list of X products from full_url ###

    get_x_products = requests.get(full_url)

    list_products = get_x_products.json()["products"]

### Excluding all products with no fr notes, no name, no stores + TBD ###

    for each_product in list_products:
        if '-- fr' in each_product['nutrition_score_debug'] and each_product['generic_name'] != "" and each_product['stores_tags']:

            ### Notes are on the form X | -X | XX at the end of the string

            note_product = each_product['nutrition_score_debug'][len(each_product['nutrition_score_debug']) - 2:]
            note_product = note_product.strip()

            name_product = each_product['generic_name']

            selling_points = each_product['stores_tags']

            product_url = each_product['url']

            print(name_product, 'NOTE ' + note_product, 'URL ' + product_url)
            # print(selling_points)
        else:
            pass
