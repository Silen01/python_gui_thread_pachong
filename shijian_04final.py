from tkinter import *
from tkinter import scrolledtext
import requests
import json
import threading
import time
import queue
import tkinter
from lxml import etree
from urllib.parse import urlencode

ct1 = 0
ct2 = 0
ct3 = 0
ct4 = 0
mes_list = []
p_list=[]
myqueue = queue.Queue()

#页数
start_number1=0
start_number2=0
start_number3=0
start_number4=0

root=Tk()
root.title("gui多线程爬虫")
root['width']=800
root['height']=600


class Producer(threading.Thread):
    result = []
    def __init__(self, threadname, ret):
        threading.Thread.__init__(self, name = threadname)
        self.result = ret
    def run(self):
        global myqueue
        myqueue.put(self.result)
        time.sleep(0.1)

class Consumer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        global myqueue
        if not myqueue.empty():
            item = myqueue.get()
            scr.insert(END, self.getName() +"\n")
            for i in item:
                scr.insert(END,self.getName()+" "+i['id']+ " " +i['title']+ " " +i['rate']+" "+i['url']+ " " + '\n')

def Craw_movie(url):
    html = requests.get(url).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
    movie = json.loads(html)
    result = []
    if movie and 'subjects' in movie.keys():
        for item in movie.get('subjects'):
            film = {
                'rate': item.get('rate'),
                'title': item.get('title'),
                'url':item.get('url'),
                'id':item.get('id')}
            result.append(film)

    return result

def MyEvent1():
    global ct1
    ct1 = 1 - ct1
    if ct1 == 1 :
         global start_number1
         data = {
            'type': 'movie',
            'tag': '华语',
            'sort': 'recommend',
            'page_limit': 20,
            'page_start': start_number1
         }
         url = 'https://movie.douban.com//j/search_subjects?' + urlencode(data, 'utf-8')
         start_number1=start_number1+20

         ret = Craw_movie(url)
         p = Producer ("Producer " + str(len(mes_list)),ret)
         p.start()
         p_list.append(p)
         c = Consumer('Consumer' + str(len(mes_list)))
         mes_list.append(c)

def MyEvent2():
    global start_number2
    global ct2
    ct2 = 1 - ct2
    if ct2 == 1:
        data = {
            'type': 'movie',
            'tag': '欧美',
            'sort': 'recommend',
            'page_limit': 20,
            'page_start': start_number2
        }
        url = 'https://movie.douban.com//j/search_subjects?' + urlencode(data, 'utf-8')
        start_number2 = start_number2 + 20

        ret = Craw_movie(url)
        p = Producer("Producer " + str(len(mes_list)), ret)
        p.start()
        p_list.append(p)
        c = Consumer('Consumer' + str(len(mes_list)))
        mes_list.append(c)

def MyEvent3():
    global start_number3
    global ct3
    ct3 = 1 - ct3
    if ct3 == 1:
        data = {
            'type': 'movie',
            'tag': '韩国',
            'sort': 'recommend',
            'page_limit': 20,
            'page_start': start_number3
        }
        url = 'https://movie.douban.com//j/search_subjects?' + urlencode(data, 'utf-8')
        start_number3 = start_number3 + 20

        ret = Craw_movie(url)
        p = Producer("Producer " + str(len(mes_list)), ret)
        p.start()
        p_list.append(p)
        c = Consumer('Consumer' + str(len(mes_list)))
        mes_list.append(c)

def MyEvent4():
    global start_number4
    global ct4
    ct4 = 1 - ct4
    if ct4 == 1:
        data = {
            'type': 'movie',
            'tag': '日本',
            'sort': 'recommend',
            'page_limit': 20,
            'page_start': start_number4
        }
        url = 'https://movie.douban.com//j/search_subjects?' + urlencode(data, 'utf-8')
        start_number4 = start_number4 + 20

        ret = Craw_movie(url)
        p = Producer("Producer " + str(len(mes_list)), ret)
        p.start()
        p_list.append(p)
        c = Consumer('Consumer' + str(len(mes_list)))
        mes_list.append(c)

scrolW = 150 # 设置文本框的长度
scrolH = 80 # 设置文本框的高度
scr = scrolledtext.ScrolledText(root, width=scrolW, height=scrolH)
scr.place(x=10,y=10,width=780,height=440)


c1=Checkbutton(root,text="华语",onvalue=1,offvalue=0,command= MyEvent1)
c1.place(x=20,y=450,width=100,height=40)


c2=Checkbutton(root,text="欧美",onvalue=1,offvalue=0,command= MyEvent2)
c2.place(x=210,y=450,width=100,height=40)


c3=Checkbutton(root,text="韩国",onvalue=1,offvalue=0,command= MyEvent3)
c3.place(x=400,y=450,width=100,height=40)


c4 = Checkbutton(root,text="日本",onvalue=1,offvalue=0,command=MyEvent4)
c4.place(x=590,y=450,width=100,height=40)

def close():
    global mes_list
    mes_list = []
    scr.delete(0.0, END)

def begin():
    global mes_list
    for i in mes_list:
        if not i.is_alive():
            i.start()
    mes_list = []

button = Button(root, text='get', font=('宋体',12), command=begin)
button.place(x=210,y=500,width=60,height=40)
button = Button(root, text='clear', font=('宋体',12), command=close)
button.place(x=420,y=500,width=60,height=40)

root.mainloop()