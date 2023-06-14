import os
import sys
import time
import requests
from bs4 import BeautifulSoup
import json
import csv
from urllib.parse import urlparse
import variables as vars
import productCSVSchema as WOO
import ast


def scan_page(url):
    print(vars.bcolors.OKBLUE + "Scanning page.."+vars.bcolors.ENDC)
    result = requests.get(url, headers={"User-Agent": "AppleTV6,2/11.1"})
    print(result.status_code)
    # print(result.headers)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, 'lxml')
        return soup
    else:
        return vars.bcolors.FAIL + "Sorry the page not found!, check the url and retry."+vars.bcolors.ENDC


def write_csv_file(dictionary, file_name, file_id):

    # print("HIIIII", dictionary[0].keys())

    dir_name = "products_csv"
    current_dir = os.getcwd()
    final_dir_name = os.path.join(current_dir, dir_name)
    file_name = file_name+'_'+file_id
    save_path = final_dir_name+'/'+file_name

    # data_file = open(save_path+'.csv', 'w', newline='')
    # with open(save_path+'.csv', 'w') as csvfile:
    #     w = csv.DictWriter(csvfile, to_csv[0].keys())
    #     w.writeheader()
    #     w.writerow(to_csv)
    keys = dictionary[0].keys()

    with open(save_path+'.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dictionary)


def write_json_file(dictionary, file_name, file_id):
    # Writing to sample.json
    dir_name = "products"
    current_dir = os.getcwd()
    final_dir_name = os.path.join(current_dir, dir_name)
    file_name = file_name+'_'+file_id
    save_path = final_dir_name+'/'+file_name
    with open(save_path+'.json', "w") as outfile:
        json.dump(dictionary, outfile)


def braggsOpencartProductScrape(url, product_id):
    soup = scan_page(url)
    if not isinstance(soup, str):

        # product title
        title = soup.find("title").text.strip().replace("|", "-")

        # product category
        product = soup.find("div", {"id": "product-product"})
        breadcrumbs = product.find("ul", {"class", "breadcrumb"})
        breadcrumbsList = breadcrumbs.find_all('a')
        category = breadcrumbsList[1].text.strip()

        # product images
        content = soup.find("div", {"id": "content"})
        thumbs_obj = content.find(
            "ul", {"class": "thumbnails"})  # .find_all('a')

        if (thumbs_obj != None):
            thumbnails = thumbs_obj.find_all('a')
            thumbnail_link_list = []
            for thumbnail_a in thumbnails:
                if thumbnail_a['href'].find("https://www.braggsschoolwear.co.uk/image/") != -1:
                    thumbnail_link_list.append(thumbnail_a['href'])
        else:
            thumbnail_link_list = []

        # product name
        cols = content.find_all("div", {"class", "col-sm-6"})
        product_name = cols[1].find("h1").text.strip()

        # product sale price
        product_price = cols[1].find("h2").text.replace("\u00a3", "").strip()

        # product desctiption
        prod_desc_tab = content.find("div", {"id": "tab-description"})
        desc_paras = prod_desc_tab.find_all("p")
        prod_desc_paras = []
        if desc_paras != []:
            for para in desc_paras:
                prod_desc_paras.append(para.text.strip().replace("\n", ""))

        # product code
        prod_details_cols = cols[1].find_all("ul", {"class", "list-unstyled"})
        prod_details_list = prod_details_cols[0].find_all("li")

        pd_dic = {}

        for p in prod_details_list:
            parts_arr = p.text.strip().split(":")
            pd_dic[parts_arr[0].strip().replace(" ", "_").lower()
                   ] = parts_arr[1].strip()
        # product_code = prod_details_list[0].text.replace(
        #     "Product Code:", '').strip()

        # # product availability
        # product_status = prod_details_list[1].text.replace(
        #     "Availability:", '').strip()

        # product options
        selectors = cols[1].find("div", {"id": "product"}).find_all(
            "div", {"class", "form-group"})

        label = selectors[0].find("label").text.strip()
        optionsList = selectors[0].find_all("option")
        optionsList.pop(0)  # remove 1st item which is --- Please Select ---

        options = []
        for option in optionsList:
            options.append(option.text.strip().replace(
                ' ', '').replace('\n', ''))

        print(vars.bcolors.OKCYAN + title+vars.bcolors.ENDC)

        product_dictionary = {
            "id": product_id,
            "name": title,
            "category": category,
            "thumbnails": thumbnail_link_list,
            "product_name": product_name,
            "product_description_paragraphs": prod_desc_paras,
            "product_price": product_price,
            # "product_status": product_status,
            "variant_choice": {"parameter": label, "options": options}
        }

        final_dic = {**product_dictionary, **pd_dic}
        print(final_dic)

        woo_product_dictionary = WOO.toWooCommerceSchema(final_dic)

        # here we pass woo dictionary instead of final dictionary
        write_json_file(final_dic, product_name, product_id)
        # write_json_file(woo_product_dictionary, product_name, product_id)
        write_csv_file(woo_product_dictionary, product_name, product_id)

    else:
        print(soup)


def braggsOpencartCategoryScrape(url):
    soup = scan_page(url)
    if not isinstance(soup, str):
        # category title
        title = soup.find("title").text.strip().replace("|", "-")
        print(vars.bcolors.OKGREEN + title + vars.bcolors.ENDC)

        # products
        content = soup.find("div", {"id": "content"})
        product_cards = content.find_all("div", {"class", "product-layout"})
        # print(product_cards)
        product_links = []
        for card in product_cards:
            link = card.find("a")
            href = link["href"]
            product_links.append(href)

        for url in product_links:
            print(vars.bcolors.WARNING +
                  "Curently Scraping "+vars.bcolors.ENDC, url)
            braggsOpencartProductScrape(url)
            for i in range(5, 0, -1):
                print(vars.bcolors.OKCYAN +
                      f"Next product will be scraped in {i}"+vars.bcolors.ENDC, end="\r", flush=True)
                time.sleep(1)


def router(elements, url, type):
    # extractproduct id
    product_id = elements["queries"][2].replace(
        "product_id=", "").strip()

    site = elements["netloc"]

    if site == 'www.braggsschoolwear.co.uk':
        print(site+" is a supported!")
        if type == "product":
            braggsOpencartProductScrape(url, product_id)
        elif type == "category":
            # categoryscraper
            print("CATEGORY SCRAPER")
            braggsOpencartCategoryScrape(url)
        else:
            print("We can't scrape types other than products or categories for now")

    else:
        print(site)
        print("Unsupported site: please contact the developer")


def url_parser(url):

    parts = urlparse(url)
    directories = parts.path.strip('/').split('/')
    queries = parts.query.strip('&').split('&')

    elements = {
        'scheme': parts.scheme,
        'netloc': parts.netloc,
        'path': parts.path,
        'params': parts.params,
        'query': parts.query,
        'fragment': parts.fragment,
        'directories': directories,
        'queries': queries,
    }

    # print("=======================PARSE URL START==========================")
    # print(elements)
    # print("=======================PARSE URL END==========================")
    return elements


state = True
while state:
    print("\n")
    print(vars.bcolors.FAIL + "TODO:"+vars.bcolors.ENDC,
          "extract product id from query params and append to name")
    print(vars.bcolors.FAIL + "TODO:"+vars.bcolors.ENDC,
          "this typy of posts break the loop, fix it", "route=product/product&path=87&product_id=505")
    print("\n")

    val = input("Product/Category URL> : ")
    if val != "":
        if val == "help":
            vars.getHelp()
        elif val == "version":
            print(vars.bcolors.OKGREEN + "\ndnsamScraper" +
                  vars.bcolors.ENDC + " v1.0 - june 2023.\n")
        elif val == "info":
            vars.getInfo()
        elif val == "list":
            vars.getList()
        elif val == "exit" or val == "x":
            print("program exit")
            state = False
        else:
            url = str(val).strip()
            elements = url_parser(url)
            if elements["queries"][0] == "route=product/category":
                print("PRODUCT CATEGORY URL")
                # router(elements, url, "category")
            elif elements["queries"][0] == "route=product/product":
                print("SINGLE PRODUCT URL")
                router(elements, url, "product")
            else:
                print("Don't know anything about this URL type yet. Contact Dileepa.")
    else:
        print("No input, Downloader terminated!")
        state = False
