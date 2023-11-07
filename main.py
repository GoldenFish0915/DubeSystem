import tkinter as tk
from tkinter import ttk,Listbox,Text,CHECKBUTTON,messagebox
import sqlite3
import re
from datetime import datetime
import openpyxl
import pandas as pd
import os
import shutil
import time
import io

import backup

def PetChipComparison(petChip,PetChip10,Petchip15): # 晶片碼比對
    chip_10 = '^[0-9,A-Z]{10}$'  # 10碼晶片
    chip_15 = '^[0-9]{15}$'  # 15碼晶片
    PetChip10 = re.search(chip_10, str(petChip))
    Petchip15 = re.search(chip_15, str(petChip))
    return PetChip10,Petchip15



# 數字計算
def lenght_cul(n):
    sum = 0
    while n > 0 :
        sum = sum + 1
        n = n//10
    return sum



### 正規表達式的function
def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None





database_path = os.path.join(os.path.dirname(__file__), 'data', 'dube.db')
# db = sqlite3.connect(database_path)

db = sqlite3.connect('dube.db')

db.create_function("REGEXP", 2, regexp) ##正規表達式的函式







cursor = db.cursor()
window = tk.Tk()
# window.geometry('2000x768')
window.attributes('-fullscreen', True)
window.config(bg='grey')
window.title('Dube System')





tabcontrol = ttk.Notebook(window)
tabcontrol.pack(fill='both',expand=True) #分頁位置

tab1 = ttk.Frame(tabcontrol)
tabcontrol.add(tab1,text='飼主資料')

tab2 = ttk.Frame(tabcontrol)
tabcontrol.add(tab2,text='寵物資料')

tab3 = ttk.Frame(tabcontrol)
tabcontrol.add(tab3,text='住宿資料')

tab4 = ttk.Frame(tabcontrol)
tabcontrol.add(tab4,text='美容資料')

tab5 = ttk.Frame(tabcontrol)
tabcontrol.add(tab5,text='匯出付款資料')

tab6 = ttk.Frame(tabcontrol)
tabcontrol.add(tab6,text='總資料',state='hidden')

tab7 = ttk.Frame(tabcontrol)
tabcontrol.add(tab7,text='登入後台')

tab8 = ttk.Frame(tabcontrol)
tabcontrol.add(tab8,text='主人資料',state='hidden')

tab9 = ttk.Frame(tabcontrol)
tabcontrol.add(tab9,text='備份位址',state='hidden')

tabcontrol.select(tab1)






###########主人資料

#搜尋飼主電話
title_label = tk.Label(tab1,text='若須 修改、刪除 ，請搜尋飼主電話',font=('Arial', 10))
title_label.place(relx=0.02,rely=0.1)
label_tab2_2 = tk.Label(tab1,text='電話')
label_tab2_2.place(relx=0.02,rely=0.14)
#電話輸入
master_seacher_phone = tk.Entry(tab1)
master_seacher_phone.place(relx=0.02,rely=0.18)

#飼主標題
mastertitle = tk.Label(tab1,text='飼主資料',font=('Arial', 20))
mastertitle.place(relx=0.02,rely=0.02)
#分隔線
cut_label = ttk.Separator(tab1,orient='horizontal')
cut_label.pack(fill=tk.X,pady=170)



#輸入飼主的 身分證字號、姓名、電話、地址
label_1 = tk.Label(tab1,text='身分證字號 (A123456789)')
label_1.place(relx=0.3,rely=0.4)
tab1_id_entry = tk.Entry(tab1)
tab1_id_entry.place(relx=0.3,rely=0.44)
label_2 = tk.Label(tab1,text='姓名')
label_2.place(relx=0.5,rely=0.4)
tab1_name_entry = tk.Entry(tab1)
tab1_name_entry.place(relx=0.5,rely=0.44)
label_3 = tk.Label(tab1,text='電話 (0911111111)')
label_3.place(relx=0.3,rely=0.55)
tab1_phone_entry = tk.Entry(tab1)
tab1_phone_entry.place(relx=0.3,rely=0.59)
label_4 = tk.Label(tab1,text='地址')
label_4.place(relx=0.5,rely=0.55)
tab1_address_entry = tk.Entry(tab1)
tab1_address_entry.place(relx=0.5,rely=0.59)
#輸出新增結果
result_master = tk.Label(tab1)
result_master.place(relx=0.3,rely=0.3)
#輸出查詢結果
result_master_seacher = tk.Label(tab1)
result_master_seacher.place(relx=0.5,rely=0.18)

result_pet_seacher = tk.Label(tab2)
result_pet_seacher.place(relx=0.5,rely=0.18)

result_stay = tk.Label(tab3)
result_stay.place(relx=0.5,rely=0.18)

def master_entry_delete():
    tab1_id_entry.delete(0, 'end')
    tab1_name_entry.delete(0, 'end')
    tab1_phone_entry.delete(0, 'end')
    tab1_address_entry.delete(0, 'end')




def master_insert():
    message = []
    customId = tab1_id_entry.get()
    idtest = re.search('^[A-Z][12][0-9]{8}$',str(customId))
    customName = tab1_name_entry.get()
    customPhone = tab1_phone_entry.get()
    phonetest = re.search('^09[0-9]{8}$',str(customPhone))
    customAddress = tab1_address_entry.get()
    if customId != "":
        if idtest is None:
            message.append('ID格式有誤!!')
    else:
        message.append('身份證字號為必填欄位。')
    if customPhone != "":
        if phonetest is None:
            message.append('電話格式有誤!!')
    else:
        message.append('電話號碼為必填欄位。')
    check = "select * FROM mastertab WHERE mid = ? OR mphone = ?"
    cursor.execute(check,[customId,customPhone])
    checkdata = cursor.fetchall()
    if len(checkdata) != 0:
        messagebox.showinfo('注意!', "已有此人資料")
    else:
        if not message:
            #result_master.configure(text=customName + '已加')
            sql = 'insert into mastertab(mid, mname, mphone, maddress)values(?, ?, ?, ?)'
            val = (customId, customName, customPhone, customAddress)
            cursor.execute(sql, val)
            db.commit()
            result = "身分證字號:"+customId+"  姓名:"+customName+"  電話:"+customPhone+"  地址:"+customAddress
            messagebox.showinfo('新增成功!', str(result))
            master_entry_delete()

        else:
            tk.messagebox.showwarning(title='警告!', message=message)




def master_seacher():
    tab1_id_entry.delete(0,'end')
    tab1_name_entry.delete(0,'end')
    tab1_phone_entry.delete(0,'end')
    tab1_address_entry.delete(0,'end')
    phone_number = master_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone, maddress FROM mastertab WHERE mphone = (?)",[phone_number])
    # 取出全部資料
    data = cursor.fetchall()
    #辨識有無資料
    if len(data) == 0:
        tk.messagebox.showinfo(title='注意!', message="查無此資料")
    else:
        #讓資料塞入各個欄位
        i=0
        tab1_id_entry.insert(0,data[0][i])
        i=i+1
        tab1_name_entry.insert(0,data[0][i])
        i = i + 1
        tab1_phone_entry.insert(0, "0")
        tab1_phone_entry.insert(1,data[0][i])
        i = i + 1
        tab1_address_entry.insert(0,data[0][i])

def master_delete():
    if master_seacher_phone.get() =="":
        tk.messagebox.showwarning(title='警告!', message="請查詢電話號碼!")
    else:
        phone_number = master_seacher_phone.get()
        cursor.execute("SELECT mid FROM mastertab WHERE '%s' = mastertab.mphone" % (phone_number))
        getmid = cursor.fetchone()[0] #抓mid出來
        sql3 = 'DELETE FROM staytab WHERE mid = ?'
        cursor.execute(sql3, [getmid])  # 刪除住宿資料
        db.commit()
        sql4 = 'DELETE FROM cosmetictab WHERE mid = ?'
        cursor.execute(sql4, [getmid])  # 刪除美容資料
        db.commit()
        sql2 = 'DELETE FROM pettab WHERE mid = ?'#從 pettab 刪 mid
        cursor.execute(sql2, [getmid])  # 刪除寵物資料
        db.commit()
        sql = 'DELETE FROM mastertab WHERE mphone=?'
        cursor.execute(sql, [phone_number])#刪除主人資料
        db.commit()
        tk.messagebox.showinfo("注意!","資料已刪除")
        master_seacher_phone.delete(0, 'end')
        tab1_id_entry.delete(0, 'end')
        tab1_name_entry.delete(0, 'end')
        tab1_phone_entry.delete(0, 'end')
        tab1_address_entry.delete(0, 'end')

def master_update():
    message = []
    phone_number = master_seacher_phone.get()
    customId = tab1_id_entry.get()
    customName = tab1_name_entry.get()
    customPhone = tab1_phone_entry.get()
    customAddress = tab1_address_entry.get()
    idtest = re.search('^[A-Z][12][0-9]{8}$', str(customId))#ID字串匹配
    phonetest = re.search('^09[0-9]{8}$', str(customPhone))#電話字串匹配
    if idtest is None:
        message.append('ID有誤，第一個字母要大寫!!')
    if phonetest is None:
        message.append('電話有誤，請以09作為開頭!!')
    if not message:
        sql = 'UPDATE mastertab SET mid=?, mname=?, mphone=?,maddress=? WHERE mphone=?'
        cursor.execute(sql, [customId,customName,customPhone,customAddress,phone_number])
        db.commit()
        result = "已修改為 身分證字號:" + customId + "  姓名:" + customName + "  電話:" + customPhone + "  地址:" + customAddress
        messagebox.showinfo('修改成功!', str(result))
        master_entry_delete()
    else:
        tk.messagebox.showwarning(title='警告!', message=message)


