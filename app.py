import google as gl
import config as cf
import requests, re, urllib.parse
import datetime as dt
from csv import writer
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from datetime import date, timedelta, datetime
from calendar import monthrange

today = date.today()
tanggalwaktu = datetime.today()
days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]

print(Figlet(font='slant').renderText("LEONARDO"))
print("Indonesia News Crawler.")

def progressBar2(current, total, barLength = 20):
    percent = current*100 / int(total)
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print("Progress: "+'[%s%s] %d %%' % (arrow, spaces, percent), end='\r')

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
dt_string = tanggalwaktu.strftime("%Y%m%d_%H%M%S")

nama_file = "hasil/"+str(dt_string)+"_"+re.sub('[^A-Za-z0-9]+', '', keyword)

# print(nama_file)
for i in range(int(lama_waktu)):
    this_bulan = awal_bulan_depan-dt.timedelta(days=1)
    progressBar2(i,input_hari, barLength = 20)
    final_keyword = keyword+" before:"+str(awal_bulan_depan)+" after:"+str(akhir_bulan_lalu)
    hasil = gl.google(cf.cookie,final_keyword, 1000)
    if(len(hasil) > 0):
        for info in hasil:
            try:
                info['time'] = str(ago2date(info['time']))
            except:
                info['time'] = ""

            if(info['time'] != ""):
                info['date'] = info['time']
                output = info['date']+"\t"+info['title']+"\t"+info['summary']+"\t"+info['url']
                print(output)
                writer = open(nama_file+'.csv','a', encoding='utf-8')
                writer.seek(0,2)
                writer.writelines(output+"\r")
        
    gap_day = dt.timedelta(days=1)
    today = akhir_bulan_lalu
    akhir_bulan_lalu = today.replace(day=1) - timedelta(days=1)
    awal_bulan_depan = today.replace(day=1) + timedelta(days_in_month(today)) - gap_day

