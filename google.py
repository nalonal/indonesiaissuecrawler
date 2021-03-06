import requests, re
import urllib.parse
import datetime as dt
from bs4 import BeautifulSoup

import config as cf

def decode(string):
	this_string = string
	decode_string = ['<', '"', '\'', '>', '&',]
	encode_string = ['&lt;', '&quot;', '&#039;', '&gt;', '&amp;']
	for e_string, d_string in zip(encode_string, decode_string):
		this_string = this_string.replace(e_string, d_string)
	for e_string, d_string in zip(encode_string[::-1], decode_string[::-1]):
		this_string = this_string.replace(e_string, d_string)
	return this_string

def encode(string):
	this_string = string
	decode_string = ['+']
	encode_string = [' ']
	for e_string, d_string in zip(encode_string, decode_string):
		this_string = this_string.replace(e_string, d_string)
	for e_string, d_string in zip(encode_string[::-1], decode_string[::-1]):
		this_string = this_string.replace(e_string, d_string)
	return this_string


def cleansing(perlink, persummary,pertime):
	perlink = perlink[0]
	summary = persummary[0]
	this_per = {}
	find_url = perlink.get('href').strip('/url?q=')
	delimeter_url = find_url.find('&')
	this_per['url'] = find_url[0:delimeter_url]
	this_per['title'] = perlink.select('.vvjwJb')[0].text
	this_per['summary'] = summary.text.replace("\n","")
	if(len(pertime) < 2):
		this_per['time'] = ""
	if(len(pertime) > 2):
		this_per['time'] = ""
	if(len(pertime) == 2):
		this_per['time'] = BeautifulSoup(str(pertime[0]), "html.parser").text
	return this_per

def google(cookie, keyword, num):
	this_search = []
	this_keyword = urllib.parse.quote(encode(keyword),encoding='utf-8')
	headers = {
	    'Host': 'developers.facebook.com',
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Accept-Encoding': 'deflate',
	    'Connection': 'keep-alive',
	    'Cookie': cookie,
	    'Upgrade-Insecure-Requests': '1',
	    'Cache-Control': 'max-age=0',
	    'TE': 'Trailers'
	    }
	url = "https://developers.facebook.com/tools/debug/echo/?q=https%3A%2F%2Fgoogle.com%2Fsearch?q%3D"+this_keyword+"%26num%3D"+str(num+1)
	google_search = requests.get(url, headers=headers)
	cleaned_response = decode(google_search.text)
	soup = BeautifulSoup(cleaned_response, 'html.parser')
	for perlink in soup.select(cf.class_list_of_search):
		if(len(perlink.select(cf.class_link_of_search)) > 0):
			try:
				this_search.append(cleansing(perlink.select(cf.class_link_of_search), perlink.select(cf.class_desc_of_search),perlink.select(cf.class_desc_of_time)))
			except:
				pass
	return this_search