#飼主新增按鈕
master_add_Btn = tk.Button(tab1, text='新增',width='20',command=master_insert)
master_add_Btn.place(relx=0.2,rely=0.7)

#飼主查詢按鈕
master_seacher_Btn = tk.Button(tab1, text='搜尋',width='10',command=master_seacher)
master_seacher_Btn.place(relx=0.2,rely=0.18)

#飼主刪除按鈕
master_delete_Btn = tk.Button(tab1, text='刪除', width='20',command=master_delete)
master_delete_Btn.place(relx=0.4,rely=0.7)

#飼主修改按鈕
master_update_Btn = tk.Button(tab1, text='修改', width='20',command=master_update)
master_update_Btn.place(relx=0.6,rely=0.7)

###########主人資料




#########寵物資料
##寵物列表選單
listbox = Listbox(tab2,width=15, height=4)
listbox.place(relx=0.02,rely=0.54)


#搜尋飼主電話
title_label = tk.Label(tab2,text='若須 修改、刪除 ，請搜尋飼主電話及寵物名稱',font=('Arial', 10))
title_label.place(relx=0.02,rely=0.1)
#電話輸入
label_tab2_2 = tk.Label(tab2,text='電話')
label_tab2_2.place(relx=0.02,rely=0.14)
pet_seacher_phone = tk.Entry(tab2)
pet_seacher_phone.place(relx=0.02,rely=0.18)
#寵物輸入
# label_tab2_pet = tk.Label(tab2,text='寵物名字')
# label_tab2_pet.place(relx=0.18,rely=0.14)
# pet_seacher_petname = tk.Entry(tab2)
# pet_seacher_petname.place(relx=0.18,rely=0.18)


#寵物標題
mastertitle = tk.Label(tab2,text='寵物資料',font=('Arial', 20))
mastertitle.place(relx=0.02,rely=0.02)
#分隔線
cut_label = ttk.Separator(tab2,orient='horizontal')
cut_label.pack(fill=tk.X,pady=160)

#主人姓名
pet_master = tk.Label(tab2,text='主人姓名')
pet_master.place(relx=0.02,rely=0.3)
pet_master_listbox = Listbox(tab2,height=1,width=20)
pet_master_listbox.place(relx=0.02,rely=0.34)
#主人電話
pet_master_phone = tk.Label(tab2,text='主人電話')
pet_master_phone.place(relx=0.02,rely=0.4)
pet_master_phone_listbox = Listbox(tab2,height=1,width=20)
pet_master_phone_listbox.place(relx=0.02,rely=0.44)




#輸入寵物的 ID、主人姓名、名字、性別、品種、生日、體重、是否結紮、紀錄
pet_label_9 = tk.Label(tab2,text='寵物晶片')
pet_label_9.place(relx=0.2,rely=0.3)
pet_chip_entry = tk.Entry(tab2)
pet_chip_entry.place(relx=0.2,rely=0.34)
pet_label_1 = tk.Label(tab2,text='ID')
pet_label_1.place(relx=0.2,rely=0.4)
pet_id_entry = tk.Entry(tab2)
pet_id_entry.place(relx=0.2,rely=0.44)
pet_label_2 = tk.Label(tab2,text='名字')
pet_label_2.place(relx=0.4,rely=0.4)
pet_name_entry = tk.Entry(tab2)
pet_name_entry.place(relx=0.4,rely=0.44)
pet_label_3 = tk.Label(tab2,text='性別')
pet_label_3.place(relx=0.6,rely=0.4)
pet_label_10 = tk.Label(tab2,text='備註')
pet_label_10.place(relx=0.4,rely=0.27)
pet_remark_entry = tk.Entry(tab2)
pet_remark_entry.place(relx=0.4,rely=0.3,width=550,height=50)
#性別下拉是選單
sex_select = ttk.Combobox(tab2,values=["","男","女"])
sex_select.place(relx=0.6,rely=0.44)
pet_label_4 = tk.Label(tab2, text='品種')
pet_label_4.place(relx=0.8,rely=0.4)
pet_breed_entry = tk.Entry(tab2)
pet_breed_entry.place(relx=0.8,rely=0.44)
###-----------------------------寵物年齡
pet_label_5_1 = tk.Label(tab2, text='年齡:')
pet_label_5_1.place(relx=0.2,rely=0.55)
pet_age_entry_1 = tk.Entry(tab2,width=6)
pet_age_entry_1.place(relx=0.2,rely=0.59)
pet_label_5_2 = tk.Label(tab2, text='年')
pet_label_5_2.place(relx=0.25,rely=0.59)
pet_age_entry_2 = tk.Entry(tab2,width=6)
pet_age_entry_2.place(relx=0.28,rely=0.59)
pet_label_5_3 = tk.Label(tab2, text='月')
pet_label_5_3.place(relx=0.33,rely=0.59)
###-----------------------------寵物年齡
pet_label_6 = tk.Label(tab2,text='體重')
pet_label_6.place(relx=0.4,rely=0.55)
pet_weight_entry = tk.Entry(tab2)
pet_weight_entry.place(relx=0.4,rely=0.59)
pet_label_7 = tk.Label(tab2,text='結紮')
pet_label_7.place(relx=0.6,rely=0.55)
##結紮下拉式選單
ligation_select = ttk.Combobox(tab2,values=["","無","有"])
ligation_select.place(relx=0.6,rely=0.59)
pet_label_8 = tk.Label(tab2,text='就醫紀錄')
pet_label_8.place(relx=0.8,rely=0.55)
pet_record_entry = tk.Entry(tab2)
pet_record_entry.place(relx=0.8,rely=0.59)



###寵物歲數計算
def Pet_Age_to_Database(year,month): #從介面轉到資料庫

    now_month = cursor.execute("SELECT strftime('%m','now')").fetchall()[0][0] ###抓現在月份
    now_year = cursor.execute("SELECT strftime('%Y','now')").fetchall()[0][0] ###抓現在年分
    age_year = int(now_year)-int(year)
    age_month = int(now_month)-int(month)

    if age_month < 0:
        age_year = age_year-1
        age_month = abs(age_month)-2

    return age_year,age_month

def Database_to_Pet_Age(phone,pid): #從資料庫轉到介面
    now_month = cursor.execute("SELECT strftime('%m','now')").fetchall()[0][0]  ###抓現在月份
    now_year = cursor.execute("SELECT strftime('%Y','now')").fetchall()[0][0]  ###抓現在年分
    master_id = cursor.execute("SELECT mid FROM mastertab WHERE mphone = (?)",[phone]).fetchall()[0][0]
    age = cursor.execute("SELECT page FROM pettab WHERE mid = (?) and pid = (?)",[master_id,pid]).fetchall()[0][0]

    if age == '':
        return 0
    else:
        age_year = str(age)[:4]
        age_month = str(age)[4:]
        show_year = int(now_year) - int(age_year)
        show_month = (int(now_month) - int(age_month))%12
        return show_year,show_month


def pet_entry_delete():
    pet_name_entry.config(state="normal")
    pet_name_entry.delete(0,'end')
    pet_weight_entry.delete(0,'end')
    pet_id_entry.delete(0,'end')
    pet_breed_entry.delete(0,'end')
    pet_age_entry_1.delete(0,'end')
    pet_age_entry_2.delete(0, 'end')
    pet_chip_entry.delete(0,'end')
    pet_record_entry.delete(0,'end')
    pet_remark_entry.delete(0, 'end')
    ligation_select.current(0)
    sex_select.current(0)




def pet_seacher():
    #將欄位清空
    pet_entry_delete()
    listbox.delete(0,'end')
    #得手機號碼
    phone_number = pet_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone, maddress FROM mastertab WHERE mphone = (?)",[phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    #辨識有無資料
    if len(masterdata) == 0:
        messagebox.showinfo('注意!', "查無此飼主")
    else:
        # 得到主人ID
        masterid = masterdata[0][0]
        # 得到主人姓名
        mastername = masterdata[0][1]
        # result_master_seacher.configure(text=data)
        cursor.execute(
            "SELECT pid, pname, psex, pbreed, page, pweight, pligatoin, precord, pchip FROM pettab WHERE mid = (?) ",
            [masterid])
        petdata = cursor.fetchall()
        #抓寵物名字出來
        cursor.execute("SELECT pname FROM pettab WHERE mid = (?) ",[masterid])
        #寵物列表的迴圈
        allpetname = cursor.fetchall()
        for item in allpetname:
            listbox.insert(tk.END,item[0])#用item[0]可以擷取二維陣列一筆資料的第一個
        #將主人姓名、電話塞入listbox
        pet_master_listbox.delete(0, 'end')
        pet_master_phone_listbox.delete(0, 'end')
        pet_master_listbox.insert(tk.END, mastername)
        pet_master_phone_listbox.insert(tk.END, phone_number)




