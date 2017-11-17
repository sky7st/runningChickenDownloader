#coding=utf-8
import requests,re,cv2,urllib,sys,os
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk  ##py3  py2:import ttk
import json
import webbrowser
import threading
import time
from queue import Queue

class get_runninchicken_image:

    def __init__(self):
        self.__headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.__activity_list_url = "http://www.runninchicken.photos/api/get_activity_list"
        self.__album_list_url="http://www.runninchicken.photos/api/search_album_with_keyword?activity="
        self.__album_url = "http://www.runninchicken.photos/api/search_photo_with_keyword?keyword=&activity="
        self.__photo_url = "http://runninchicken-photo.nidbox.net"
        self.__rs = requests.Session()
    def get_activity_list(self):
        activity_sn_list=[]
        activity_sub_list = []
        __json_activity_list = self.__rs.get(self.__activity_list_url, headers = self.__headers).text
        if len(__json_activity_list)!=0:
            __json_activity_list = json.loads(__json_activity_list)
            for __info in __json_activity_list:
                if (__info['activity_sn']!=None):
                    activity_sn_list.append(__info['activity_sn'])
                    activity_sub_list.append(__info['activity_subject'])
            return activity_sn_list,activity_sub_list
        else:
            return activity_sn_list,activity_sub_list
    def get_album_list(self,choose_activity_sn):
        album_sn_list = []
        album_sub_list = []
        if choose_activity_sn!=-1:
            __new_album_list_url = self.__album_list_url + str(choose_activity_sn)
            __json_album_list = self.__rs.get(__new_album_list_url, headers = self.__headers).text
            __json_album_list = json.loads(__json_album_list)['list']
            for __info in __json_album_list:
                if(__info['album_sn']!=None):
                    album_sn_list.append(__info['album_sn'])
                    album_sub_list.append(__info['album_subject'])
            return album_sn_list,album_sub_list
        else:
            return album_sn_list,album_sub_list
    def get_photo_list(self,choose_activity_sn,choose_album_sn):
        choose_album_sn = str(choose_album_sn)
        choose_activity_sn = str(choose_activity_sn)
        photo_list = []
        if(len(choose_album_sn)!=0):
            __new_photo_list_url = self.__album_url + choose_activity_sn + "&album=" + (choose_album_sn)
            __json_photo_list = self.__rs.get(__new_photo_list_url,headers = self.__headers).text
            __json_photo_list = json.loads(__json_photo_list)['list']
            for __info in __json_photo_list:
                photo_list.append(__info['photo_url'])
            return photo_list
        else:
            return photo_list
    def get_photo_files(self,photo_list,resize):
        def __url_to_image(url):
            resp = urllib.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image
        photo_url_list=Queue()
        for photo_url in photo_list:
            __photo__file_fullurl = self.__photo_url + photo_url
            photo_url_list.put(__photo__file_fullurl)
##            __img = __url_to_image(__photo__file_fullurl)
##            if resize==True:
##                newWidth = 800
##                newHeight = int(__img.shape[0]*(float(800)/__img.shape[1]))
##                __img = cv2.resize(__img,(newWidth,newHeight))
       
##            cv2.imshow("img",__img)
##            if cv2.waitKey(0) & 0xff ==ord('q'):
##                cv2.destroyAllWindows()
##                sys.exit()
##            elif cv2.waitKey(0):
##                cv2.destroyAllWindows()
        return photo_url_list
