<b>Synopsis</b>

This project was added to fulfill the requirements of the interview challenge presented by Sortable at https://sortable.com/challenge/.

<b>Running Instructions</b>

This project runs on Python 2.7.
```
python matchings.py
```
A file named "results.txt" will be created in the data directory containing the results of the program.

You can also pass the program three command line arguments specifying alternate products, listings, and results files, like so:
```
python matchings.py products-file listings-file results-file
```

<b>Motivation</b>

This challenge is an example of Record Linkage, Entity Resolution or Reference Reconciliation. The file data/products.txt contains unique product items and the file data/listings.txt contains listings of different products by third party vendors. The aim of this challenge is to find a one-many correspondence between the products and the listings.

<b>Efficiency</b>

Each product is processed and hashed once. Each listing is processed once. The number of times we attempt to hash it only depends on the length of its title and the number of families the manufacturer produces. If these have constant bounds, then the program runs in O(m + n), where m is the number of products and n is the number of listings.

<b>Algorithm</b>

The basic idea behind this approach is that a listing is matched with a product if and only if the product manufacturer and model appear in the listing title, and exactly one product is matched with the listing. From this idea, we apply several refinements to improve the amount of matches and eliminate false positives.

A dictionary is used to store mappings from tuples of (manufacturer, family, model names) to sets of products. This enables average case O(1) lookup for any product in the dictionary. The vast majority of products are uniquely identified by the manufacturer and model name pair, but there are a couple of products which share the same manufacturer and model name.

For most listings, it is necessary and sufficient that we find exactly one product that has the same manufacturer as given in the listing, and whose model appears within the listing. However, there could be subtle differences between the model name as listed in products.txt and the way the listings list the model. For example, products.txt might give the model name as "QV 3000EX", whereas in a listing the model is given as "QV3000 EX". Something else to consider when checking a listing is if we check for a model "T30", but the listing is in fact for a model "T30i" device.

In order to handle that, I used a regular expression which only matches a word by allowing for spaces or hyphens between characters in the model name and also ensures that model names which are prefixes of other model names do not match return results for the former when the listing is actually for the latter. The Regex is also case sensitive so as not to miss 'FUJIFILM' and 'Fujifilm'.

I also observed that there are listings where there are a lot of listings after the word 'for' or 'with' so I  filtered listings out by removing anything after words such as 'for' or 'with'.