def pet_select():#選擇寵物名並丟進輸入欄
    pet_name_entry.config(state="normal")
    decision = listbox.curselection()  # 這是寵物列表的index
    if decision == ():
        messagebox.showerror("注意!", "未選取寵物")
    else:
        decision = listbox.curselection()[0] #這是寵物列表的index
        #拿主人id和寵物名字
        phone_number = pet_seacher_phone.get()
        cursor.execute("SELECT mid FROM mastertab WHERE mphone = (?)", [phone_number])
        masterdata = cursor.fetchall()
        masterid = masterdata[0][0]
        cursor.execute(
            "SELECT pwid, pname, psex, pbreed, page, pweight, pligatoin, precord, pchip FROM pettab WHERE mid = (?) ",
            [masterid])
        petdata = cursor.fetchall()

        pid = cursor.execute("SELECT pid FROM pettab WHERE mid = (?)", [masterid]).fetchall()[decision][0]
        petage = Database_to_Pet_Age(phone_number,pid) #轉換年齡

        ##注入前要先清除
        pet_entry_delete()
        #注入寵物資料
        i = 0
        pet_id_entry.insert(0, petdata[decision][i])
        i = i + 1
        pet_name_entry.insert(0, petdata[decision][i])
        i = i + 2
        pet_breed_entry.insert(0, petdata[decision][i])
        i = i + 2
        pet_weight_entry.insert(0, petdata[decision][i])
        i = i + 2
        pet_record_entry.insert(0, petdata[decision][i])
        i = i + 1
        pet_chip_entry.insert(0, petdata[decision][i])

        # 結紮選擇
        if petdata[decision][6] != "-1":
            if petdata[decision][6] == 0:
                ligation_select.current(1)  ##無
            else:
                ligation_select.current(2)  ##有
        else:
            ligation_select.current(0)
        # 性別選擇
        if petdata[decision][2] != "-1":
            if petdata[decision][2] == "0":
                sex_select.current(1)  ##男
            else:
                sex_select.current(2)  ##女
        else:
            sex_select.current(0)  ##無
        if petage == 0:
            pass
        else:
            petage1 = petage[0]
            petage2 = petage[1]
            pet_age_entry_1.insert(0,petage1)
            pet_age_entry_2.insert(0, petage2)
        pet_name_entry.config(state="disable")




def pet_insert():
    #拿主人ID
    phone_number = pet_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone, maddress FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    flag = 0 #判斷是否跳出警告
    if masterdata == []:
        messagebox.showwarning("注意!", "未做任何查詢")
        flag = 1
    else:
        # 得到主人ID
        masterid = masterdata[0][0]
        # 拿主人ID
        petWid = pet_id_entry.get()
        petName = pet_name_entry.get()
        petSex = sex_select.current()
        petBreed = pet_breed_entry.get()
        petAge1 = pet_age_entry_1.get()
        petAge2 = pet_age_entry_2.get()
        petWeight = pet_weight_entry.get()
        petLigatoin = ligation_select.current()
        petRecord = pet_record_entry.get()
        petChip = pet_chip_entry.get()
        petRemark = pet_remark_entry.get()

        cursor.execute("SELECT pname FROM pettab WHERE mid = (?)", [masterid])
        # 取出全部資料
        allpetname = cursor.fetchall()



        if petName == "" :
            messagebox.showwarning("注意!","寵物名為必填!")
            flag=1
        else:
            for i in allpetname:
                if petName == i[0]:
                    messagebox.showwarning("注意!", "寵物名重複!")
                    flag=1

        if flag == 0:
            if petAge1 != "" and petAge2 != "":
                Age_Year = Pet_Age_to_Database(petAge1,petAge2)[0]
                Age_Month = Pet_Age_to_Database(petAge1,petAge2)[1]
                petAge = str(Age_Year)+str(Age_Month).zfill(2) #zfill 補零 EX: 3+4 --> 03+04
                print(petAge)
            else:
                petAge = ""

            petchip_10_test = None
            petchip_15_test = None
            PetChipComparison(petChip,petchip_10_test,petchip_15_test)  # 晶片碼比對



            if petChip == "":
                # 用現在時間當作id
                cursor.execute("SELECT  julianday('now')")
                jwritetime = cursor.fetchall()
                pid = jwritetime[0][0]
                result = " 寵物名字:" + petName + " 新增成功"
                messagebox.showinfo('新增成功!', str(result))
                sql = 'insert into pettab(pwid, mid, pname, psex, pbreed, page, pweight, pligatoin, precord,pchip,premark,pid)values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                val = (petWid,masterid,petName, petSex, petBreed, petAge, petWeight, petLigatoin, petRecord, petChip, petRemark, pid)
                cursor.execute(sql,val)
                db.commit()
                pet_entry_delete()

            else:
                if petchip_10_test is not None or petchip_15_test is not None: ##晶片
                    messagebox.showerror('失敗!',"寵物晶片應輸入 10 - 15 個數字")
                else:
                    # 用現在時間當作id
                    cursor.execute("SELECT  julianday('now')")
                    jwritetime = cursor.fetchall()
                    pid = jwritetime[0][0]
                    result = " 寵物名字:" + petName + " 新增成功"
                    messagebox.showinfo('新增成功!', str(result))
                    sql = 'insert into pettab(pwid, mid, pname, psex, pbreed, page, pweight, pligatoin, precord,pchip,premark,pid)values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    val = (petWid,masterid,petName, petSex, petBreed, petAge, petWeight, petLigatoin, petRecord, petChip, petRemark, pid)
                    cursor.execute(sql,val)
                    db.commit()
                    pet_entry_delete()




def pet_delete():
    phone_number = pet_seacher_phone.get()
    getpwid = pet_id_entry.get()
    getpname = pet_name_entry.get()
    if getpname == "":
        messagebox.showerror('注意!', "未選取寵物")
    else:
        cursor.execute("SELECT mid FROM mastertab WHERE '%s' = mastertab.mphone" % (phone_number))
        getmid = cursor.fetchone()[0] #抓mid出來
        sql3 = 'DELETE FROM staytab WHERE mid = ?'
        cursor.execute(sql3, [getmid])  # 刪除住宿資料
        db.commit()
        sql4 = 'DELETE FROM cosmetictab WHERE mid = ?'
        cursor.execute(sql4, [getmid])  # 刪除美容資料
        db.commit()
        #從 pettab 刪 mid
        cursor.execute("DELETE FROM pettab WHERE mid = (?) AND pwid = (?) AND pname = (?)",[getmid,getpwid,getpname])  # 刪除寵物資料
        db.commit()
        messagebox.showinfo("成功!","此筆資料已刪除")
        pet_entry_delete()
        listbox.delete(0, 'end')

def pet_update():
    # phone_number = pet_seacher_phone.get()
    # cursor.execute("SELECT mid FROM mastertab WHERE '%s' = mastertab.mphone" % (phone_number))
    # getmid = cursor.fetchone()[0]  # 抓mid出來
    # petWid = pet_id_entry.get()
    # petName = pet_name_entry.get()
    # petSex = sex_select.current()
    # petBreed = pet_breed_entry.get()
    # petAge1 = pet_age_entry_1.get()
    # petAge2 = pet_age_entry_2.get()
    # petWeight = pet_weight_entry.get()
    # petLigatoin = ligation_select.current()
    # petRecord = pet_record_entry.get()
    # petChip = pet_chip_entry.get()
    # petRemark = pet_remark_entry.get()
    # petAge = petAge1.zfill(2) + petAge2.zfill(2)  # zfill 補零 EX: 3+4 --> 03+04
    # sql = 'UPDATE pettab SET pwid=?, pname=?, psex=?, pbreed=?, page=?, pweight=?, pligatoin=?, precord=?, pchip=?, premark=? WHERE mid=? and pname=?'
    # cursor.execute(sql, [petWid,petName,petSex,petBreed,petAge,petWeight,petLigatoin,petRecord,petChip,petRemark,getmid,petName])
    # db.commit()
    # messagebox.showinfo("成功!",petName+" 已修改")


    # 拿主人ID
    phone_number = pet_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone, maddress FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    if len(masterdata) == 0:
        messagebox.showerror('注意!', "未選取寵物")
    else:
        # 得到主人ID
        masterid = masterdata[0][0]# 拿主人ID

        petWid = pet_id_entry.get()
        petName = pet_name_entry.get()
        petSex = sex_select.current()
        petBreed = pet_breed_entry.get()
        petAge1 = pet_age_entry_1.get()
        petAge2 = pet_age_entry_2.get()
        petWeight = pet_weight_entry.get()
        petLigatoin = ligation_select.current()
        petRecord = pet_record_entry.get()
        petChip = pet_chip_entry.get()
        petRemark = pet_remark_entry.get()

        if petName == "":
            messagebox.showwarning("注意!", "寵物名為必填!")
        else:

            if petAge1 != "" and petAge2 != "":
                Age_Year = Pet_Age_to_Database(petAge1, petAge2)[0]
                Age_Month = Pet_Age_to_Database(petAge1, petAge2)[1]
                petAge = str(Age_Year) + str(Age_Month).zfill(2)  # zfill 補零 EX: 3+4 --> 03+04
            else:
                petAge = ""

            petchip_10_test = None
            petchip_15_test = None
            PetChipComparison(petChip, petchip_10_test, petchip_15_test)  # 晶片碼比對

            if petChip == "":

                sql = 'UPDATE pettab SET pwid=?, pname=?, psex=?, pbreed=?, page=?, pweight=?, pligatoin=?, precord=?, pchip=?, premark=? WHERE mid=? and pname=?'
                cursor.execute(sql, [petWid, petName, petSex, petBreed, petAge, petWeight, petLigatoin, petRecord, petChip,
                                     petRemark, masterid, petName])
                db.commit()
                print(petAge)
                messagebox.showinfo("成功!", petName + " 已修改")
                pet_entry_delete()
            else:
                if petchip_10_test is not None or petchip_15_test is not None: ##晶片
                    sql = 'UPDATE pettab SET pwid=?, pname=?, psex=?, pbreed=?, page=?, pweight=?, pligatoin=?, precord=?, pchip=?, premark=? WHERE mid=? and pname=?'
                    cursor.execute(sql,
                                   [petWid, petName, petSex, petBreed, petAge, petWeight, petLigatoin, petRecord, petChip,
                                    petRemark, masterid, petName])
                    db.commit()
                    messagebox.showinfo("成功!", petName + " 已修改")
                    pet_entry_delete()
                else:
                    messagebox.showerror('失敗!', "寵物晶片應輸入 10 - 15 個數字")


