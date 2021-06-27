from bs4 import BeautifulSoup as bs
import requests as rq
str1='https://www.amazon.in/s?i=electronics&bbn=1389432031&rh=n%3A1389432031%2Cp_36%3A'
str2='-'
Low_price=int(input("Enter the lower range:"))
high_Price=int(input("Enter the higher range:"))
url=str1+str(Low_price)+'00'+str2+str(high_Price)+'00'
html_text=rq.get('https://www.flipkart.com/search?q=mobiles&p%5B%5D=facets.price_range.from%3D10000&p%5B%5D=facets.price_range.to%3D20000').text
soup=bs(html_text,'lxml')
jobs=soup.find('div',attrs={'class':'_4rR01T'}).text
print (jobs)