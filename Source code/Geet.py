import tkinter as tk
from tkinter import filedialog
import requests
import time
from bs4 import BeautifulSoup
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import random
from tkinter import messagebox as mb
from pathlib import Path

screen = tk.Tk()
screen.title("Geet")
screen.geometry("270x150")
string = tk.StringVar(screen)
string2 = tk.StringVar(screen)
var = tk.IntVar(screen)
url = ""
down_pth = ""
stg = "|"
driver = ""
th2 = ""
cond = True

def setvar(value,colour = "Black"):
    string.set("")
    tk.Label(screen,textvariable = string,fg = colour).place(x = 76,y = 43)
    string.set(value)
    tk.Label(screen,textvariable = string,fg = colour).place(x = 76,y = 43)

def set_downstats(value,colour = "Black"):
    string2.set(value)
    tk.Label(screen,textvariable = string2,fg = colour).place(x = 76,y = 64)

def check_download():
    global stg,driver,down_pth,color
    z = ""
    old_lst = os.listdir(down_pth)
    x = 0
    while cond:
        new_lst = os.listdir(down_pth)
            
        if new_lst != old_lst:
            z = set(new_lst) - set(old_lst)
            z = str(z)
            z = z.replace("{","")
            z = z.replace("}","")
            z = z.strip("'")
            print(z)
            if Path(z).suffix == '.mp3':
                set_downstats("|"*54+"100%","green")
                driver.quit()
                x = 0
                mb.showinfo("Geet","Download complete")
                case = var.get()
                if case :
                    os.chdir(down_pth)
                    os.startfile(z)
                break
            
        x+=1
         
        if x<=52:
            set_downstats(stg,"blue")
            per = str(int(len(stg)/0.54))+"%"
            stg = per.rjust(x,"|")
            time.sleep(random.uniform(0.1,1))

def start_down():
    global url,down_pth,driver,th2,cond
    set_downstats("Searching song","blue")
    path = os.getcwd()
    if not down_pth:
        down_pth = path
        print(down_pth)
    Song_name = sn.get()
    Artist_name = an.get()
    if Artist_name != "(Optional)":
        Song_name = Song_name+" by "+Artist_name
    try:
        url = 'https://www.youtube.com/results?q=' + Song_name
        sc = requests.get(url)
        sctext = sc.text
        soup = BeautifulSoup(sctext,"html.parser")
        songs = soup.findAll("div",{"class":"yt-lockup-video"})
        song = songs[0].contents[0].contents[0].contents[0]
        songurl = song["href"]
        url = "https://www.youtube.com"+songurl
    except:
        cond = False
        set_downstats("Song not found!","red")
        mb.showwarning("Geet",f"Could not find {Song_name}\nEnter few more lyrics or Artist name")
        return
    print(url,down_pth)
    threading.Thread(target = check_download).start()
    chromeOptions=Options()
    chromeOptions.add_experimental_option("prefs",{"download.default_directory":down_pth})
    chromeOptions.add_argument("--headless")
    driver=webdriver.Chrome(path+"/chromedriver.exe",options=chromeOptions)
    driver.get("https://ytmp3.cc/en13/")
    driver.maximize_window()
    driver.find_element_by_xpath("//*[@id='mp3']").click()
    driver.find_element_by_xpath("//*[@id='input']").send_keys(url)
    driver.find_element_by_xpath("//*[@id='submit']").click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="buttons"]/a[1]').click()

def Download():
    global th2,cond
    time.sleep(0.5)
    cond = True
    threading.Thread(target=start_down).start()
    time.sleep(1)
    
def Browse_folder():
    global down_pth
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        down_pth = folder_selected.replace("/","\\")
        setvar(down_pth[:30]+"...","green")

S_name = tk.Label(screen,text="Song Name").grid(row = 0,column = 0)
sn = tk.Entry(screen,width = 30)
sn.grid(row = 0,column = 1)
A_name = tk.Label(screen,text = "Artist Name").grid(row = 1,column = 0)
an = tk.Entry(screen,width = 30)
an.insert("end","(Optional)")
an.grid(row = 1,column = 1)
browse = tk.Button(screen,text = "Browse",command = Browse_folder,width = 7).place(x = 55,y = 115)
btn = tk.Button(screen,text = "Download",command = Download,width = 7).place(x = 155,y = 115)
tk.Label(screen,text = "Download to: ").grid(row = 2,column = 0)
tk.Label(screen,text = "Status: ").grid(row = 3,column = 0)
var.set(1)
che = tk.Checkbutton(screen,text="Play song after downloading",variable=var).place(x = 5,y = 82)
setvar(os.getcwd()[:30]+"...","blue")
set_downstats("None","blue")
screen.mainloop()