#寵物>飼主查詢按鈕
pet_seacher_Btn = tk.Button(tab2, text='搜尋',width='10',command=pet_seacher)
pet_seacher_Btn.place(relx=0.2,rely=0.18)

#寵物>新增按鈕
pet_add_Btn = tk.Button(tab2, text='新增',width='20',command=pet_insert)
pet_add_Btn.place(relx=0.2,rely=0.7)

#寵物>刪除按鈕
pet_delete_Btn = tk.Button(tab2, text='刪除', width='20',command=pet_delete)
pet_delete_Btn.place(relx=0.4,rely=0.7)

#寵物>修改按鈕
pet_update_Btn = tk.Button(tab2, text='修改', width='20',command=pet_update)
pet_update_Btn.place(relx=0.6,rely=0.7)

#寵物>列表按鈕
select_pet_Btn = tk.Button(tab2, text='確定',width='10', command=pet_select)
select_pet_Btn.place(relx=0.02,rely=0.65)

#寵物>重整按鈕
reorg_pet_Btn = tk.Button(tab2, text='重整',width='10', command=pet_entry_delete)
reorg_pet_Btn.place(relx=0.8,rely=0.7)





frame1 = tk.Frame(tab3)



##########住宿資料
#搜尋飼主電話
title_label = tk.Label(tab3,text='若須 修改、刪除 ，請搜尋飼主電話',font=('Arial', 10))
title_label.place(relx=0.02,rely=0.1)
label_tab3_2 = tk.Label(tab3,text='電話')
label_tab3_2.place(relx=0.02,rely=0.14)
#電話輸入
stay_seacher_phone = tk.Entry(tab3)
stay_seacher_phone.place(relx=0.02,rely=0.18)

#寵物標題
mastertitle = tk.Label(tab3,text='住宿資料',font=('Arial', 20))
mastertitle.place(relx=0.02,rely=0.02)
#分隔線
cut_label = ttk.Separator(tab3,orient='horizontal')
cut_label.pack(fill=tk.X,pady=170)

#主人姓名
stay_master = tk.Label(tab3,text='主人姓名')
stay_master.place(relx=0.02,rely=0.3)
stay_master_listbox = Listbox(tab3,height=1,width=20)
stay_master_listbox.place(relx=0.02,rely=0.34)
#主人電話
stay_master_phone = tk.Label(tab3,text='主人電話')
stay_master_phone.place(relx=0.02,rely=0.4)
stay_master_phone_listbox = Listbox(tab3,height=1,width=20)
stay_master_phone_listbox.place(relx=0.02,rely=0.44)

##住宿寵物列表選單
stay_listbox = Listbox(tab3,width=15, height=4)
stay_listbox.place(relx=0.02,rely=0.54)

#住宿輸入欄位
stay_label_1 = tk.Label(tab3,text='住宿編號')
stay_label_1.place(relx=0.2,rely=0.4)
stay_no_entry = tk.Entry(tab3)
stay_no_entry.place(relx=0.2,rely=0.44)
stay_label_2 = tk.Label(tab3,text='入住時間')
stay_label_2.place(relx=0.4,rely=0.4)
stay_intime_entry = tk.Entry(tab3)
stay_intime_entry.place(relx=0.4,rely=0.44)
stay_label_3 = tk.Label(tab3,text='退房時間')
stay_label_3.place(relx=0.6,rely=0.4)
stay_outtime_entry = tk.Entry(tab3)
stay_outtime_entry.place(relx=0.6,rely=0.44)
stay_label_4 = tk.Label(tab3, text='記事')
stay_label_4.place(relx=0.2,rely=0.5)
stay_record_entry = tk.Text(tab3,width=50,height=10)
stay_record_entry.place(relx=0.2,rely=0.54)
stay_label_5 = tk.Label(tab3,text='付款')
stay_label_5.place(relx=0.8,rely=0.4)
stay_pay_entry = tk.Entry(tab3)
stay_pay_entry.place(relx=0.8,rely=0.44)


def stay_seacher():
    stay_listbox.delete(0,'end')
    # 得手機號碼
    phone_number = stay_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    # 辨識有無資料
    if len(masterdata) == 0:
        messagebox.showerror("注意!","查無此飼主")
    else:
        # 得到主人ID
        masterid = masterdata[0][0]
        mastername = masterdata[0][1]
        # 抓寵物名字出來
        cursor.execute("SELECT pname FROM pettab WHERE mid = (?) ", [masterid])
        # 寵物列表的迴圈
        allpetname = cursor.fetchall()
        for item in allpetname:
            stay_listbox.insert(tk.END, item[0])  # 用item[0]可以擷取二維陣列一筆資料的第一個
        # print(str(listbox.curselection()))
        # 將主人姓名、電話塞入listbox
        stay_master_listbox.delete(0, 'end')
        stay_master_phone_listbox.delete(0, 'end')
        stay_master_listbox.insert(tk.END, mastername)
        stay_master_phone_listbox.insert(tk.END, phone_number)




        # #得到寵物名字
        # cursor.execute("SELECT  pname FROM pettab WHERE mid = (?) ",[masterid])
        # petdate = cursor.fetchall()
        # if len(petdate) != 0:
        #     petname = petdate[0][0]
        #     #取得住宿資料
        #     cursor.execute("SELECT mid, pid, sNo, intime, outtime, spay,snote FROM staytab WHERE mid = (?)", [masterid])
        #     # 取出全部資料
        #     staydata = cursor.fetchall()
        #     result_stay.configure(text=staydata)
        #     if len(staydata)!=0:
        #         # 讓資料塞入各個欄位
        #         i = 2
        #         stay_no_entry.insert(0, staydata[0][i])
        #         i=i+1
        #         stay_intime_entry.insert(0, staydata[0][i])
        #         i=i+1
        #         stay_outtime_entry.insert(0, staydata[0][i])
        #         i=i+1
        #         stay_pay_entry.insert(0, staydata[0][i])
        #         i=i+1
        #         stay_record_entry.insert(1.0, staydata[0][i])
        # else:
        #     result_stay.configure(text="此人無寵物")



def stay_select():#選擇寵物名並丟進輸入欄
    decision = stay_listbox.curselection()  # 這是寵物列表的index
    if decision == ():
        messagebox.showerror("注意!", "未選取寵物")
    else:
        decision = stay_listbox.curselection()[0] #這是寵物列表的index
        #拿主人id和寵物名字
        phone_number = stay_seacher_phone.get()
        #找出主人ID
        cursor.execute("SELECT mid FROM mastertab WHERE mphone = (?)", [phone_number])
        masterdata = cursor.fetchall()
        masterid = masterdata[0][0]
        #找出寵物ID
        cursor.execute("SELECT pid FROM pettab WHERE mid = (?)",[masterid])
        petdata = cursor.fetchall()
        #找是主人的第幾個寵物
        petid = petdata[decision][0]
        #跨表格的SELECT 取出主人和寵物名字及住宿資料
        cursor.execute("SELECT mname, pname, sNo, intime, outtime, spay,snote FROM mastertab,pettab,staytab WHERE mastertab.mid = (?) AND pettab.pid = (?) AND staytab.pid = (?)", [masterid,petid,petid])
        # 取出全部寵物住宿資料
        staydata = cursor.fetchall()
        if len(staydata) == 0:
            ##要先清除
            treeviewtest.delete(*treeviewtest.get_children())  # 用來將表格清除
            stay_no_entry.delete(0, 'end')
            stay_intime_entry.delete(0, 'end')
            stay_outtime_entry.delete(0, 'end')
            stay_record_entry.delete(1.0, 'end')
            stay_pay_entry.delete(0, 'end')
            messagebox.showerror("注意!","此寵物尚未有住宿資料")
        else:
            ##注入前要先清除
            treeviewtest.delete(*treeviewtest.get_children())#用來將表格清除
            stay_no_entry.delete(0, 'end')
            stay_intime_entry.delete(0, 'end')
            stay_outtime_entry.delete(0, 'end')
            stay_record_entry.delete(1.0, 'end')
            stay_pay_entry.delete(0, 'end')
            if len(staydata) == 0:
                messagebox.showinfo("注意!","尚無資料，請進行輸入")
            else:
                for data in staydata:
                    treeviewtest.insert('', 0, values=data)  # 添加數據到末尾


