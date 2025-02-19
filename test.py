# import re
# import requests
# from bs4 import BeautifulSoup
# import logging
# import csv

# # ----------------------------- LOGGER ------------------------------
# def loggerInit(logFileName):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
#     file_handler = logging.FileHandler(f'logs/{logFileName}')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(formatter)
#     logger.addHandler(stream_handler)
#     return logger

# logger = loggerInit(logFileName="build.log")

# # -------------------------------------------------------------------

# def scrapperUnit():
#     # Open CSV file for writing the data
#     with open('products.csv', mode='w') as file:
#         writer = csv.DictWriter(file, fieldnames=["MPN","sku","Item Name", "Item Price", "Stock"])
        

#         if file.tell() == 0:
#             writer.writeheader()

#         try:
#             URL_LIST = [
#                 "https://www.tgw.com/p/nike-mens-dri-fit-victory-golf-pants",
#                 "https://www.tgw.com/p/nike-mens-victory-1-2-zip-golf-pullover",
#                 "https://www.tgw.com/p/nike-jordan-rise-gx-structured-cb-golf-hat"
#             ]

#             for url in URL_LIST:
#                 page = requests.get(url)
#                 soup = BeautifulSoup(page.text, 'html.parser')
            
#                 itemData = {}
                
#                 # Scrape model number (MPN)
#                 # Model = soup.find("span", attrs={'data-automation': 'product-model-number'})
#                 # if Model:
#                 #     itemData["MPN"] = Model.text.strip()
#                 # else:
#                 #     itemData["MPN"] = None

#                 # Scrape sku
#                 Item = soup.find_all("span", attrs={'partnumber':"P171715"})
#                 if Item:
#                     itemData["sku"] = Item.text.strip()
#                 else:
#                     itemData["sku"] = None    

#                 # Scrape item name
#                 # Name = soup.find("h1", class_="ma0 fw6 lh-title di f5 f3-ns")
#                 # if Name:
#                 #     itemData["Item Name"] = Name.text.strip()
#                 # else:
#                 #     itemData["Item Name"] = None

#                 # Scrape item price
#                 # Price = soup.find("span", class_="b lh-copy")
#                 # if Price:
#                 #     p = re.findall(r"\$([0-9,]+(?:\.\d{2})?)", Price.text)
#                 #     if p:
#                 #         itemData["Item Price"] = p[0].replace(",", "")
#                 #     else:
#                 #         itemData["Item Price"] = None
#                 #         print("Price not found!")
#                 # else:
#                 #     itemData["Item Price"] = None

#                 # Scrape item stock
#                 # Stk = soup.find("span", class_="theme-grey-darker lh-solid")
#                 # if Stk:
#                 #     itemData["Stock"] = Stk.text.strip()
#                 # else:
#                 #     itemData["Stock"] = None

#                 # Write the item data into the CSV file
#                 writer.writerow(itemData)

#                 # Print item data
#                 print(itemData)

#         except Exception as e:
#             logger.error(f"error in scrapper Unit: {e}")

# if __name__ == "__main__":
#     try:
#         scrapperUnit()
#     except Exception as e:
#         logger.error(f"error in main: {e}")

import re
import requests
from bs4 import BeautifulSoup
import logging
import csv

# ----------------------------- LOGGER ------------------------------
def loggerInit(logFileName):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(f'logs/{logFileName}')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

logger = loggerInit(logFileName="build.log")

# -------------------------------------------------------------------

def scrapperUnit():
    # Open CSV file for writing the data
    with open('products.csv', mode='w') as file:
        writer = csv.DictWriter(file, fieldnames=["MPN", "sku", "Item Name", "Item Price", "Stock"])

        if file.tell() == 0:
            writer.writeheader()

        try:
            # Read the URLs from 'url_list.csv'
            URL_LIST = []
            with open('product_urls.csv', mode='r') as url_file:
                url_reader = csv.reader(url_file)
                # Skip header if exists, uncomment the next line if there's a header
                # next(url_reader)
                for row in url_reader:
                    if row:
                        URL_LIST.append(row[0])  # Assuming URLs are in the first column

            # Now scrape data from each URL in the list
            for url in URL_LIST:
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')

                itemData = {}

                # Scrape sku
                Item = soup.find("span",class_="a-type-h2 m-buy-box-header__name")
                if Item:
                    itemData["sku"] = Item[0].text.strip()  # Updated to take first element from list
                else:
                    itemData["sku"] = None    

                # Write the item data into the CSV file
                writer.writerow(itemData)

                # Print item data
                print(itemData)

        except Exception as e:
            logger.error(f"error in scrapper Unit: {e}")

if __name__ == "__main__":
    try:
        scrapperUnit()
    except Exception as e:
        logger.error(f"error in main: {e}")
