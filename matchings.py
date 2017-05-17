import json
import collections

def readFile(filename):
    jsonList = []
    with open(filename) as json_file:
        for line in json_file:
            data = json.loads(line)
            jsonList.append(data)
        return jsonList

def createProductDictionary(productList):
    products = {}
    for json in productList:
        familyDict =  products.get(json['manufacturer'], {})
        if not familyDict:
            products[json['manufacturer']] = familyDict
        modelDict = familyDict.get(json.get('family', 'N/A'), {})
        if not modelDict:
            familyDict[json.get('family', 'N/A')] = modelDict
        productListing = modelDict.get(json.get('model', 'N/A'), '')
        if not productListing:
            modelDict[json.get('model', 'N/A')] = json
    return products

def matchProductsAndListings(productDictionary,listingsList):
    matches = {}
    for listing in listingsList:
        manufacturerFamilyDict = productDictionary.get(listing.get('manufacturer','N/A'),{})
        listingTitle = listing.get('title', '')
        if manufacturerFamilyDict and listingTitle:
            for family in manufacturerFamilyDict:
                if family in listingTitle or family == 'N/A':
                    modelDict = manufacturerFamilyDict[family]
                    for model in modelDict:
                        if model in listingTitle:
                            matches[modelDict[model]['product_name']] = matches.get(modelDict[model]['product_name'], []) + [listing]
                            break
                    break
    return matches



productList = readFile('data/products.txt')
productDictionary = createProductDictionary(productList)
listingsList = readFile('data/listings.txt')
matches = matchProductsAndListings(productDictionary,listingsList)


with open('results.txt', 'wb') as outfile:
    for obj in matches:
        writeObj = collections.OrderedDict()
        writeObj['product_name'] = obj
        writeObj['listings'] = matches[obj]
        json.dump(writeObj, outfile)
        outfile.write('\n')

"""
count = 0
for obj in matches:
    count += len(matches[obj])
print 'num listings matched :', count
"""
