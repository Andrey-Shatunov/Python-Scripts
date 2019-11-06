# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
import unicodedata
import csv

START_DATE = '19-10-2019'
TYPE = "1MFR_F"


def get_key():
	url = 'https://www.moex.com/ru/derivatives/open-positions.aspx'
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	evenvalodation = soup.select_one('input#__EVENTVALIDATION')

	return evenvalodation['value']


def get_page_for_day(strdate, evenvalodation):
	date = datetime.datetime.strptime(strdate, '%d-%m-%Y')
	url = 'https://www.moex.com/ru/derivatives/open-positions.aspx'
	data = { "__EVENTTARGET":"",
			"__EVENTARGUMENT":"",
			"__VIEWSTATE":"",
			"__EVENTVALIDATION":evenvalodation,
			"ctl00$PageContent$frmInstrumList": TYPE,
			"ctl00$PageContent$frmDateTime$CDateDay": date.day,
			"ctl00$PageContent$frmDateTime$CDateMonth": date.month,
			"ctl00$PageContent$frmDateTime$CDateYear": date.year,
			"ctl00$PageContent$frmButtom": "Показать"
	}

	req =  requests.post(url, data)
	return req.text

	
def parse_response(strdate, res):
	clean_text = unicodedata.normalize("NFKD",res)
	columns = [strdate]
	soup = BeautifulSoup(clean_text, 'html.parser')
	table = soup.find("table", {"class": "table1 _full-width table1"})
	trs = table.find_all('tr')
	for i in range(3, 7):
		tds = trs[i].find_all('td')
		for td in tds[1:]:
			columns.append(td.text.replace(' ', ''))

	return columns


def generate_csv(start_date, end_date, evenvalodation):
	table = []
	while(start_date < end_date):
		print(start_date)
		str_start_date = start_date.strftime('%d-%m-%Y')
		page = get_page_for_day(str_start_date, evenvalodation)
		pars_list = parse_response(str_start_date, page)
		with open('result.csv', 'a', newline='') as myfile:
		    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, dialect='excel')
		    wr.writerow(pars_list)

		table.append(pars_list)
		start_date = start_date + datetime.timedelta(days=1)


if __name__ == "__main__":
	start_date = datetime.datetime.strptime(START_DATE, '%d-%m-%Y')
	end_date = datetime.datetime.now()
	evenvalodation = get_key()
	generate_csv(start_date, end_date, evenvalodation)

		