class App(get_runninchicken_image):
    def __init__(self,master):
        chicken = get_runninchicken_image()
        master.title("攝影雞抓圖程式 by Sky7st")
        master.resizable(width=False, height=False)
        master.geometry('500x500')
        global __set_sn,__activity_url
        global album_sn,album_sub
        global __set_album_sn,__album_url
        __set_sn = -1
        __activity_url = ""
        album_sn = -1
        album_sub = ""
        label_chicken_url = ttk.Label(master, text = "點我造訪攝影雞",font=("", 13))
        label_choose_activitys = ttk.Label(master, text = "請選擇馬拉松場次",font=("", 10))
        def home_go(event):
            webbrowser.open_new("http://www.runninchicken.photos/")

        activity_sn,activity_sub =chicken.get_activity_list()
        activity_choose = tk.StringVar()
        combo_activity_choose = ttk.Combobox(master, width=20, textvariable=activity_choose ,state='readonly') 
        combo_activity_choose['values'] = activity_sub

        def choose_activity():
            global __set_sn,__activity_url
            global album_sn,album_sub
            if combo_activity_choose.current()!=-1:
                __set_sn = activity_sn[combo_activity_choose.current()]
                __activity_url= "http://www.runninchicken.photos/albumlist?act=" + __set_sn + "&key="
                button_activity_url.grid(column=3, row=2)
                album_sn,album_sub = chicken.get_album_list(__set_sn)
                combo_album_choose['values'] = album_sub
                button_album_choose = ttk.Button(master, text = "選擇相簿",  command = choose_album).grid(column=1, row=4)
                label_choose_album.grid(column=0, row=3)
                combo_album_choose.grid(column=0, row=4)
        
            else:
                __set_sn = -1
                __activity_url=""
        button_activity_choose =  ttk.Button(master, text='選擇場次', command = choose_activity)
        def activity_go():
            webbrowser.open_new(__activity_url)

        button_activity_url = ttk.Button(master, text = "點我查看賽事",  command = activity_go)   

        label_choose_album = ttk.Label(master, text = "請選擇相簿",font=("", 10))
        

        album_choose = tk.StringVar()
        combo_album_choose = ttk.Combobox(master, width=20, textvariable=album_choose ,state='readonly') 

        def choose_album():
            global __set_sn
            global __set_album_sn,__album_url
            global photo_list
            def download_all():
                    tStart = time.time()
                    photo_url_list = chicken.get_photo_files(photo_list, 0)
                    
##                    for i  in range(len(photo_list)):
##                        print photo_url_list.get()
                    threads = []    
                    for j in range(5):
                        c = Parser('c' + str(j),photo_url_list)
                        c.start()
                        threads.append(c)
                    for thread in threads:
                        thread.join()
                    tEnd = time.time()
                    total_time = tEnd - tStart
                    print ("Download finish!Total time: %d seconds")%(total_time)
                    
            if combo_album_choose.current()!=-1:
                __set_album_sn = album_sn[combo_album_choose.current()]
                __album_url="http://www.runninchicken.photos/album?act=" + __set_sn + "&key=&album=" + __set_album_sn
                button_album_url.grid(column=3, row=4)
                photo_list = chicken.get_photo_list(__set_sn,__set_album_sn)
                total_photo_num = ttk.Label(master, text = "共有%d張照片"%(len(photo_list))).grid(column=0, row=5)
                button_dowload_all = ttk.Button(master , text = "下載全部照片", command = download_all).grid(column=0, row=6)


        def album_go():
            webbrowser.open_new(__album_url)


        

        
        button_album_url = ttk.Button(master, text = "點我查看相簿",  command = album_go)

        label_chicken_url.grid(column=1, row=0)
        label_chicken_url.bind("<Button-1>", home_go)
        label_choose_activitys.grid(column=0, row=1)
        combo_activity_choose.grid(column=0, row=2)
        button_activity_choose.grid(column=1, row=2)
        
class Parser(threading.Thread):
    def __init__(self, name, photo_url_list):
        threading.Thread.__init__(self)
        self.name = name
        self.photo_url_list = photo_url_list
    def download(self,url):
        file_name = url.split("http://runninchicken-photo.nidbox.net/photo_file/")
        r = requests.get(url,stream = True)
        with open(file_name[1], 'wb') as f:
            f.write(r.content)
            f.close()
            print (file_name[1]," finish\n")
        
    def run(self):
        while self.photo_url_list.empty() is False:
            current_url = self.photo_url_list.get()
            self.download(current_url)

    
        
        
        
        


if __name__ =="__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
