import requests
import base64
from bs4 import BeautifulSoup
import csv
import time
import json
import time

FILENAME = "......csv"
f1 = open(FILENAME , 'a',encoding = 'utf-8')
writer = csv.writer(f1)

def read_sitemap():
   f = open('....txt')
   line = f.readline()
   list_of_data = []
   while line:
      a=0
      if a>=0:
         try:
            line=line.strip()
            result=parser_html(line)
            list_of_data.append(result)
            if(result!=0):
               writer.writerows(result)
         except:
            time.sleep(10)
      line = f.readline()
   f.close()
   f1.close()

  
def parser_html(url):
   r = requests.get(url)
   result_review = []
   soup = BeautifulSoup(r.text, "html.parser")
   usr_ = url.strip()+' '
   id = url.split('/')[len(url.split('/'))-1]
   title = soup.find('meta',{'name':'sailthru.title'})['content'].strip()
   description = soup.find('div',{'class':'description'}).text.strip()
   gen_rating=soup.find('div',{'class':'row averageRating ratingText'})
   gen_rating=gen_rating.find('strong').text
   url_en = url+'/reviewhtml/all/en'
   url_de = url+'/reviewhtml/all/de'
   url_nl = url+'/reviewhtml/all/nl'
   url_es = url+'/reviewhtml/all/es'
   url_fr = url+'/reviewhtml/all/fr'
   r_en = requests.get(url_en)
   r_de = requests.get(url_de)
   r_nl = requests.get(url_nl)
   r_es = requests.get(url_es)
   r_fr = requests.get(url_fr)
   soup_en = BeautifulSoup(r_en.text, "html.parser")
   soup_de = BeautifulSoup(r_de.text, "html.parser")
   soup_nl = BeautifulSoup(r_nl.text, "html.parser")
   soup_es = BeautifulSoup(r_es.text, "html.parser")
   soup_fr = BeautifulSoup(r_fr.text, "html.parser")
                           
   li_en = soup_en.find_all('li',{'class':'review-entry'})
   li_de = soup_de.find_all('li',{'class':'review-entry'})
   li_nl = soup_nl.find_all('li',{'class':'review-entry'})
   li_es = soup_es.find_all('li',{'class':'review-entry'})
   li_fr = soup_es.find_all('li',{'class':'review-entry'})
   
   result = []
   list_of_review =[]
   
   for i in li_en:
      rating = eval(i.find('div',{'class':'rating js-ratingCalc'})['data-rating'])
      rev_rating = rating['rating']
      author = i.find('div',{'class':'author'}).text.strip()
      date = i.find('div',{'class':'date'}).text.strip()
      rev_text = i.find('div',{'class':'content'}).text.strip()
      rev_title = i.find('div',{'class':'title'}).text.strip()
      result=[id,usr_,title,description,gen_rating,author,date,rev_title,rev_text,rev_rating]
      list_of_review.append(result)

   for i in li_de:
      rating = eval(i.find('div',{'class':'rating js-ratingCalc'})['data-rating'])
      rev_rating = rating['rating']
      author = i.find('div',{'class':'author'}).text.strip()
      date = i.find('div',{'class':'date'}).text.strip()
      rev_text = i.find('div',{'class':'content'}).text.strip()
      rev_title = i.find('div',{'class':'title'}).text.strip()
      result=[id,usr_,title,description,gen_rating,author,date,rev_title,rev_text,rev_rating]
      list_of_review.append(result)

   for i in li_nl:
      rating = eval(i.find('div',{'class':'rating js-ratingCalc'})['data-rating'])
      rev_rating = rating['rating']
      author = i.find('div',{'class':'author'}).text.strip()
      date = i.find('div',{'class':'date'}).text.strip()
      rev_text = i.find('div',{'class':'content'}).text.strip()
      rev_title = i.find('div',{'class':'title'}).text.strip()
      result=[id,usr_,title,description,gen_rating,author,date,rev_title,rev_text,rev_rating]
      list_of_review.append(result)

   for i in li_es:
      rating = eval(i.find('div',{'class':'rating js-ratingCalc'})['data-rating'])
      rev_rating = rating['rating']
      author = i.find('div',{'class':'author'}).text.strip()
      date = i.find('div',{'class':'date'}).text.strip()
      rev_text = i.find('div',{'class':'content'}).text.strip()
      rev_title = i.find('div',{'class':'title'}).text.strip()
      result=[id,usr_,title,description,gen_rating,author,date,rev_title,rev_text,rev_rating]
      list_of_review.append(result)

   for i in li_fr:
      rating = eval(i.find('div',{'class':'rating js-ratingCalc'})['data-rating'])
      rev_rating = rating['rating']
      author = i.find('div',{'class':'author'}).text.strip()
      date = i.find('div',{'class':'date'}).text.strip()
      rev_text = i.find('div',{'class':'content'}).text.strip()
      rev_title = i.find('div',{'class':'title'}).text.strip()
      result=[id,usr_,title,description,gen_rating,author,date,rev_title,rev_text,rev_rating]
      list_of_review.append(result)

   
   if len(list_of_review)==0:
      list_of_review.append([id,usr_,title,description,0,'none','','',''])
   return list_of_review
      
   

if __name__ == "__main__":
	startTime = time.time()
	read_sitemap()
	print(time.time()-startTime)

