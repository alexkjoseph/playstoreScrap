#You can find all the reqired packages in requirements.txt
#Or you can just install obsei 0.0.7
#Or you can use "pip install obsei"
#If nothing works use "!pip install git+https://github.com/lalitpagaria/obsei.git"
from obsei.source.playstore_scrapper import PlayStoreScrapperConfig, PlayStoreScrapperSource
from obsei.analyzer.classification_analyzer import ClassificationAnalyzerConfig, ZeroShotClassificationAnalyzer
from bs4 import BeautifulSoup as bs
import requests as rq
str1='https://play.google.com/store/search?q='
str2='&c=apps'
str3='https://play.google.com'
analyzer_config=ClassificationAnalyzerConfig(# initialize classification analyzer config
   labels=["positive","negative","neutral"], # here we can specify which label to be checked.
)
text_analyzer = ZeroShotClassificationAnalyzer(
   model_name_or_path="typeform/mobilebert-uncased-mnli", # Refer https://huggingface.co/models?filter=zero-shot-classification,for supported models
   device="auto" 
)

def webScraper(url):#This function will render the website for entered package name and find package heading, package name and link to package  
  html_text=rq.get(url).text
  soup=bs(html_text,'html.parser')
  heading=soup.find('div',attrs={'class':'WsMG1c nnK0zc'}).text #heading
  link_full=soup.find('a',attrs={'class':'poRVub'})['href'] # link to package 
  link_full_split=link_full.split("=")
  package_name=link_full_split[-1] #package name
  return heading,link_full,package_name

def similerWebScraper(product_url):#This function will render similer products website for the entered package name and find package heading list, package name list
  product=rq.get(product_url).text
  newSoup=bs(product)
  similer_link=newSoup.find('div',attrs={'class':'W9yFB'}).a['href']
  similer_url=str3+similer_link 
  similer_html=rq.get(similer_url).text #render similer products website
  similer_products_soup=bs(similer_html)
  similer_products_head=similer_products_soup.find_all('div',attrs={'class':'WsMG1c nnK0zc'})
  similer_products_package=similer_products_soup.find_all('a',attrs={'class':'poRVub'})
  similer_products_head_actual=[i.text for i in similer_products_head] #package heading list
  similer_products_link=[i['href'].split("=")[-1] for i in similer_products_package] #package name list
  return similer_products_head_actual,similer_products_link

def obseiAnalysis(package):
  source_config = PlayStoreScrapperConfig( # Need two parameters package name and country.    # `package name` can be found at the end of the url of app in play store.
    countries=["in"], # Country in ccTLD(country code top-level domain) format
    package_name=package,
    max_count=20, #count of reviews to be found
    lookup_period="2h" #Time period
  )
  source = PlayStoreScrapperSource() # initializes play store reviews retriever
  source_response_list = source.lookup(source_config) # This will fetch information from configured source
  analyzer_response_list = text_analyzer.analyze_input( # This will execute analyzer
      source_response_list=source_response_list,
      analyzer_config=analyzer_config
  )
  return analyzer_response_list

def Print(heading,analyzer_response_list): # This function will print the o/p as heading and positive or negative accodint to reviews
  print(heading+":")
  print("")
  for i in analyzer_response_list:
    if i.segmented_data['positive']<i.segmented_data['negative'] and i.segmented_data['neutral']<i.segmented_data['negative']:
      Response="Negative: "+i.processed_text
    elif i.segmented_data['positive']>i.segmented_data['negative'] and i.segmented_data['positive']>i.segmented_data['neutral']:
      Response="Positive: "+i.processed_text
    else:
      Response="Neutral: "+i.processed_text
    print("         "+Response)
  print("")
if __name__=="__main__":
  p="y"
  while p=="y":
    packageName=input("Enter name of App you want to install:") #Input App name
    similer_app_count=input("Enter the number of similer apps to be found[Default 15 maximum 35]:")#[Optional] Input similer app to be found
    if similer_app_count.isnumeric()and int(similer_app_count)<36:
      similer_app_count=int(similer_app_count)
    else:
      print("Default selected:15")
      similer_app_count=15
    url=str1+packageName+str2
    first_product_head,first_product_link_full,first_product_link=webScraper(url) #getting heading, package and link to first product
    sentimentAnalysis=obseiAnalysis(first_product_link) #Sentiment analysis of first product
    Print(first_product_head,sentimentAnalysis)#Outputting first product with review
    product_url=str3+first_product_link_full
    similer_products_head_actual,similer_products_link=similerWebScraper(product_url) #getting headings and packages  to similer products
    if similer_app_count>len(similer_products_head_actual):
      similer_app_count=len(similer_products_head_actual)
      print ("Sorry only {} similer products is available".format(len(similer_products_head_actual)))

    for i in range(similer_app_count):
        sentimentAnalysis=obseiAnalysis(similer_products_link[i]) #Sentiment analysis of similer products
        Print(similer_products_head_actual[i],sentimentAnalysis)#Outputting similer products with review
    p=input("Do you want to check another product (type y for check more more)").lower()
