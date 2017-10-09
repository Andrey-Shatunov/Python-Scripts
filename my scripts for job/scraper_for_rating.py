import requests
import base64
from bs4 import BeautifulSoup
import csv
import time
import json
import time

FILENAME = "raiting.csv"
f1 = open(FILENAME , 'a',encoding = 'utf-8')
writer = csv.writer(f1)

def read_sitemap():
   f = open('sitemapmedicine1_1.txt')
   line = f.readline()
   list_of_data = []
   while line:
      a=0
      if a>=0:
         try:
            line=line.strip()
            result=parser_html(line)
            writer.writerows(result)
         except:
            time.sleep(1)
      line = f.readline()
   f.close()
   f1.close()
   print(i)

  
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

   list_of_review = [[id,gen_rating]]
   return list_of_review
      

if __name__ == "__main__":
	startTime = time.time()
	read_sitemap()
	print(time.time()-startTime)
	f1.close()
