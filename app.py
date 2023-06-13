import os
import time
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import variables as vars


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


def write_json_file(dictionary, file_name, file_id):
    # Writing to sample.json
    dir_name = "products"
    current_dir = os.getcwd()
    final_dir_name = os.path.join(current_dir, dir_name)
    file_name = file_name+'_'+file_id
    save_path = final_dir_name+'/'+file_name
    with open(save_path+'.json', "w") as outfile:
        json.dump(dictionary, outfile)


def braggsOpencart(url):
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
        thumbnails = content.find(
            "ul", {"class": "thumbnails"}).find_all('a')

        thumbnail_link_list = []
        for thumbnail_a in thumbnails:
            if thumbnail_a['href'].find("https://www.braggsschoolwear.co.uk/image/") != -1:
                thumbnail_link_list.append(thumbnail_a['href'])

        # product name
        cols = content.find_all("div", {"class", "col-sm-6"})
        product_name = cols[1].find("h1").text.strip()

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

        print(title)
        print("=============================")
        print(category)
        print(thumbnail_link_list)
        print(product_name)
        print("DESCRIPTION", prod_desc_paras)
        # print(product_status)
        print(pd_dic)
        print("")
        print("===============OPTIONS==============")
        print(label)
        print(options)

        product_dictionary = {
            "title": title,
            "category": category,
            "thumbnails": thumbnail_link_list,
            "product_name": product_name,
            "product_description_paragraphs": prod_desc_paras,
            # "product_code": product_code,
            # "product_status": product_status,
            "variant_choice": {"parameter": label, "options": options}
        }

        final_dic = {**product_dictionary, **pd_dic}
        print(final_dic)

        write_json_file(final_dic, product_name, "123")

    else:
        print(soup)


def router(elements, url):

    site = elements["netloc"]

    if site == 'www.braggsschoolwear.co.uk':
        print(site+" is a supported!")
        braggsOpencart(url)
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

    print("=======================PARSE URL START==========================")
    print(elements)
    print("=======================PARSE URL END==========================")
    return elements


state = True
while state:
    val = input("Product URL> : ")
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
            router(elements, url)
    else:
        print("No input, Downloader terminated!")
        state = False
