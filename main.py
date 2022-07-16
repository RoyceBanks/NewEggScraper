from bs4 import BeautifulSoup
import requests
import re

search = input("What are you buying??")                                         #User Inputs Desired Item From Site    (One word input)

url= f"https://www.newegg.com/p/pl?d={search}&n=8000%204131"                    #Makes the URL with the search term
page = requests.get(url)                                                        #Searches the site
doc = BeautifulSoup(page.text, "html.parser")                                   #Turn it into Text

page_text = doc.find(class_="list-tool-pagination-text")                        #Looks for Number of pages
pages= int(str(page_text).split("/")[-3].split(">")[-1][:-1])                   #Number of pages

items_found = {}                                                                #Makes Dict for Items Found

for page in range(1,pages + 1):                                                 #Goes over all the pages
    url= f"https://www.newegg.com/p/pl?d={search}&n=8000%204131&page={page}"   
    page = requests.get(url)
    doc = BeautifulSoup(page.text, "html.parser")
    
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")


    items = div.find_all(text=re.compile(search))                               #Grabs Items
    for item in items:                                                          #For loop to go over each Item
        parent = item.parent                                                    #Gets parents class
        if parent.name !="a":                                                   #Skips unwanted parents 
            continue

        link = parent["href"]                                                   #Grabs Items Link
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").strong.string      #Grabs Items Price
            items_found[item] = {'price': int(price.replace(",", "")), 'link': link}    
        except:
            pass
    

sorted_items = sorted(items_found.items(), key=lambda x : x[1]['price'])    #Sorts Dict by price from least to greatest

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("----------------------------------------------------------------")

