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
    with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["MPN","sku","Item Name", "Item Price", "Stock"])
        
        if file.tell() == 0:
            writer.writeheader()

        try:
            URL_LIST = [
                "https://www.build.com/product/summary/1569636",
                "https://www.build.com/product/summary/1884576",
                "https://www.build.com/product/summary/1332894",
                "https://www.build.com/product/summary/1332867",
                "https://www.build.com/product/summary/1317725"
            ]

            for url in URL_LIST:
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
            
                itemData = {}

                # Scrape model number (MPN)
                Model = soup.find("span", attrs={'data-automation': 'product-model-number'})
                if Model:
                    itemData["MPN"] = Model.text.strip()
                else:
                    itemData["MPN"] = None

                Item = soup.find("span", attrs={'data-automation': 'product-item-number'})
                if Item:
                    itemData["sku"] = Item.text.strip()
                else:
                    itemData["sku"] = None    

                # Scrape item name
                Name = soup.find("h1", class_="ma0 fw6 lh-title di f5 f3-ns")
                if Name:
                    itemData["Item Name"] = Name.text.strip()
                else:
                    itemData["Item Name"] = None

                # Scrape item price
                Price = soup.find("span", class_="b lh-copy")
                if Price:
                    # Match dollar value including commas and decimals
                    p = re.findall(r"\$([0-9,]+(?:\.\d{2})?)", Price.text)
                    if p:
                        # Remove commas but keep decimals
                        cleaned_price = p[0].replace(",", "")
                        
                        # Convert to float and format correctly to 2 decimal places
                        try:
                            formatted_price = float(cleaned_price)
                            itemData["Item Price"] = f"{formatted_price:.2f}"  # Force 2 decimal places
                        except ValueError:
                            itemData["Item Price"] = None
                            print(f"Error converting price: {cleaned_price}")
                    else:
                        itemData["Item Price"] = None
                        print("Price not found!")
                else:
                    itemData["Item Price"] = None
                # Scrape item stock
                Stk = soup.find("span", class_="theme-grey-darker lh-solid")
                if Stk:
                    itemData["Stock"] = Stk.text.strip()
                else:
                    itemData["Stock"] = None

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
#     with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=["MPN","Item Name", "Item Price", "Stock"])
        
#         if file.tell() == 0:
#             writer.writeheader()

#         try:
#             URL_LIST = [
#                 "https://www.build.com/product/summary/1569636",
#                 "https://www.build.com/product/summary/1884576",
#                 "https://www.build.com/product/summary/1332894",
#                 "https://www.build.com/product/summary/1332867",
#                 "https://www.build.com/product/summary/1317725"
#             ]

#             for url in URL_LIST:
#                 page = requests.get(url)
#                 soup = BeautifulSoup(page.text, 'html.parser')
            
#                 itemData = {}

#                 # Scrape model number (MPN)
#                 Model = soup.find("span", attrs={'data-automation': 'product-model-number'})
#                 if Model:
#                     itemData["MPN"] = Model.text.strip()
#                 else:
#                     itemData["MPN"] = None

#                 # Scrape item name
#                 Name = soup.find("h1", class_="ma0 fw6 lh-title di f5 f3-ns")
#                 if Name:
#                     itemData["Item Name"] = Name.text.strip()
#                 else:
#                     itemData["Item Name"] = None

#                 # Scrape item price
#                 Price = soup.find("span", class_="b lh-copy")
#                 if Price:
#                     # Match dollar value including commas and decimals
#                     p = re.findall(r"\$([0-9,]+(?:\.\d{2})?)", Price.text)
#                     if p:
#                         # Debugging: print out the captured price
#                         print(f"Original price text: {Price.text.strip()}")
#                         print(f"Captured price (raw): {p[0]}")

#                         # Remove commas but keep decimals
#                         itemData["Item Price"] = p[0].replace(",", "")
                        
#                         # Debugging: print the processed price
#                         print(f"Processed price: {itemData['Item Price']}")
#                     else:
#                         itemData["Item Price"] = None
#                         print("Price not found!")
#                 else:
#                     itemData["Item Price"] = None

#                 # Scrape item stock
#                 Stk = soup.find("span", class_="theme-grey-darker lh-solid")
#                 if Stk:
#                     itemData["Stock"] = Stk.text.strip()
#                 else:
#                     itemData["Stock"] = None

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
