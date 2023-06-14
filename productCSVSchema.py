def createParetProduct(product_dict):
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

    woo_dict = {
        "ID": int(product_dict["id"]),
        "Type": "variable",
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
        "Stock": 50,
        "Backorders allowed?": 0,
        "Sold individually?": 0,
        "Weight (lbs)": ".5",
        "Length (in)": 24,
        "Width (in)": 1,
        "Height (in)": 2,
        "Allow customer reviews?": 1,
        "Purchase note": "",
        "Sale price": "",
        "Regular price": float(product_dict["product_price"]),
        "Categories": f"Schoolwear,Schoolwear > {product_dict['category']}",
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
        "Attribute 1 name": "",
        "Attribute 1 value(s)": "",
        "Attribute 1 visible": 1,
        "Attribute 1 global": 1,
        "Meta: _wpcom_is_markdown": 1,
        "Download 1 name": "",
        "Download 1 URL": "",
        "Download 2 name": "",
        "Download 2 URL": ""
    }

    woo_dict["Attribute 1 name"] = product_dict["variant_choice"]["parameter"]
    woo_dict["Attribute 1 value(s)"] = ','.join(
        product_dict["variant_choice"]["options"])

    return woo_dict


def createProductVariations(product_dict):

    # calculate variant id
    parent_id = int(product_dict["id"])

    # assume sku = product code in braggs - PLEASE CONFIRM!!
    sku = product_dict["product_code"]

    # parse availability
    is_in_stock = 0
    if product_dict["availability"] == "In Stock":
        is_in_stock = 1  # this is like a boolean

    # generate image string
    images_string = ""
    if product_dict["thumbnails"] != []:
        images_string = ','.join(product_dict["thumbnails"])

    woo_dict = {
        "ID": "",
        "Type": "variation",
        "SKU": "",
        "Name": product_dict["name"],
        "Published": 1,
        "Is featured?": 0,
        "Visibility in catalog": "visible",
        "Short description": "",
        "Description": "",
        "Date sale price starts": "",
        "Date sale price ends": "",
        "Tax status": "taxable",
        "Tax class": "",
        "In stock?": is_in_stock,
        "Stock": 50,
        "Backorders allowed?": 0,
        "Sold individually?": 0,
        "Weight (lbs)": ".5",
        "Length (in)": 24,
        "Width (in)": 1,
        "Height (in)": 2,
        "Allow customer reviews?": 0,
        "Purchase note": "",
        "Sale price": "",
        "Regular price": float(product_dict["product_price"]),
        "Categories": f"Schoolwear > {product_dict['category']}",
        "Tags": "",
        "Shipping class": "",
        "Images": images_string,
        "Download limit": "",
        "Download expiry days": "",
        "Parent": sku,
        "Grouped products": "",
        "Upsells": "",
        "Cross-sells": "",
        "External URL": "",
        "Button text": "",
        "Position": 0,
        "Attribute 1 name": "",
        "Attribute 1 value(s)": "",
        "Attribute 1 visible": " 1",
        "Attribute 1 global": 1,
        "Meta: _wpcom_is_markdown": 1,
        "Download 1 name": "",
        "Download 1 URL": "",
        "Download 2 name": "",
        "Download 2 URL": ""
    }

    product_variations = product_dict["variant_choice"]
    product_dict_arr = []
    if product_variations != {}:
        attribute = product_variations["parameter"]
        variants = product_variations["options"]
        if len(variants) > 0:
            woo_dict["Attribute 1 name"] = attribute
            for i, variation in enumerate(variants):
                current_iteration = i+1
                print(parent_id+current_iteration)
                woo_dict["ID"] = parent_id + current_iteration
                woo_dict["Attribute 1 value(s)"] = variation
                woo_dict["Tax class"] = "parent"
                woo_dict["Name"] = product_dict["name"] + \
                    " - " + str(variation)
                woo_dict["Position"] = current_iteration

                product_dict_arr.append(woo_dict.copy())

    return product_dict_arr


def toWooCommerceSchema(product_dict):
    print(product_dict)

    product_dict_arr = []

    # ditermine product type
    product_type = ""
    if product_dict["variant_choice"] != {}:
        product_type = "variable"
        product_dict_arr = createProductVariations(product_dict)
        product_dict_arr.append(createParetProduct(product_dict))
    else:
        product_type = "simple"

    return product_dict_arr