def stay_insert():
    # 拿主人ID
    phone_number = stay_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    # 得到主人ID
    masterid = masterdata[0][0]
    intime = stay_intime_entry.get()
    outtime = stay_outtime_entry.get()
    pay = stay_pay_entry.get()

    #寫入的時間
    cursor.execute("SELECT datetime(CURRENT_TIMESTAMP,'localtime')")
    writetime = cursor.fetchall()
    swritetime = str(writetime[0][0])
    #正規表達式
    intimetest = re.search('^[0-9]{4}-(0?[1-9]|1[0-2])-((0?[1-9])|((1|2)[0-9])|30|31)$', str(intime))  # ID字串匹配
    outtimetest = re.search('^[0-9]{4}-(0?[1-9]|1[0-2])-((0?[1-9])|((1|2)[0-9])|30|31)$', str(outtime))  # 電話字串匹配
    if intimetest is None or (outtime != "" and outtimetest is None):
        messagebox.showwarning("注意!","日期請依照 20XX-XX-XX 填寫!")
    elif pay == "" or pay == "0":
        messagebox.showwarning("注意!", "金額不可為空或為零")
    else:
        decision = stay_listbox.curselection()  # 這是寵物列表的index
        if decision == ():
            messagebox.showerror("注意!", "未選取寵物")
        else:
            decision = decision[0]
            #先跳出詢問視窗，顯示「新增後內容即無法修改，請問要新增嗎?」
            result = messagebox.askokcancel("注意!","新增後內容即無法修改，請問要新增嗎?")
            if result == True:
                #寵物ID
                cursor.execute("SELECT  pid FROM pettab WHERE mid = (?) ", [masterid])
                petdate = cursor.fetchall()
                petid = petdate[decision][0]
                # 拿主人ID
                stayNo = stay_no_entry.get()
                stayintime = stay_intime_entry.get()
                stayouttime = stay_outtime_entry.get()
                staypay = stay_pay_entry.get()
                staynote = stay_record_entry.get(1.0, tk.END+"-1c")
                sql = 'insert into staytab(mid, pid, sNo, intime, outtime, spay, snote, swritetime)values(?, ?, ?, ?, ?, ?, ?,?)'
                val = (masterid,petid,stayNo,stayintime,stayouttime,staypay,staynote,swritetime)
                cursor.execute(sql,val)
                db.commit()
                messagebox.showinfo("成功!","新增成功!")
                stay_no_entry.delete(0, 'end')
                stay_intime_entry.delete(0, 'end')
                stay_outtime_entry.delete(0, 'end')
                stay_record_entry.delete(1.0, 'end')
                stay_pay_entry.delete(0, 'end')




##住宿表格呈現
columns = ("主人","寵物","住宿編號","入住時間","退房時間","付款")
treeviewtest = ttk.Treeview(tab3,height=5,show="headings",column=columns)

treeviewtest.column("主人",width=100,anchor='center')
treeviewtest.column("寵物",width=100,anchor='center')
treeviewtest.column("住宿編號",width=100,anchor='center')
treeviewtest.column("入住時間",width=100,anchor='center')
treeviewtest.column("退房時間",width=100,anchor='center')
treeviewtest.column("付款",width=100,anchor='center')

treeviewtest.heading("主人",text="主人")
treeviewtest.heading("寵物",text="寵物")
treeviewtest.heading("住宿編號",text="住宿編號")
treeviewtest.heading("入住時間",text="入住時間")
treeviewtest.heading("退房時間",text="退房時間")
treeviewtest.heading("付款",text="付款")
treeviewtest.place(relx=0.3,rely=0.02)



# yscrollbar = tk.Scrollbar(treeviewtest,orient="vertical", command=treeviewtest.yview)


# tree.pack()

# yscrollbar.config(command=treeviewtest.yview)
#
# treeviewtest.configure(yscrollcommand=yscrollbar.set)

# treeviewtest.place(relx=0.3,rely=0.02)
# yscrollbar.place(x=580,y=50,anchor='e')



#飼主查詢按鈕
stay_seacher_Btn = tk.Button(tab3, text='搜尋',width='10',command=stay_seacher)
stay_seacher_Btn.place(relx=0.2,rely=0.18)
#住宿>新增按鈕
stay_add_Btn = tk.Button(tab3, text='新增',width='20',command=stay_insert)
stay_add_Btn.place(relx=0.6,rely=0.5)
#住宿>列表確定按鈕
select_pet_Btn = tk.Button(tab3, text='確定',width='10', command=stay_select)
select_pet_Btn.place(relx=0.02,rely=0.65)
##########住宿資料



##########美容資料
#搜尋飼主電話
title_label = tk.Label(tab4,text='若須 修改、刪除 ，請搜尋飼主電話',font=('Arial', 10))
title_label.place(relx=0.02,rely=0.1)
label_tab4_2 = tk.Label(tab4,text='電話')
label_tab4_2.place(relx=0.02,rely=0.14)
#電話輸入
c_seacher_phone = tk.Entry(tab4)
c_seacher_phone.place(relx=0.02,rely=0.18)

#美容標題
ctitle = tk.Label(tab4,text='美容資料',font=('Arial', 20))
ctitle.place(relx=0.02,rely=0.02)
#分隔線
cut_label = ttk.Separator(tab4,orient='horizontal')
cut_label.pack(fill=tk.X,pady=170)

#主人姓名
c_master = tk.Label(tab4,text='主人姓名')
c_master.place(relx=0.02,rely=0.3)
c_master_listbox = Listbox(tab4,height=1,width=20)
c_master_listbox.place(relx=0.02,rely=0.34)
#主人電話
c_master_phone = tk.Label(tab4,text='主人電話')
c_master_phone.place(relx=0.02,rely=0.4)
c_master_phone_listbox = Listbox(tab4,height=1,width=20)
c_master_phone_listbox.place(relx=0.02,rely=0.44)
#寵物名稱
c_pet_name = tk.Label(tab4,text='寵物')
c_pet_name.place(relx=0.02,rely=0.5)
c_pet_name_listbox = Listbox(tab4,height=4,width=15)
c_pet_name_listbox.place(relx=0.02,rely=0.54)


##日期
c_label_1 = tk.Label(tab4,text='日期')
c_label_1.place(relx=0.2,rely=0.3)
c_date_entry = tk.Entry(tab4)
c_date_entry.place(relx=0.2,rely=0.34)

c_label_2 = tk.Label(tab4,text='毛孩狀況')
c_label_2.place(relx=0.4,rely=0.3)

c_label_3 = tk.Label(tab4,text='金額')
c_label_3.place(relx=0.2,rely=0.4)
c_pay_entry = tk.Entry(tab4)
c_pay_entry.place(relx=0.2,rely=0.44)




def cos_seacher():
    c_pet_name_listbox.delete(0,'end')
    # 得手機號碼
    phone_number = c_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()
    # 辨識有無資料
    if len(masterdata) == 0:
        messagebox.showerror("注意!","查無此飼主")
    else:
        # 得到主人ID
        masterid = masterdata[0][0]
        mastername = masterdata[0][1]
        # 抓寵物名字出來
        cursor.execute("SELECT pname FROM pettab WHERE mid = (?) ", [masterid])
        # 寵物列表的迴圈
        allpetname = cursor.fetchall()
        for item in allpetname:
            c_pet_name_listbox.insert(tk.END, item[0])  # 用item[0]可以擷取二維陣列一筆資料的第一個
        # 將主人姓名、電話塞入listbox
        c_master_listbox.delete(0, 'end')
        c_master_phone_listbox.delete(0, 'end')
        c_master_listbox.insert(tk.END, mastername)
        c_master_phone_listbox.insert(tk.END, phone_number)




#設定複選變數，以方便取得其中的boolen值
check1 = tk.IntVar()
check2 = tk.IntVar()
check3 = tk.IntVar()
check4 = tk.IntVar()
check5 = tk.IntVar()
check6 = tk.IntVar()
check7 = tk.IntVar()
check8 = tk.IntVar()


