import json
import collections
import re

def read_file(filename):
    jsonList = []
    with open(filename) as json_file:
        for line in json_file:
            data = json.loads(line)
            jsonList.append(data)
        return jsonList

def find_whole_word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def filter_listings(listings_list):
    sep_list = ['for' , 'pour', 'fur', 'with', 'avec']
    new_list = []
    for listing in listings_list:
        for for_word in sep_list:
            title = listing.get('title', '')
            match = find_whole_word(for_word)(title)
            if match:
                title = title[:match.start()]
            listing['title'] = title
            new_list.append(listing)
    return new_list



def create_product_dictionary(product_list):
    products = {}
    for product in product_list:
        manufacturer = product.get('manufacturer', '').lower()
        family = product.get('family','').lower()
        model = product.get('model', '').lower()
        if products.get(manufacturer, {}):
            if products[manufacturer].get(family,''):
                products[manufacturer][family].append((model,product))
            else:
                products[manufacturer][family] = [(model,product)]
        else:
            products[manufacturer] = {}
            products[manufacturer][family] = [(model,product)]
    return products

def match_products_and_listings(product_dictionary,listings_list):
    matches = {}
    for listing in listings_list:
        title = listing.get('title', '').lower()
        listing_manufacturer = listing.get('manufacturer', '').lower()
        if product_dictionary.get(listing_manufacturer):
            for family in product_dictionary[listing_manufacturer]:
                model_list = product_dictionary[listing_manufacturer][family]
                for model_tup in model_list:
                    if find_whole_word(model_tup[0])(title):
                        matches[model_tup[1]['product_name']] = matches.get(model_tup[1]['product_name'], []) + [listing]
                        break
                break
    return matches


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        products_filename = "data/products.txt"
        listings_filename = "data/listings.txt"
        results_filename = "data/results.txt"
    elif len(sys.argv) == 4:
        products_filename, listings_filename, results_filename = sys.argv[1:4]
    else:
        print("Usage: python " + sys.argv[0] + " [products_file, listings_file, results_file]")
        sys.exit()

    filtered_listing = filter_listings(read_file(listings_filename))
    product_dictionary = create_product_dictionary(read_file(products_filename))
    matches = match_products_and_listings(product_dictionary,filtered_listing)

    with open(results_filename, 'wb') as outfile:
        for obj in matches:
            write_obj = collections.OrderedDict()
            write_obj['product_name'] = obj
            write_obj['listings'] = matches[obj]
            json.dump(write_obj, outfile)
            outfile.write('\n')

    count = 0
    for obj in matches:
        count += len(matches[obj])
    print 'num listings matched :', count
