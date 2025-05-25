from bs4 import BeautifulSoup #used for parsing the html code
import requests # type: ignore # used for imple menting the http methods
url = "https://saamaan.pk/collections/accessories-and-gadgets"

content = requests.get(url).content
# # checking 

response = requests.get(url).status_code
print(response)


print(content)

soup = BeautifulSoup(content, "html.parser")

titles = soup.find_all(class_ = "product-item__title text--strong link")

print(titles)


for title in titles:
    print(title.text)