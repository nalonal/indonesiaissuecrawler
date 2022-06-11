import google as gl
import config as cf
import requests
import urllib.parse
import datetime as dt
from csv import writer
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from datetime import date, timedelta, datetime
from calendar import monthrange

today = date.today()
days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]

print(Figlet(font='slant').renderText("LEONARDO"))
print("Indonesia News Crawler.")

def progressBar(bulan, current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    if(current != total):
        print("Mengambil berita bulan "+bulan+' Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
    else:
        print("Mengambil berita bulan "+bulan+' Progress: [%s%s] %d %%' % (arrow, spaces, percent))

def mdy_to_ymd(d):
    return datetime.strptime(d, '%b %d, %Y').strftime('%Y/%m/%d')

def ago2date(ago):
	if(ago.find('hour') > 0 or  ago.find('minute') > 0 ):
		time = today.strftime("%Y/%m/%d")
	elif(ago.find('day') > 0):
		this_day = dt.date.today()
		number = ago.split(' ')[0]
		gap_day = dt.timedelta(days=int(number))
		after = this_day - gap_day
		time = after.strftime("%Y/%m/%d")
	else:
		after = mdy_to_ymd(ago)
		time = after
	return time


akhir_bulan_lalu = today.replace(day=1) - timedelta(days=1)
awal_bulan_depan = today.replace(day=1) + timedelta(days_in_month(today))

gap_day = dt.timedelta(days=1)
this_day = dt.date.today()
after = this_day - gap_day
before = this_day + gap_day

input_keyword = input("Masukkan Keyword Pencarian Berita: ")
input_hari = input("Masukkan Durasi Bulan: ")

# input_keyword = "ivermectin"
# input_hari = "5"


keyword = str(input_keyword)
lama_waktu = str(input_hari)
dt_string = today.strftime("%Y%m%d_%H%M%S")

nama_file = "hasil/"+str(dt_string)+"_"+keyword


for i in range(int(lama_waktu)):
    no_daftar_link = 1
    for per_link in cf.daftar_link:
    	this_bulan = awal_bulan_depan-dt.timedelta(days=1)
    	progressBar(str(this_bulan.strftime("%m/%Y")),no_daftar_link, len(cf.daftar_link), barLength = 20)
    	news = per_link
    	final_keyword = "site:"+news+" intitle:"+keyword+" before:"+str(awal_bulan_depan)+" after:"+str(akhir_bulan_lalu)
    	hasil = gl.google(cf.cookie,final_keyword, 1000)
    	if(len(hasil) > 0):
            for info in hasil:
            	if(info['time'] != ""):
            		info['date'] = str(ago2date(info['time']))
            		info['sumber'] = news
            		output = info['date']+"\t"+info['title']+"\t"+info['summary']+"\t"+info['sumber']+"\t"+info['url']
            		# print(output)
            		writer = open(nama_file+'.csv','a')
            		writer.seek(0,2)
            		writer.writelines(output+"\r")
    	no_daftar_link = no_daftar_link+1
		
    gap_day = dt.timedelta(days=1)
    today = akhir_bulan_lalu
    akhir_bulan_lalu = today.replace(day=1) - timedelta(days=1)
    awal_bulan_depan = today.replace(day=1) + timedelta(days_in_month(today)) - gap_day

