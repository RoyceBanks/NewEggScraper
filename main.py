from bs4 import BeautifulSoup
import requests
import re

search = input("What are you buying??")

url= f"https://www.newegg.com/p/pl?d={search}&n=8000%204131"
page = requests.get(url)
doc = BeautifulSoup(page.text, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text")
pages= int(str(page_text).split("/")[-3].split(">")[-1][:-1])

items_found = {}

for page in range(1,pages + 1):
    url= f"https://www.newegg.com/p/pl?d={search}&n=8000%204131&page={page}"
    page = requests.get(url)
    doc = BeautifulSoup(page.text, "html.parser")
    
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")


    items = div.find_all(text=re.compile(search))
    for item in items:
        parent = item.parent
        if parent.name !="a":
            continue

        link = parent["href"]
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").strong.string
            items_found[item] = {'price': int(price.replace(",", "")), 'link': link}
        except:
            pass
    

sorted_items = sorted(items_found.items(), key=lambda x : x[1]['price'])    

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("----------------------------------------------------------------")


#prices = doc.find_all(text="$")
#parent = prices[0].parent
#strong = parent.find("strong")
#print ("$",strong.string)




