
import os, sys, shutil
import time
import tkinter as tk
from tkinter import filedialog
import sqlite3
import re

text = []

print(os.getcwd())

database_path = os.path.join(os.path.dirname(__file__), 'data', 'dube.db')


def progress(status, remaining, total):
    print(f'Copied {total - remaining} of {total} pages...')


def back_up_des_path():
    location_f = open('location.txt', 'r+')
    text = []
    for line in location_f.readlines():
        text.append(line)
    root = tk.Tk().withdraw()
    floder_path = filedialog.askdirectory()
    print(floder_path)
    if floder_path == '':
        pass
    else:
        location_f.truncate(0)  ##刪除內容
        location_f.seek(0)  ##移動到最前面
        text[1] = floder_path
        for lines in text:
            location_f.writelines(lines)
        location_f.close()




def way_to_backup(des_path,system_name):
    src = sqlite3.connect(database_path)
    dst = sqlite3.connect(des_path + '/' + system_name + '.db')
    with dst:
        src.backup(dst, pages=1, progress=progress)
    dst.close()
    src.close()


def backup_dube():
    db = sqlite3.connect(database_path)
    text = []
    location_f = open('location.txt', 'r')
    for line in location_f:
        text.append(line)
    src_path = text[0]
    des_path = text[1]
    des_path = des_path.replace('\n','')
    print(des_path)
    CURRENT_TIME = time.strftime("%Y-%m-%d_%H_%M", time.localtime())
    TODAY_TIME = time.strftime("%Y-%m-%d", time.localtime())
    system_name = CURRENT_TIME + "_DubeSystemBackup"
    files = os.listdir(des_path)
    if files == []:
        way_to_backup(des_path, system_name)
    else:
        for file in files:
            reg = re.compile(TODAY_TIME)
            reg_search = reg.search(file)
            if reg_search is None: ### 不同日期的新增資料庫
                print('sdfghjkl')
                print(des_path + '/' + file)
                way_to_backup(des_path,system_name)
                break

            else: ### 有同天日期的複寫資料庫
                print(des_path + '/' + file)
                os.remove(des_path + '/' + file)
                way_to_backup(des_path, system_name)
                break


    # ###做備份動作
    # def progress(status, remaining, total):
    #     print(f'Copied {total - remaining} of {total} pages...')
    # src = sqlite3.connect('dube.db')
    # dst = sqlite3.connect(des_path+'/'+system_name+'.db')
    # with dst:
    #     src.backup(dst, pages=1, progress=progress)
    # dst.close()
    # src.close()






