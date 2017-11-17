#coding=utf-8
import requests
import re
import numpy as np
import Tkinter as tk
import ttk


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
url = "http://www.runninchicken.photos/"
activity_list = "http://www.runninchicken.photos/api/get_activity_list"
album_list_url="http://www.runninchicken.photos/api/search_album_with_keyword?activity=" 
album_url = "http://www.runninchicken.photos/api/search_photo_with_keyword?keyword=&activity="
photo_url = "http://www.runninchicken.photos/photo_file/"
def get_activity_list(res_activity_list):
    sel_option_val=[]
    patt_1 = re.compile(r'"activity_sn":"(\d*?)"',re.I|re.X)
    patt_2 = re.compile(r'"activity_subject":"(.*?)"',re.I|re.X)
    
    option_val = patt_1.findall(res_activity_list)
    option_sub = patt_2.findall(res_activity_list)
    for a in range(len(option_sub)):
        option_sub[a] = option_sub[a].decode('unicode_escape')
    return option_val,option_sub

def go_album_list(albumlist_act):
    list_url=album_list_url + albumlist_act + "&key="
    res_albumlist = requests.get(list_url,headers = headers).text
    patt_1 = re.compile(r'"album_sn":"(\d*?)"',re.I|re.X)
    patt_2 = re.compile(r'"album_subject":"(.*?)"',re.I|re.X)
    album_val =  patt_1.findall(res_albumlist)
    res_album_val=list(set(album_val))
    res_album_val.sort(key = album_val.index)
    res_album_sub = patt_2.findall(res_albumlist)
    for a in range(len(res_album_sub)):
        res_album_sub[a] = res_album_sub[a].decode('unicode_escape')
    return res_album_val,res_album_sub

def go_album(albumlist_act,album_act):
    photo_list_url =  album_url + albumlist_act + "&album=" + album_act
    photo_list = requests.get(photo_list_url,headers = headers).text
    patt_1 = re.compile(r'"photo_url":".\\/photo_file\\/(.*?)"')
    photo = patt_1.findall(photo_list)
    return photo


def window_main(list_option_val,list_option_sub):
    def choose_match():
        choose_num = matchChosen.current()
        albumlist_act = list_option_val[choose_num]
        res_album_val,res_album_sub = go_album_list(albumlist_act)
        if len(res_album_val) !=0:
            albumChosen['values'] = res_album_sub
            albumChosen.grid(column=0, row=3)
            action2.grid(column=2,row=3)
            ttk.Label(win, text = "選擇相簿").grid(column=0, row=2)
        return res_album_val,albumlist_act
    def choose_album():
        res_album_val,albumlist_act =choose_match()
        choose_num = albumChosen.current()
        album_act = res_album_val[choose_num]
        photo = go_album(albumlist_act,album_act)
        ttk.Label(win, text = "共有 %d 張"%(len(photo))).grid(column=0, row=4)
        download.grid(column=2, row=4)
        return photo
    def download_all():
        photo = choose_album()
        print album
        for a in range(len(photo)):
            r = requests.get(photo_url+photo[a],headers = headers,stream = True)
            with open ((photo[a]),'wb') as f:
                f.write(r.content)     
                print "已經下載%d/%d張"%(a+1,len(photo))
                f.close()


##        frame.grid(column=0, row=5)
##        a=0
##        pb = ttk.Progressbar(frame, length=300, mode='determinate',maximum=len(photo),variable=a)
##        pb.grid(column=0, row=0)
##        pb.start(0)

        
    
        
        
                

    
    win = tk.Tk()
    win.title("攝影雞")
    ttk.Label(win, text = "選擇場次").grid(column=0, row=0)

    match = tk.StringVar()
    matchChosen = ttk.Combobox(win, width=20, textvariable=match ,state='readonly')
    matchChosen['values'] =  list_option_sub
    matchChosen.grid(column=0, row=1)
    action = ttk.Button(win, text='Choose', command = choose_match)
    action.grid(column=2,row=1)
    album = tk.StringVar()
    albumChosen = ttk.Combobox(win,  width=20, textvariable=album ,state='readonly')
    action2 = ttk.Button(win, text='Choose', command = choose_album)

    download = ttk.Button(win, text='下載全部', command = download_all)
    frame = ttk.Frame()
    
    
    
    
    
    
    
        
    
    win.mainloop()


    
    
if __name__ == "__main__":


    res_activity_list = requests.get(activity_list,headers = headers).text

    #soup_index = bs(res_activity_list.text)
    activity_list_option_val,activity_list_option_sub = get_activity_list(res_activity_list)
    window_main(activity_list_option_val,activity_list_option_sub)
    
    
