import os
import json
import pandas as pd
from datetime import datetime


# Dtermin Lst id  for current product id calculaton


def readLastId():
    # Opening JSON file
    with open('last_id.json', 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)

    return json_object["last_id"]


def writeLastId(current_id):
    # datetime object containing current date and time
    now = datetime.now()

    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    last_id_dic = {"last_id": int(
        current_id), "last_modified_date_time": dt_string}

    with open("last_id.json", "w") as outfile:
        json.dump(last_id_dic, outfile)


def createParetProduct(product_dict):

    # read last id fromthe json file and add 1 to it.
    parent_id = int(readLastId())+1

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
        "ID": parent_id,
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

    if product_dict["variant_choice"] != {}:
        woo_dict["Attribute 1 name"] = product_dict["variant_choice"]["parameter"]
        woo_dict["Attribute 1 value(s)"] = ','.join(
            product_dict["variant_choice"]["options"])
    else:
        woo_dict["Type"] = "simple"
        woo_dict["Attribute 1 visible"] = ""
        woo_dict["Attribute 1 global"] = ""

    # adding 1is not required here for variable products but in cas if in the futre we can use this forsimple products as well
    writeLastId(parent_id+1)
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
    # parent_id = int(product_dict["id"]) this methos is absndoned due to duplicate vatiant ids

    # read last id fromthe json file and add 1 to it.
    parent_id = int(readLastId())+1

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
            current_id_calc = 0
            for i, variation in enumerate(variants):
                current_iteration = i+1
                current_id_calc = parent_id+current_iteration
                print('CALCULATED CURENT PRODUCT ID : ', current_id_calc)
                woo_dict["ID"] = current_id_calc
                woo_dict["Attribute 1 value(s)"] = variation
                woo_dict["Tax class"] = "parent"
                woo_dict["Name"] = product_dict["name"] + \
                    " - " + str(variation)
                woo_dict["Position"] = current_iteration

                product_dict_arr.append(woo_dict.copy())

            # write the last variant id of the loop as the last id
            writeLastId(current_id_calc)

    return product_dict_arr


def toWooCommerceSchema(product_dict):
    # print(product_dict)

    product_dict_arr = []

    # ditermine product type
    product_type = ""
    if product_dict["variant_choice"] != {}:
        product_type = "variable"
        product_dict_arr = createProductVariations(product_dict)
        product_dict_arr.append(createParetProduct(product_dict))
    else:
        product_type = "simple"
        product_dict_arr = createParetProduct(product_dict)

    return product_dict_arr
