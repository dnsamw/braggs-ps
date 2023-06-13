def toWooCommerceSchema(product_dict):

    print(product_dict)

    # ditermine product type
    product_type = ""
    if product_dict["variant_choice"] != {}:
        product_type = "variable"
    else:
        product_type = "simple"

    # assume sku = product code in braggs - PLEASE CONFIRM!!
    sku = product_dict["product_code"]

    # generate short string description

    short_description = ""
    for para in product_dict["product_description_paragraphs"]:
        short_description += para.replace(".", "")+". "

    # in braggs there is no long description so:
    long_description = short_description

    # parse availability
    is_in_stock = 0
    if product_dict["availability"] == "In Stock":
        is_in_stock = 1  # this is like a boolean

    # generate image string
    images_string = ""
    if product_dict["thumbnails"] != []:
        images_string = ','.join(product_dict["thumbnails"])

    woo_json = {
        "ID": product_dict["id"],
        "Type": product_type,
        "SKU": sku,
        "Name": product_dict["name"],
        "Published": 1,
        "Is featured?": 0,
        "Visibility in catalog": "visible",
        "Short description": short_description,
        "Description": long_description,
        "Date sale price starts": "",
        "Date sale price ends": "",
        "Tax status": "taxable",
        "Tax class": "",
        "In stock?": is_in_stock,
        "Stock": "",
        "Backorders allowed?": 0,
        "Sold individually?": 0,
        "Weight (lbs)": ".5",
        "Length (in)": 24,
        "Width (in)": 1,
        "Height (in)": 2,
        "Allow customer reviews?": 1,
        "Purchase note": "",
        "Sale price": "",
        "Regular price": "",
        "Categories": f"Schoolwear > {product_dict['category']}",
        "Tags": "",
        "Shipping class": "",
        "Images": images_string,
        "Download limit": "",
        "Download expiry days": "",
        "Parent": "",
        "Grouped products": "",
        "Upsells": "",
        "Cross-sells": "",
        "External URL": "",
        "Button text": "",
        "Position": 0,
        "Attribute 1 name": "Color",
        "Attribute 1 value(s)": "Blue, Green, Red",
        "Attribute 1 visible": 1,
        "Attribute 1 global": 1,
        "Attribute 2 name": "Size",
        "Attribute 2 value(s)": "Large, Medium, Small",
        "Attribute 2 visible": 1,
        "Attribute 2 global": 1,
        "Meta: _wpcom_is_markdown": 1,
        "Download 1 name": "",
        "Download 1 URL": "",
        "Download 2 name": "",
        "Download 2 URL": ""
    }

    return woo_json
