from selenium import webdriver
import time
from datetime import datetime
import Global_var
import sys , os
import ctypes
import wx
import string
import re
import html
from insert_on_database import insert_in_Local
app = wx.App()
    
browser = webdriver.Chrome(executable_path=str(f"C:\\Translation EXE\\chromedriver.exe"))
browser.maximize_window()

        
def loader_process():
    loader_found = True
    while loader_found == True:
        try:
            browser.get('http://www.mpwz.co.in/#/home')
            time.sleep(10)
            try:
                for tenders in browser.find_elements_by_xpath('//*[@routerlink="/public-tender-ven"]'):
                    tenders.click()
                    time.sleep(6)
                    loader_found = False
                    break
            except:
                print('Error Tenders Nav')
                loader_found = True
                time.sleep(2)
        except:
            loader_found = True
    loader_find = True
    while loader_find == True:
        loader_find = False
        try:
            for wait_for_hide_loader in browser.find_elements_by_xpath('//*[@class="loadimg"]'):
                loader_find = True
        except:
            loader_find = True
            print('Error On Loader')

    time.sleep(2)
    Scrap_details()
def Scrap_details():
    try:
        alert = browser.switch_to.alert
        alert.accept()
        loader_process()
    except:
        pass
    a = 0
    while a == 0:
        try:
            table_outerHTML_main = ''
            for table_outerHTML in browser.find_elements_by_xpath('/html/body/app-root/app-public-tender-ven/div/div[2]/div/div[1]/div/table'):
                table_outerHTML = table_outerHTML.get_attribute('outerHTML').replace('\n','').replace('<!---->','').strip()
                table_outerHTML_main = re.sub('\s+', ' ', table_outerHTML)
                break
            if table_outerHTML_main != "":
                list_of_tbody = re.findall(r'(?<=<tbody _ngcontent).*?(?=</tbody>)' , table_outerHTML_main)
                del list_of_tbody[0]
                for tr_body in list_of_tbody:
                    list_of_tr = re.findall(r'(?<=<tr _ngcontent).*?(?=</tr>)' , tr_body)
                    del list_of_tr[0]
                    for td_body in list_of_tr:
                        SegFeild = []
                        for data in range(46):
                            SegFeild.append('')
                        td_list = re.findall(r'(?<=<td _ngcontent).*?(?=td>)' , td_body)

                        Date = td_list[1].partition(">")[2].partition("</")[0].strip()
                        SegFeild[41] = Date

                        datetime_object_pub = datetime.strptime(Date, '%Y-%m-%d')
                        User_Selected_date = datetime.strptime(str(Global_var.From_Date), '%Y-%m-%d')

                        timedelta_obj = datetime_object_pub - User_Selected_date
                        day = timedelta_obj.days

                        if day >= 0:
                            SegFeild[44] = td_list[0].partition(">")[2].partition("</")[0].strip()

                            Title = td_list[2].partition(">")[2].partition("</")[0].strip()
                            SegFeild[19] = string.capwords(Title).strip()

                            Document = td_list[3].partition('href="')[2].partition('"')[0].strip()
                            SegFeild[45] = Document.replace('#/','http://www.mpwz.co.in/#/')

                            SegFeild[3] = "NA" + "~" + "NA" + "~" + "NA" + "~" + "NA" + "~" + "NA"

                            SegFeild[20] = ""
                            SegFeild[22] = ""
                            SegFeild[14] = "2".strip()  # notice_type
                            SegFeild[7] = "IN"
                            SegFeild[12] = "MADHYA PRADESH PASCHIM KSHTETRA VIDYUT VITARAN COMPANY LTD."

                            SegFeild[18] = f'{SegFeild[19]}<br>\nDocument Number: {str(SegFeild[44])}<br>\nDate: {str(SegFeild[41])}'
                            SegFeild[26] = ""
                            SegFeild[27] = "0"  # Financier
                            SegFeild[28] = "http://www.mpwz.co.in/#/home"
                            SegFeild[31] = "mpwz.co.in"
                            SegFeild[36] = ""
                            SegFeild[42] = SegFeild[7]
                            SegFeild[43] = ""
                            for SegIndex in range(len(SegFeild)):
                                print(SegIndex, end=' ')
                                SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                                SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
                                print(SegFeild[SegIndex])
                            insert_in_Local(SegFeild)
                            Global_var.Total +=1
                            print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(Global_var.inserted) + " Skipped: " + str(Global_var.skipped) + " Deadline Not given: " + str(Global_var.deadline_Not_given) + " QC Tenders: " + str(Global_var.QC_tender),'\n')
                ctypes.windll.user32.MessageBoxW(0 , "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(Global_var.inserted) + "\n""Skipped: " + str(Global_var.skipped) + "\n""Deadline Not given: " + str(Global_var.deadline_Not_given) + "\n""QC Tenders: "+ str(Global_var.QC_tender) + "" , "sppp.rajasthan.gov.in" , 1)
                browser.close()
                time.sleep(2)
                sys.exit()
            else:
                print('Table not Found')
            a = 1
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a = 0
loader_process()