#複選紐
check_btn1 = tk.Checkbutton(tab4, text='黴菌',variable=check1,onvalue=1, offvalue=0)  # 放入第一個按鈕
check_btn1.place(relx=0.4,rely=0.34)
check_btn2 = tk.Checkbutton(tab4, text='紅疹',variable=check2,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn2.place(relx=0.4,rely=0.38)
check_btn3 = tk.Checkbutton(tab4, text='內耳髒',variable=check3,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn3.place(relx=0.4,rely=0.42)
check_btn4 = tk.Checkbutton(tab4, text='耳炎',variable=check4,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn4.place(relx=0.4,rely=0.46)
check_btn5 = tk.Checkbutton(tab4, text='跳蚤',variable=check5,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn5.place(relx=0.4,rely=0.50)
check_btn6 = tk.Checkbutton(tab4, text='壁蝨',variable=check6,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn6.place(relx=0.4,rely=0.54)
check_btn7 = tk.Checkbutton(tab4, text='指甲長',variable=check7,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn7.place(relx=0.4,rely=0.58)
check_btn8 = tk.Checkbutton(tab4, text='其他',variable=check8,onvalue=1, offvalue=0) # 放入第二個按鈕
check_btn8.place(relx=0.4,rely=0.62)

#其他的輸入框
c_other_entry = tk.Entry(tab4)
c_other_entry.place(relx=0.455,rely=0.625)
#改善與建議
c_label_4 = tk.Label(tab4,text='改善方式與建議')
c_label_4.place(relx=0.6,rely=0.3)
c_suggest_entry = tk.Text(tab4,height=10,width=40)
c_suggest_entry.place(relx=0.6,rely=0.34)

##美容表格呈現
cos_columns = ("日期","毛孩情況","改善與建議","金額")
cos_treeview = ttk.Treeview(tab4,height=5,show="headings",column=cos_columns)

###########################################卷軸
# yscrollbar=tk.Scrollbar(tab4)  #卷軸
# yscrollbar.pack(side="right",fill='y')
# yscrollbar.config(command=cos_treeview.yview)
# cos_treeview.configure(yscrollcommand=yscrollbar.set)

###美容的表格
cos_treeview.column("日期",width=100,anchor='center')
cos_treeview.column("毛孩情況",width=200,anchor='center')
cos_treeview.column("改善與建議",width=200,anchor='center')
cos_treeview.column("金額",width=100,anchor='center')

cos_treeview.heading("日期",text="日期")
cos_treeview.heading("毛孩情況",text="毛孩情況")
cos_treeview.heading("改善與建議",text="改善與建議")
cos_treeview.heading("金額",text="金額")
cos_treeview.place(relx=0.3,rely=0.02)



def cos_insert():
    # 拿主人ID
    phone_number = c_seacher_phone.get()
    cursor.execute("SELECT mid, mname, mphone FROM mastertab WHERE mphone = (?)", [phone_number])
    # 取出全部資料
    masterdata = cursor.fetchall()

    # 寫入的時間
    cursor.execute("SELECT datetime(CURRENT_TIMESTAMP,'localtime')")
    writetime = cursor.fetchall()
    cwritetime = str(writetime[0][0])


    # 得到主人ID
    masterid = masterdata[0][0]
    decision = c_pet_name_listbox.curselection()  # 這是寵物列表的index
    pay_zero = c_pay_entry.get()
    date = c_date_entry.get()

    #date_test = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', str(date))  # ID字串匹配
    date_test = re.search('^[0-9]{4}-(0?[1-9]|1[0-2])-((0?[1-9])|((1|2)[0-9])|30|31)$', str(date)) # 完整的日期字串匹配
    if decision == ():
        messagebox.showerror("注意!","未選取寵物")
    elif date_test is None:
        messagebox.showerror("注意!", "日期請依照 20XX-XX-XX 格式填寫")
    elif pay_zero == '' or int(pay_zero) <=0:
        messagebox.showerror("注意!", "金額不可為空或為零")
    else:
        decision = decision[0]
        # 先跳出詢問視窗，顯示「新增後內容即無法修改，請問要新增嗎?」
        result = messagebox.askokcancel("注意!", "新增後內容即無法修改，請問要新增嗎?")
        if result == True:
            # 寵物ID
            cursor.execute("SELECT  pid FROM pettab WHERE mid = (?) ", [masterid])
            petdate = cursor.fetchall()
            petid = petdate[decision][0]
            selection = [] #selection 以list形態代表毛孩狀態
            #確定前先清除
            selection.append(check1.get())
            selection.append(check2.get())
            selection.append(check3.get())
            selection.append(check4.get())
            selection.append(check5.get())
            selection.append(check6.get())
            selection.append(check7.get())
            selection.append(check8.get())
            #藉由判斷 "其他"是否被勾選 和 其他的欄位是否有內容 來決定要不要增加進 selection
            if check8.get() == 1 and c_other_entry.get() != "":
                other = c_other_entry.get()
                selection.append(str(other))
            else:
                check8.set(0)
                selection[7] = 0
            date = c_date_entry.get()
            date_test = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', str(date))  # ID字串匹配
            suggest = c_suggest_entry.get(1.0, tk.END+"-1c")
            pay = c_pay_entry.get()
            selection = "".join(map(str, selection))#將list轉成字串
            text = cursor.execute('insert into cosmetictab(mid, pid,  csuggest, cdate, csittuation, cpay, cwritetime)values(?, ?, ?, ?,?, ?,?)', [masterid, petid, suggest, date, selection,pay,cwritetime])
            db.commit()
            messagebox.showinfo("成功!", "新增成功!")
            #清除欄位資料
            c_date_entry.delete(0, 'end')
            c_suggest_entry.delete(1.0, 'end')
            c_pay_entry.delete(0, 'end')
            check_btn1.deselect()
            check_btn2.deselect()
            check_btn3.deselect()
            check_btn4.deselect()
            check_btn5.deselect()
            check_btn6.deselect()
            check_btn7.deselect()
            check_btn8.deselect()





def cos_select():#選擇寵物名並丟進輸入欄
    decision = c_pet_name_listbox.curselection()  # 這是寵物列表的index
    if decision == ():
        messagebox.showerror("注意!","未選取寵物")
    else:
        #清除欄位資料
        c_date_entry.delete(0, 'end')
        c_suggest_entry.delete(1.0, 'end')
        c_pay_entry.delete(0, 'end')
        check_btn1.deselect()
        check_btn2.deselect()
        check_btn3.deselect()
        check_btn4.deselect()
        check_btn5.deselect()
        check_btn6.deselect()
        check_btn7.deselect()
        check_btn8.deselect()
        decision = c_pet_name_listbox.curselection()[0] #這是寵物列表的index
        #拿主人id和寵物名字
        phone_number = c_seacher_phone.get()
        #找出主人ID
        cursor.execute("SELECT mid FROM mastertab WHERE mphone = (?)", [phone_number])
        masterdata = cursor.fetchall()
        masterid = masterdata[0][0]
        #找出寵物ID
        cursor.execute("SELECT pid FROM pettab WHERE mid = (?)",[masterid])
        petdata = cursor.fetchall()
        #找是主人的第幾個寵物
        petid = petdata[decision][0]
        #跨表格的SELECT 取出主人和寵物名字及住宿資料
        cursor.execute("SELECT mname, pname, csittuation, csuggest, cdate , cpay FROM mastertab,pettab,cosmetictab WHERE mastertab.mid = (?) AND pettab.pid = (?) AND cosmetictab.pid = (?)", [masterid,petid,petid])
        # 取出全部寵物住宿資料
        cosdata = cursor.fetchall()
        #當無此寵物的資料
        if len(cosdata) == 0:
            ##要先清除表格資料
            x = cos_treeview.get_children()
            for item in x:
                cos_treeview.delete(item)
            #treeviewtest.delete(*treeviewtest.get_children())  # 用來將表格清除
            c_date_entry.delete(0, 'end')
            c_suggest_entry.delete(1.0, 'end')
            messagebox.showerror("注意!","此寵物尚未有住宿資料")
        else:
            ##注入前要先清除
            ##要先清除表格資料
            x = cos_treeview.get_children()
            for item in x:
                cos_treeview.delete(item)
            #cos_treeview.delete(*treeviewtest.get_children())#用來將表格清除
            c_date_entry.delete(0, 'end')
            c_suggest_entry.delete(1.0, 'end')
            if len(cosdata) == 0:
                messagebox.showinfo("注意!","尚無資料，請進行輸入")
            else:
                final_sittuation_result = []
                #可以顯示病症
                for j in range(len(cosdata)):
                    final_sittuation_result = []
                    date = cosdata[j][4]
                    suggest = cosdata[j][3]
                    pay = cosdata[j][5]
                    final_sittuation_result.append(date)
                    string_sittuation = cosdata[j][2]
                    count = 0
                    final_print = []
                    for i in string_sittuation:#處理毛孩情況的迴圈
                        if count ==0 and i == "1":
                            final_print.append("黴菌")
                        if count ==1 and i == "1":
                            final_print.append("紅疹")
                        if count ==2 and i == "1":
                            final_print.append("內耳髒")
                        if count ==3 and i == "1":
                            final_print.append("耳炎")
                        if count ==4 and i == "1":
                            final_print.append("跳蚤")
                        if count ==5 and i == "1":
                            final_print.append("壁蝨")
                        if count ==6 and i == "1":
                            final_print.append("指甲長")
                        if count ==7 and i == "1":
                            final_print.append(string_sittuation[8:])
                        count = count+1
                    # cos_treeview.insert('',1,values=final_print)
                    # for data in cosdata:
                    #     cos_treeview.insert('', 0, values=data)  # 添加數據到末尾
                    final_print = ",".join(map(str, final_print))##轉字串+多逗號，是毛孩情況的最終結果
                    final_sittuation_result.append(final_print)
                    final_sittuation_result.append(suggest)
                    final_sittuation_result.append(pay)
                    cos_treeview.insert('', 0, values=final_sittuation_result)






#美容>查詢按鈕
cos_seacher_Btn = tk.Button(tab4, text='搜尋',width='10',command=cos_seacher)
cos_seacher_Btn.place(relx=0.2,rely=0.18)

#美容>確定鍵
cos_check_Btn = tk.Button(tab4, text = '新增資料', width='10', command=cos_insert)
cos_check_Btn.place(relx=0.4,rely=0.67)

#美容>寵物確定按鈕
select_pet_Btn = tk.Button(tab4, text='確定',width='10',command=cos_select)
select_pet_Btn.place(relx=0.02,rely=0.65)


######匯出報表

##日期的正規表達式
day_Expression = '^[0-9]{4}-([0]{1}[0-9]{1}|[1]{1}[0-2]{1})-([0-2]{1}[0-9]{1}|[3]{1}[0-1]{1})$'
##月份的正規表達式
month_Expression = '^[0-9]{4}-([0]{1}[0-9]{1}|[1]{1}[0-2]{1})$'

report_out_txt = tk.Label(tab5,text='請輸入想列印之報表日期',font=('microsoft yahei', 10,'bold'))
#report_out_txt.place(relx=0.4,rely=0.1)
report_out_txt.pack(side="top",ipady=20)
report_out_txt_entry = tk.Entry(tab5)
#report_out_txt_entry.place(relx=0.4,rely=0.14)
report_out_txt_entry.pack(side="top")
report_notice_txt = tk.Label(tab5,text='請使用「20XX-MM-DD」或「20XX-MM」的格式輸入',font=('microsoft yahei',9,'bold'))
report_notice_txt.place(relx=0.02,rely=0.02)
report_notice_txt_1 = tk.Label(tab5,text='若點選【日報表】，將產出輸入日期當日之報表\n若點選【月報表】，將產出輸入日期當月之報表')
report_notice_txt_1.place(relx=0.02,rely=0.05)
finish_label = tk.Label(tab5, text = '',font=('microsoft yahei',9,'bold'))
#report_notice_txt.pack(side="top",ipady=20)

# report_out_month_txt = tk.Label(tab5,text='請輸入想列印之報表月份',font=('microsoft yahei', 10,'bold'))
# #report_out_txt.place(relx=0.4,rely=0.1)
# report_out_month_txt.pack(side="top",ipady=20)
# report_out_month_txt_entry = tk.Entry(tab5)
# #report_out_txt_entry.place(relx=0.4,rely=0.14)
# report_out_month_txt_entry.pack(side="top")


def Daily_report_out():
    location_f = open('location.txt', 'r')
    for line in location_f:
        text.append(line)
    des_path = text[2]

    date = report_out_txt_entry.get()

    if re.match(day_Expression,date) is not None:
        #資料部分
        date_rec_cos = cursor.execute('SELECT mid, pid, cpay FROM cosmetictab WHERE cdate = (?)', [date])
        date_rec_cos_tuple = tuple(date_rec_cos.fetchall())
        date_rec_stay = cursor.execute("SELECT mid, pid, spay FROM staytab WHERE intime = (?)", [date])
        date_rec_stay_tuple = tuple(date_rec_stay.fetchall())

        all_list = []
        expand_list = []
        total_a_day = 0
        cost = 0
        no_data_flag = 0
        if date_rec_cos_tuple != ():
            for mid, pid, pay in date_rec_cos_tuple:
                expand_list = []
                # print(mid,pid,pay)
                master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                master_phone = (cursor.execute('SELECT mphone FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
                expand_list = (master_name[0],'0'+str(master_phone[0]), pet_id[0],date,'美容', pay)
                total_a_day = total_a_day + pay
                # print(expand_list)
                cost = cost + pay
                all_list.append(expand_list)
        else:
            no_data_flag += 1  # 如果沒資料，flag +1

        if date_rec_stay_tuple != ():
            for mid, pid, pay in date_rec_stay_tuple:
                expand_list = []
                master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                master_phone = (cursor.execute('SELECT mphone FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
                expand_list = (master_name[0], '0'+str(master_phone[0]), pet_id[0], date, '住宿', pay)
                total_a_day = total_a_day + pay
                all_list.append(expand_list)
                cost = cost + pay
        else:
            no_data_flag += 1  # 如果沒資料，flag +1

        if no_data_flag == 2:
            messagebox.showinfo("注意!", "此日無資料")
        else:
            all_tuple = list(all_list)
            all_tuple_df = pd.DataFrame(all_tuple)
            all_tuple_df.columns = ['主人', '電話', '寵物', '日期', '服務', '金額']  # 建立標頭
            all_tuple_df.index = all_tuple_df.index + 1
            all_tuple_df.loc[len(all_tuple_df.index)+1] = ["","","","","總金額:",cost]

            #print(all_tuple_df)

            ###寫入excel
            # wb.save("test.xlsx")
            all_tuple_df.to_excel(des_path+'/'+f"{date}.xlsx")
            finish_label['text'] = '已產生 '+str(date)+' 的日報表。'
    else:
        messagebox.showinfo("注意!", "請照 20XX-MM-DD 格式輸入來產生 日報表")


def Monthly_report():

    location_f = open('location.txt', 'r')
    for line in location_f:
        text.append(line)
    des_path = text[2]

    date = report_out_txt_entry.get()

    if re.match(month_Expression, date) is not None:
        # 資料部分
        cursor.execute('SELECT cdate FROM cosmetictab WHERE cdate REGEXP ?', [date])
        date_rec_cos = cursor.execute('SELECT mid, pid, cpay, cdate FROM cosmetictab WHERE cdate REGEXP (?)', [date])
        date_rec_cos_tuple = tuple(date_rec_cos.fetchall())
        date_rec_stay = cursor.execute("SELECT mid, pid,spay, intime FROM staytab WHERE intime REGEXP (?)", [date])
        date_rec_stay_tuple = tuple(date_rec_stay.fetchall())
        # print(date_rec_cos_tuple)
        # print(date_rec_stay_tuple)
        all_list = []
        expand_list = []
        total_a_day = 0
        cost = 0
        no_data_flag = 0
        if date_rec_cos_tuple != ():
            for mid, pid, pay, time in date_rec_cos_tuple:
                expand_list = []
                # print(mid,pid,pay)
                master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                master_phone = (cursor.execute('SELECT mphone FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
                expand_list = (master_name[0], '0'+str(master_phone[0]), pet_id[0], time, '美容', pay)
                total_a_day = total_a_day + pay
                # print(expand_list)
                cost = cost + pay
                all_list.append(expand_list)
        else:
            no_data_flag += 1 #如果沒資料，flag +1

        if date_rec_stay_tuple != ():
            for mid, pid, pay, time in date_rec_stay_tuple:
                expand_list = []
                master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                master_phone = (cursor.execute('SELECT mphone FROM mastertab WHERE mid = (?)', [mid])).fetchone()
                pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
                expand_list = (master_name[0], '0'+str(master_phone[0]), pet_id[0], time, '住宿', pay)
                total_a_day = total_a_day + pay
                cost = cost + pay
                all_list.append(expand_list)
        else:
            no_data_flag += 1 #如果沒資料，flag +1


        if no_data_flag == 2:
            messagebox.showinfo("注意!", "此月份無資料")
        else:
            all_tuple = list(all_list)
            all_tuple_df = pd.DataFrame(all_tuple)
            final = all_tuple_df.sort_values(3) #按照日期排序
            final.columns=['主人','電話','寵物','日期','服務','金額'] #建立標頭
            final.reset_index(drop=True,inplace=True) #讓 index 重新排列,drop 將索引值還原成整數列 or 丟棄, inplace 重製原數據
            final.index = final.index + 1
            final.loc[len(all_tuple_df.index)+1] = ["","","","","總金額:",cost]
            # print(final)


            ###寫入excel
            final.to_excel(des_path+'/'+f"{date}.xlsx")
            finish_label['text'] = '已產生 ' + str(date) + ' 的月報表。'
    else:
        messagebox.showinfo("注意!", "請照 20XX-MM 格式輸入來產生 月報表")




###主人名/寵物名/住宿金額/美容金額/總金額?

produce_day_report_Btn = tk.Button(tab5, text='產生 日報表',width='10',command=Daily_report_out,bg='orange')
# select_pet_Btn.place(relx=0.43,rely=0.18)
produce_day_report_Btn.pack(side="top",pady=10)
produce_month_report_Btn = tk.Button(tab5, text='產生 月報表',width='10',command=Monthly_report,bg='yellow')
# select_pet_Btn.place(relx=0.43,rely=0.18)
produce_month_report_Btn.pack(side="top")

finish_label.pack(side="top",pady=10)




######匯出報表




######總資料

#抓 主人名字 寵物名 美容OR住宿 施作/住宿日期 消費金額



##表格呈現


columns2 = ("1","2","3","4","5","6")
treeview_data = ttk.Treeview(tab6,height=25,show="headings",column=columns2)



treeview_data.column("1",width=150,anchor='center')
treeview_data.column("2",width=150,anchor='center')
treeview_data.column("3",width=100,anchor='center')
treeview_data.column("4",width=150,anchor='center')
treeview_data.column("5",width=100,anchor='center')
treeview_data.column("6",width=150,anchor='center')

treeview_data.heading("1",text="主人")
treeview_data.heading("2",text="寵物")
treeview_data.heading("3",text="日期")
treeview_data.heading("4",text="住宿or美容")
treeview_data.heading("5",text="消費金額")
treeview_data.heading("6",text="編輯時間")
treeview_data.place(relx=0.2,rely=0.025)

def show_all_data():
    ##要先清除表格資料
    x = treeview_data.get_children()
    for item in x:
        treeview_data.delete(item)
    # 資料部分
    date_rec_cos = cursor.execute('SELECT mid, pid, cpay, cdate FROM cosmetictab')
    date_rec_cos_tuple = tuple(date_rec_cos.fetchall())
    date_rec_stay = cursor.execute("SELECT mid, pid,spay, intime FROM staytab")
    date_rec_stay_tuple = tuple(date_rec_stay.fetchall())
    # print(date_rec_cos_tuple)
    # print(date_rec_stay_tuple)
    all_list = []
    expand_list = []
    cost = 0
    if date_rec_cos_tuple != ():
        for mid, pid, pay, time in date_rec_cos_tuple:
            expand_list = []
            # print(mid,pid,pay)
            master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
            pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
            write_time = (cursor.execute('SELECT cwritetime FROM cosmetictab WHERE pid = (?) and mid = (?) and cdate = (?)', [pid,mid,time])).fetchone()
            expand_list = (master_name[0], pet_id[0], time, '美容', pay, write_time[0])
            # print(expand_list)
            cost = cost + pay
            all_list.append(expand_list)

    if date_rec_stay_tuple != ():
        for mid, pid, pay, time in date_rec_stay_tuple:
            expand_list = []
            master_name = (cursor.execute('SELECT mname FROM mastertab WHERE mid = (?)', [mid])).fetchone()
            write_time = (cursor.execute('SELECT swritetime FROM staytab WHERE pid = (?) and mid = (?) and intime = (?)', [pid,mid,time])).fetchone()
            pet_id = (cursor.execute('SELECT pname FROM pettab WHERE pid = (?)', [pid])).fetchone()
            expand_list = (master_name[0], pet_id[0], time, '住宿', pay, write_time[0])
            # print(write_time)
            cost = cost + pay
            all_list.append(expand_list)
    all_tuple = list(all_list)
    for i in range(len(all_tuple)):
        treeview_data.insert('', 0, values=all_tuple[i])

show_all_data() ###直接顯示總表
acc = 'ym6060606'
password = '286555'
def Cost_Data_Delete():
    curItem = treeview_data.focus()
    if treeview_data.item(curItem)['values'] != "":
        Msg_delete = messagebox.askokcancel("注意!","你確定要刪除這筆資料嗎?")
        if Msg_delete == True:
            service_item = treeview_data.item(curItem)['values'][3]
            write_time_delete = treeview_data.item(curItem)['values'][5]
            # #資料庫上的刪除動作
            if service_item == "美容":
                cursor.execute("DELETE FROM cosmetictab WHERE cwritetime = (?)",[write_time_delete])
            else:
                cursor.execute("DELETE FROM staytab WHERE swritetime = (?)", [write_time_delete])
            #表格上的刪除動作
            des = treeview_data.selection()
            for de in des:
                treeview_data.delete(de)
    else:
        messagebox.showerror("注意!!","未選取任何資料")

def Leave_Backstage():
    tabcontrol.add(tab6, state='hidden')
    tabcontrol.add(tab8, state='hidden')
    tabcontrol.add(tab9, state='hidden')
    tabcontrol.add(tab7, state='normal')
    tabcontrol.select(tab7)
    tabcontrol.add(tab1, state='normal')
    tabcontrol.add(tab2, state='normal')
    tabcontrol.add(tab3, state='normal')
    tabcontrol.add(tab4, state='normal')
    tabcontrol.add(tab5, state='normal')
    Label_error['text'] = ''


###按鈕

data_delete_Btn = tk.Button(tab6, text='刪除資料',width='15',command=Cost_Data_Delete)
data_delete_Btn.place(relx=0.02,rely=0.10)
data_reset_Btn = tk.Button(tab6, text='重整',width='15',command=show_all_data)
data_reset_Btn.place(relx=0.02,rely=0.15)
data_reset_Btn = tk.Button(tab6, text='離開',width='15',command=Leave_Backstage)
data_reset_Btn.place(relx=0.02,rely=0.2)

##############總資料end



###############主人資料表

columns3 = ("1","2","3","4","5")
treeview_master_data = ttk.Treeview(tab8,height=25,show="headings",column=columns3)



treeview_master_data.column("1",width=150,anchor='center')
treeview_master_data.column("2",width=150,anchor='center')
treeview_master_data.column("3",width=100,anchor='center')
treeview_master_data.column("4",width=200,anchor='center')
treeview_master_data.column("5",width=200,anchor='center')

treeview_master_data.heading("1",text="名字")
treeview_master_data.heading("2",text="身分證")
treeview_master_data.heading("3",text="電話")
treeview_master_data.heading("4",text="地址")
treeview_master_data.heading("5",text="寵物")
treeview_master_data.place(relx=0.2,rely=0.025)

def show_master_data():
    ##要先清除表格資料
    x = treeview_master_data.get_children()
    for item in x:
        treeview_master_data.delete(item)
    # 資料部分
    date_rec_master = cursor.execute('SELECT mname, mid, mphone, maddress FROM mastertab')
    date_rec_master_tuple = tuple(date_rec_master.fetchall())

    all_master_list = []
    expand_list = []

    if date_rec_master_tuple != ():
        for mname, mid, mphone, maddress in date_rec_master_tuple:
            expand_list = []
            # print(mid,pid,pay)
            petname = cursor.execute('SELECT pname FROM pettab WHERE mid = (?)',[mid]).fetchall()
            petname_list = []

            if len(petname)!=0 :###寵物名稱串列增加逗號
                for pet in petname:
                    petname_list.append(pet[0])
                s=",".join(petname_list)
            else:
                s=petname_list
            expand_list = (mname, mid, mphone, maddress, s)
            # print(expand_list)

            all_master_list.append(expand_list)


    all_master_tuple = list(all_master_list)
    for i in range(len(all_master_tuple)):
        treeview_master_data.insert('', 0, values=all_master_tuple[i])

###按鈕

master_data_reset_Btn = tk.Button(tab8, text='重整',width='15',command=show_master_data)
master_data_reset_Btn.place(relx=0.02,rely=0.15)
master_data_quit_Btn = tk.Button(tab8, text='離開',width='15',command=Leave_Backstage)
master_data_quit_Btn.place(relx=0.02,rely=0.2)
show_master_data() ###一開始直接顯示主人資料
###############主人資料end

#############後台登入介面

Log_in_txt = tk.Label(tab7,text='後臺登入系統',font=('microsoft yahei', 15,'bold'))
Log_in_txt.place(relx=0.45,rely=0.05,anchor='center')
Log_in_acc = tk.Label(tab7,text='帳號',font=('microsoft yahei', 11))
Log_in_acc.place(relx=0.45,rely=0.15,anchor='center')
Acc_entry = tk.Entry(tab7)
Acc_entry.place(relx=0.45,rely=0.2,anchor='center')
Log_in_password = tk.Label(tab7,text='密碼',font=('microsoft yahei', 11))
Log_in_password.place(relx=0.45,rely=0.25,anchor='center')
Password_entry = tk.Entry(tab7,show='*')
Password_entry.place(relx=0.45,rely=0.3,anchor='center')
Label_error = tk.Label(tab7,text='')
Label_error.place(relx=0.45,rely=0.47,anchor='center')

def Log_in():
    get_acc = Acc_entry.get()
    get_pass = Password_entry.get()
    if get_acc == acc and get_pass == password:
        tabcontrol.add(tab6,state='normal')
        tabcontrol.add(tab8, state='normal')
        tabcontrol.add(tab9, state='normal')
        tabcontrol.add(tab7,state='hidden')
        tabcontrol.select(tab6)
        Acc_entry.delete(0, 'end')
        Password_entry.delete(0, 'end')
        tabcontrol.add(tab1, state='disable')
        tabcontrol.add(tab2, state='disable')
        tabcontrol.add(tab3, state='disable')
        tabcontrol.add(tab4, state='disable')
        tabcontrol.add(tab5, state='disable')
        show_all_data() #重整
    else:
        Label_error['text'] = '帳號或密碼錯誤!'






Log_in_Btn = tk.Button(tab7, text='登入',width='15',command=Log_in)
Log_in_Btn.place(relx=0.45,rely=0.37,anchor='center')


########位址備份


SRC_PATH = tk.Label(tab9,text='資料庫位址:',font=('Arial', 18))
SRC_PATH.place(relx=0.25,rely=0.20,anchor='center')
DES_PATH = tk.Label(tab9,text='目的地位址:',font=('Arial', 18))
DES_PATH.place(relx=0.25,rely=0.30,anchor='center')
SRC_PATH_SHOW = tk.Entry(tab9, width=50)
SRC_PATH_SHOW.place(relx=0.45,rely=0.20,anchor='center')
DES_PATH_SHOW = tk.Entry(tab9, width=50)
DES_PATH_SHOW.place(relx=0.45,rely=0.30,anchor='center')
text = []
location_f = open('location.txt','r')
for line in location_f:
    text.append(line)
src_path = text[0]
des_path = text[1]
SRC_PATH_SHOW.insert('end',src_path)
SRC_PATH_SHOW['state']='disable'
DES_PATH_SHOW.insert('end',des_path)
DES_PATH_SHOW['state']='disable'

def ChangePath():
    backup.back_up_des_path()
    text = []
    location_f = open('location.txt', 'r')
    for line in location_f:
        text.append(line)
    src_path = text[0]
    des_path = text[1]
    SRC_PATH_SHOW['state'] = 'normal'
    DES_PATH_SHOW['state'] = 'normal'
    SRC_PATH_SHOW.delete(0,'end')
    DES_PATH_SHOW.delete(0,'end')
    SRC_PATH_SHOW.insert('end', src_path)
    SRC_PATH_SHOW['state'] = 'disable'
    DES_PATH_SHOW.insert('end', des_path)
    DES_PATH_SHOW['state'] = 'disable'



ChangePath_button = tk.Button(tab9,text='變更',width=10,command=ChangePath)
ChangePath_button.place(relx=0.65,rely=0.30,anchor='center')
ChangePath_quit_Btn = tk.Button(tab9, text='離開',width='15',command=Leave_Backstage)
ChangePath_quit_Btn.place(relx=0.02,rely=0.2)


#####quit button

quit_button1 = tk.Button(tab1,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button1.place(relx=0.92,rely=0.001)
quit_button2 = tk.Button(tab2,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button2.place(relx=0.92,rely=0.001)
quit_button3 = tk.Button(tab3,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button3.place(relx=0.92,rely=0.001)
quit_button4 = tk.Button(tab4,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button4.place(relx=0.92,rely=0.001)
quit_button5 = tk.Button(tab5,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button5.place(relx=0.92,rely=0.001)
quit_button7 = tk.Button(tab7,text='離開',width=10,command=window.quit,fg='black',bg='grey')
quit_button7.place(relx=0.92,rely=0.001)




window.mainloop()

# backup.backup_dube()

