import os
import pandas as pd
from datetime import datetime


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
    }

    woo_dict["Attribute 1 name"] = product_dict["variant_choice"]["parameter"]
    woo_dict["Attribute 1 value(s)"] = ','.join(
        product_dict["variant_choice"]["options"])

    return woo_dict


def combineCSV():
    dir_name = "products_csv"
    current_dir = os.getcwd()
    final_dir_path = os.path.join(current_dir, dir_name)
    # list all the files from the directory
    csv_file_list = os.listdir(final_dir_path)
    # print(csv_file_list)

    df_append = pd.DataFrame()
    # append all files together
    for file in csv_file_list:
        df_temp = pd.read_csv(final_dir_path+"/"+file,
                              encoding='unicode_escape')
        df_append = df_append._append(df_temp, ignore_index=True)

    print(df_append)
    final_out_dir_path = os.path.join(current_dir, "output_csv")
    # datetime object containing current date and time
    now = datetime.now()

    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    output_path = final_out_dir_path+'\products-d-' + \
        dt_string.replace("/", "-").replace(" ",
                                            "-t-").replace(":", "_")+'.csv'
    print(output_path)

    df_append.to_csv(output_path)


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
        "Weight (lbs)": "",
        "Length (in)": "",
        "Width (in)": "",
        "Height (in)": "",
        "Allow customer reviews?": 0,
        "Purchase note": "",
        "Sale price": "",
        "Regular price": float(product_dict["product_price"]),
        "Categories": "",
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
        "Attribute 1 visible": "",
        "Attribute 1 global": 1,
        "Meta: _wpcom_is_markdown": 1,
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
