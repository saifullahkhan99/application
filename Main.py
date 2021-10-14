
"""
this is the main script of project page
"""
import time,os,shutil
splash_start_time = time.time()
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter import messagebox
from importlib import reload
from PIL import Image, ImageTk
import datetime
import pdf
from distutils.dir_util import copy_tree
import requests









#todo defining and setting main window-----------------------------------------------------------------------------------------------------------------------------------------?
main_window = tk.ThemedTk(theme = 'radiance')
main_window.withdraw()

main_window_width = main_window.winfo_screenwidth() - 100
main_window_height = main_window.winfo_screenheight() - 100
splash_width = main_window_width/2 - 280
splash_height = main_window_height/2 -100
#--------------------<splash screen>------------------------------------->
root = Toplevel(main_window)
root.geometry("600x300+%d+%d"%(splash_width,splash_height))
# root.geometry("600x300+400+200")
root.overrideredirect(True)


splash_im = Image.open('Data/pics/ghanchi.bmp')
splash_im.thumbnail((670,360))
splash_img = ImageTk.PhotoImage(splash_im)



splash_label = Label(root, image = splash_img)
splash_label.pack(fill = BOTH,expand = True)


loading_im = Image.open('Data/pics/fsdf.png')
loading_im.thumbnail((30,30))
loading_img = ImageTk.PhotoImage(loading_im)

splash_loading = Label(splash_label, image = loading_img, bg = '#ffc30d')
splash_loading.place(relx = 0.48, rely = 0.88)


root.update()
def reappear(tm,):

    time.sleep(tm/2)
    root.destroy()
    main_window.deiconify()




#--------------------------------------------<splash screen ends>---------------------------------------------------------------------------------------------------------->






import NewEntry as entry_module
import admin as ad
from database import Database as db
from backup import Call_Backup
from difflib import SequenceMatcher
import threading

print(threading.active_count())


main_window.geometry("%dx%d+30+10" %(main_window_width,main_window_height))
main_window.title("New Ghanchi Steel")
main_window.iconbitmap("Data/pics/confirm.ico")
#--------------------------------------------------------------------X>




# todo styles ------------------------------------------------------------------------------------------------------------------------------------------------------->
table_frame_style = ttk.Style()
table_frame_style.configure('q.TFrame', background = '#bbd5d7')

top_frame_style = ttk.Style()
top_frame_style.configure('tf.TFrame', background ='#fffcf1')
# top_frame_style.configure('tf.TFrame', background ='#b2efef')

left_frame_style = ttk.Style()
left_frame_style.configure('lf.TFrame', background ='#fffcf1')
# left_frame_style.configure('lf.TFrame', background ='#db7093')






#TODO defining and placeing frames---------------------------------------------------------------------------------------------------------------------------------------------?
top_frame = ttk.Frame(main_window, height = 150, style = 'tf.TFrame')
left_frame = ttk.Frame(main_window, relief = 'raised', width = 180, style = 'lf.TFrame')
left_frame.pack_propagate(False)
table_frame = ttk.Frame(main_window, relief = 'sunken',borderwidth = 5, style = 'q.TFrame')
#placing
left_frame.pack(fill = Y, side = LEFT)
top_frame.pack(fill =BOTH, )
table_frame.pack(fill = BOTH,expand = True)
table_frame.grid_propagate(False)
table_frame.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10,11,), pad = 5, weight = 1,)
table_frame.grid_columnconfigure(0, pad = 10, weight = 1, minsize = 10,)
top_frame.grid_propagate(False)
top_frame.grid_columnconfigure(0,pad = 10)
top_frame.grid_rowconfigure(1,pad = 20)

process_window = entry_module.proceeing_window(main_window)
#---------------------------------------------------------------------------------------------X>

dt = datetime.datetime.now()
current_date = dt.date().strftime("%B %d, %Y")

data = db('Data/database/database.db')
var_date = StringVar()
# tem_date_label = Label(top_frame, text = 'Date: ', bg = '#fffcf1')
# tem_date_entry = ttk.Entry(top_frame, width = 20, textvariable = var_date)
#
# tem_date_label.place(relx = 0.5, rely = 0.4)
# tem_date_entry.place(relx = 0.55, rely = 0.4, height = 26)
#



#------------------database backup------------------------------------------------->
copy_days1 = [1,2,3,4,5]
copy_days2 = [25,26,27,28]
copy_day = datetime.datetime.today().day
copy_month = datetime.datetime.today().month
copy_year = datetime.date.today().year

file_chk1 = os.path.isfile(f'./Data/database/backups/database_{copy_month}_{copy_year}_{1}.db')
file_chk2= os.path.isfile(f'./Data/database/backups/database_{copy_month}_{copy_year}_{2}.db')
try:
    if file_chk1 == False or file_chk2 == False:
        fromDirectory = "./Data/database/backups"
        toDirectory = f"./Data/backup/backup{copy_year}_{copy_month}_{copy_day}"
        if copy_day in copy_days1:
            data.backup(copy_month,copy_year,1)
            shutil.copytree(fromDirectory, toDirectory, False, None)
        elif copy_day in copy_days2:
            data.backup(copy_month,copy_year,2)
            shutil.copytree(fromDirectory, toDirectory, False, None)
        else:
            pass
except FileExistsError:
    pass

#----------------------------------------------------------------------------------->









#todo defining headings insde table frame--------------------------------------------------------------------------------------------------------------------------------------?

heading_count = ttk.Label(table_frame, text = '#No', font = 'Arial 11', anchor = 'center',width = 4)
heading_code = ttk.Label(table_frame, text = 'Code', font = 'Arial 11', anchor = CENTER,width = 3)
heading_description = ttk.Label(table_frame, text = 'Description', font = 'Arial 11', anchor = CENTER,justify = CENTER)
heading_weight = ttk.Label(table_frame, text = 'Weight', font = 'Arial 11', anchor = CENTER,width = 3)
heading_cost = ttk.Label(table_frame, text = 'Cost/kg', font = 'Arial 11', anchor = CENTER,width = 3)
heading_amount = ttk.Label(table_frame, text = 'Amount', font = 'Arial 11', anchor = 'center',width = 3)

#--------------------------------------------------------------------------------------------------X>









#todo defining personal info stuff-----------------------------------------------------------------------------------------------------------------?
info_label_field = LabelFrame(top_frame, width = 400, text ="Billing Information", relief = 'groove',bg = '#fffcf1', bd = 4)
search_frame = LabelFrame(top_frame, width = 400, text ="Search", relief = 'groove',bg = '#fffcf1', bd = 4, height= 140)
search_frame.place(relx = 0.75, rely = 0.01)
twofields = entry_module.TwoFields(main_window)
twofields.var_current_date.set(current_date)
#------------------------------------------------------------------------------------------------------------->


#todo defining object variables---------------------------------------------------------------------------------------------------------------------->

#personal info variables
var_obj_name = StringVar()
var_obj_phone = StringVar()
var_obj_bill = IntVar()
var_obj_bill.set(data.bill_id())
var_b_partner_id = StringVar()
var_addr = StringVar()
direct_sale_cost = DoubleVar()

search_var = StringVar()
#---------------------------------------------------------------------------------------------------------------------->


#todo search frame------------>
var_check_search = IntVar()
search_list = []
def search_bill():
    search_list = []
    vals = data.search()

    for tup in vals:
        date_search_ratio = SequenceMatcher(None,tup[2].lower(),search_var.get().lower()).ratio()
        name_search_ratio = SequenceMatcher(None, tup[1].lower(), search_var.get().lower()).ratio()
        if var_check_search.get() == 0 and (date_search_ratio > 0.9 or name_search_ratio >= 0.85):
            search_list.append(tup)
        elif var_check_search.get() == 1 and (date_search_ratio > .7 or name_search_ratio > .55):
            search_list.append(tup)

    search_top = Toplevel(main_window)
    search_top.geometry("600x600+%d+%d"%(100,100))
    search_top.iconbitmap("Data/pics/search.png")
    tree = ttk.Treeview(search_top)
    tree['column'] = ('one',"two", "three",)
    tree.column('#0', width=60, anchor='center')
    tree.column('one', width=100, anchor='center')
    tree.column('two', width=200, anchor='center')
    tree.column('three', width=200, anchor='center')

    


    tree.heading("#0", text="SNO", )
    tree.heading("one", text="Bill No", )
    tree.heading("two", text="Date")
    tree.heading("three", text="Name")
    
    tree.pack_propagate(False)
    tree.pack(fill = Y, expand = True )
    scr = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scr.set)
    scr.pack(side=RIGHT, fill=Y)

    count = 1
    for x in search_list:
        tree.insert('', 'end', text=count, values=x)
        count += 1




try:
    serach_pic = Image.open('Data/pics/search.png')
    serach_pic.thumbnail((55, 25))
    search_img = ImageTk.PhotoImage(serach_pic)

except FileNotFoundError:
    search_img = ""


chk_style = ttk.Style()

chk_style.configure('n.TCheckbutton', background ='#fffcf1')


search_label = Label(search_frame, text = '(month day, year / Name)',bg = '#fffcf1')
search_field = ttk.Entry(search_frame, width = 30, textvariable = search_var)
search_btn = Button(search_frame, image = search_img, command = search_bill, width = 40)
loose_search_check = ttk.Checkbutton(search_frame, text = 'loose search',variable = var_check_search, style = 'n.TCheckbutton')

search_label.place(relx = 0.23, rely = 0.15)
search_field.place(relx = 0.2, rely = 0.37, height = 30)
search_btn.place(relx = 0.67, rely = 0.36)
loose_search_check.place(relx = 0.2, rely = 0.7)









#todo making entry objects------------------------------------------------------------------------------------------------------------------------>
#table
ob1 = entry_module.Entry_object(table_frame,)
ob2 = entry_module.Entry_object(table_frame,)
ob3 = entry_module.Entry_object(table_frame,)
ob4 = entry_module.Entry_object(table_frame,)
ob5 = entry_module.Entry_object(table_frame,)
ob6 = entry_module.Entry_object(table_frame,)
ob7 = entry_module.Entry_object(table_frame,)
ob8 = entry_module.Entry_object(table_frame,)


#personal info
obj_info = entry_module.CustomerInfo(info_label_field, var_obj_name, var_obj_phone, var_obj_bill,var_b_partner_id,var_addr)


#---------------------------------------------------=======------------------------------------------------------------>




var_invoice_name = StringVar()
var_invoice_phone = StringVar()

var_direct_sale = False
direct_cost_list = []
TestList = ["","",""]
vars = []
gobackvar = 0
after_print = 0
#todo new entry processing-------------------------------------------------------------------------------------------------------------------->

def process():



    current_time = dt.time().strftime("%I:%M")
    #adding customer info to TestList
    TestList[0] = var_obj_bill.get()
    TestList[1] = var_obj_name.get()
    TestList[2] = var_obj_phone.get()



    #Getting DataList for Processing---------------------->
    DataList = []
    for x in TestList:
        if x != ("",):
            DataList.append(x)




    #Varification to processing Window---------------------------------------->
    if  len(DataList) == 3:
           messagebox.showerror("Empty Entries", "Fill at least one entry")
           return False
    elif var_obj_name.get() == "" or var_obj_name.get().isspace():
        messagebox.showerror("Name Error","please enter customer name..")
        return False
    # elif var_obj_phone.get() == "" or var_obj_phone.get().isspace():
    #     messagebox.showerror("Phone Error", "please Enter customer number")
    #     return False
    #
    # elif len(var_obj_phone.get()) != 11:
    #     messagebox.showerror("Phone Error", "phone number is incorrect")
    #     return False




    #--------------------------<forgetting widgets>------------------------------------------------->
    info_label_field.grid_forget()
    table_frame.grid_forget()
    table_frame.pack_forget()
    table_frame.pack_propagate(False)
    table_frame.grid_propagate(False)
    twofields.bottom_field.pack_forget()
    top_frame.pack_forget()
    top_frame.pack_propagate(False)



    #setting processing window size------------------------
    # main_window.geometry("%dx%d+200+10" % (main_window_width-400, main_window_height))



#-----------------------<forgetting completed>---------------------------------------------->








# todo preview Values--------------------------------------------------------------------------------------------------------------------------------------->

    order_sale.configure(state = 'disabled')
    bill_no = DataList.pop(0)
    bill_name = DataList.pop(0)
    phone = DataList.pop(0)
    partner_id = var_b_partner_id.get()
    address = var_addr.get()

    process_window.var_cust_name.set(bill_name)
    process_window.var_cust_phone.set(phone)
    process_window.var_bp_id.set(bill_no)



 # Setting Up Preview Values And getting Total List

    TotalList = []
    var_x = 1
    process_window.desc_forget()
    for tup in DataList:
        num_var = StringVar(value = var_x)
        cod_var = StringVar(value = tup[0])
        cost_var = StringVar(value = tup[1])
        wgt_var = StringVar(value = tup[2])
        amount_var = StringVar(value = tup[3])

        Label(process_window.conf_desc_frame,textvariable = num_var,
              bg = '#79e9de').grid(row = var_x, column=0, sticky=EW, ipady=5)
        Label(process_window.conf_desc_frame,textvariable = cod_var,
              bg = '#79e9de').grid(row = var_x, column=1, sticky=EW, ipady=5)
        Label(process_window.conf_desc_frame,textvariable = cost_var,
              bg = '#79e9de').grid(row = var_x, column=2, sticky=EW, ipady=5)
        Label(process_window.conf_desc_frame,textvariable = wgt_var,
              bg = '#79e9de').grid(row = var_x, column=3, sticky=EW, ipady=5)
        Label(process_window.conf_desc_frame,textvariable = amount_var,
              bg = '#79e9de').grid(row = var_x, column=4, sticky=EW, ipady=5)
        TotalList.append(tup[3])
        var_x += 1

    total = sum(TotalList)

#           <--------------------------------------------------------------->


    process_window.var_paid.set(0)
    tot = total
    process_window.var_balance.set(tot)


    def entries_back(event):
        global  gobackvar
        gobackvar = 1
        new_entry_click()
        gobackvar = 0



    def Submit_Print(event):
        #window for asking---printing------------------>
        print_ask = Toplevel(main_window)
        print_width = main_window_width / 2 - 100
        print_height = main_window_height / 2 - 50
        print_ask.geometry("310x140+%d+%d"%(print_width,print_height))
        print_ask.configure(bg = 'silver')
        # print_ask.configure(bg = '#74629b')
        print_ask.grab_set()

        print_btn_style = ttk.Style()
        print_btn_style.configure('n.TButton', background ='silver')
        save_print = ttk.Button(print_ask, text = "Save & Print", style = 'n.TButton')
        save = ttk.Button(print_ask, text = "Save", style = 'n.TButton')
        print_quit =ttk.Button(print_ask, text = 'Cancel', style = 'n.TButton')

        save_print.place(relx = 0.1, rely = 0.2)
        save.place(relx = 0.55, rely = 0.2)
        print_quit.place(relx = 0.3, rely = 0.5)


        def print_quit_func(event):
            print_ask.destroy()
            print_ask.grab_release()


        def save_print_func(event,prnt):
            global after_print
            after_print =1
            if process_window.var_paid.get() == '':
                process_window.var_paid.set(0)

            if var_direct_sale == False:
                data.InsertSales(DataList, bill_name, phone, twofields.var_current_date.get(), total,
                 process_window.var_balance.get(), partner_id,address)
                tx = datetime.datetime.today().time().strftime("%H:%M:%S")
                val = data.retriev_bill(bill_no)
                pdf.Printer(val, tx, prnt)
            else:
                #direct sales bills-------
                data.InsertDirectSale(DataList, bill_name, phone, twofields.var_current_date.get(), total,
                                 process_window.var_balance.get(), partner_id, address)
                tx = datetime.datetime.today().time().strftime("%H:%M:%S")
                val = data.retriev_bill(bill_no)
                pdf.Printer(val, tx, prnt)



            time.sleep(0.5)
            print_ask.destroy()
            print_ask.grab_release()
            messagebox.showinfo("Saved", "Successfully Saved Bill")
            new_entry_click()
            var_b_partner_id.set("")
            var_obj_bill.set(data.bill_id())
            after_print = 0



        def on_closing():
            print_ask.destroy()
            print_ask.grab_release()

        #defining window's closing protocols
        print_ask.protocol("WM_DELETE_WINDOW", on_closing)
        save_print.bind("<ButtonPress>", lambda event:save_print_func(event,True))
        save.bind("<ButtonPress>", lambda event:save_print_func(event,False))
        print_quit.bind("<ButtonPress>", print_quit_func)







    def Customer_func():
        process_window.add()
        process_window.total_var.set(f'{tot:,}')

        process_window.paid_label.place(relx = 0.4, rely = 0.35)
        process_window.paid_entry.place(relx = 0.6, rely = 0.34,height = 28)


        process_window.balance_due_label.place(relx = 0.4, rely = 0.6)
        process_window.balance_due_value.place(relx = 0.6, rely = 0.6)


        process_window.total_name_label.configure(text = 'Total: ')
        process_window.paid_label.configure(text = "Paid: ")
        process_window.balance_due_label.configure(text = "Balance Due: ")
        process_window.print_btn.configure(state='disabled')

        def PaidOut(event):
            try:
                process_window.var_balance.set(tot - float(process_window.var_paid.get()))
                process_window.print_btn.configure(state='normal')
                process_window.print_btn.bind("<ButtonPress>", Submit_Print)
            except ValueError:
                messagebox.showerror("Paid","Please enter paid amount carefully...")

        process_window.paid_entry.bind("<Return>", PaidOut)



# <--------------------------------------------------------------------------------------------------------------->




    def Business_partner_func():
        process_window.add()
        process_window.total_var.set(f'{tot:,}')
        process_window.total_name_label.configure(text = 'Debit')
        process_window.var_paid.set(0)
        process_window.var_balance.set(total)

        process_window.paid_label.place_forget()
        process_window.paid_entry.place_forget()

        process_window.balance_due_label.place_forget()
        process_window.balance_due_value.place_forget()
        process_window.print_btn.configure(state = 'normal')
        process_window.print_btn.bind("<ButtonPress>", Submit_Print)
#       <----------------------------------------------------------------------------------------->


    if partner_id == '':
        Customer_func()

    else:
        Business_partner_func()


    #Go back Button-------------

    process_window.go_back_btn.bind("<ButtonPress>", entries_back)






#---------------------------------------------------------------------------------------------------------------------->

#next button....
process_btn = ttk.Button(twofields.bottom_field, text = 'Next', command = process)











# todo new entry button click---------------------------------------------------------->

# ----------------------<Stuff for new entry validation>------------------------------>
    #pics
done_pic = PhotoImage(file=r"Data/pics/tick.png")
cancel = PhotoImage(file=r"Data/pics/cancel.png")

    #labels
done_label1 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label2 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label3 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label4 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label5 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label6 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label7 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
done_label8 = Button(table_frame, image = done_pic, anchor = E, relief = 'flat', compound = TOP, bg = '#bbd5d7')
# -------------------------------------------------------------------------------------------->




# todo TickEdit objects----------------------------------------------------------------------->
# making tick edit objects
edit1 = entry_module.TickEdit(table_frame, done_label1, done_pic, cancel)
edit2 = entry_module.TickEdit(table_frame, done_label2, done_pic, cancel)
edit3 = entry_module.TickEdit(table_frame, done_label3, done_pic, cancel)
edit4 = entry_module.TickEdit(table_frame, done_label4, done_pic, cancel)
edit5 = entry_module.TickEdit(table_frame, done_label5, done_pic, cancel)
edit6 = entry_module.TickEdit(table_frame, done_label6, done_pic, cancel)
edit7 = entry_module.TickEdit(table_frame, done_label7, done_pic, cancel)
edit8 = entry_module.TickEdit(table_frame, done_label8, done_pic, cancel)

#functions handling for tickedit

EditDoneDict = {done_label1:edit1, done_label2:edit2, done_label3:edit3, done_label4:edit4,
                done_label5:edit5, done_label6:edit6, done_label7:edit7, done_label8:edit8,
                }

for key,value in EditDoneDict.items():
    key.bind("<Enter>", value.HoverEnter)
    key.bind("<Leave>", value.HoverLeave)

#---------------------------------------------------------------------------------------------------------------------->

var_initial = [
        ob1.var_code,ob2.var_code,ob3.var_code,ob4.var_code,ob5.var_code,ob6.var_code,ob7.var_code,ob8.var_code,
        ob1.var_cost,ob2.var_cost,ob3.var_cost,ob4.var_cost,ob5.var_cost,ob6.var_cost,ob7.var_cost,ob8.var_cost,
        ob1.var_desc,ob2.var_desc,ob3.var_desc,ob4.var_desc,ob5.var_desc,ob6.var_desc,ob7.var_desc,ob8.var_desc,
        ob1.var_amount,ob2.var_amount,ob3.var_amount,ob4.var_amount,ob5.var_amount,ob6.var_amount,ob7.var_amount,ob8.var_amount,
        ob1.var_weight,ob2.var_weight, ob3.var_weight,ob4.var_weight,ob5.var_weight,ob6.var_weight,ob7.var_weight,ob8.var_weight,
                  ]

for x in var_initial:
    x.set("")

entries =[
    (ob1.num_entry1,ob1.code_entry1,ob1.description_entry1,ob1.cost_entry1,ob1.weight_entry1,ob1.amount_entry1),
    (ob2.num_entry1,ob2.code_entry1,ob2.description_entry1,ob2.cost_entry1,ob2.weight_entry1,ob2.amount_entry1),
    (ob3.num_entry1,ob3.code_entry1,ob3.description_entry1,ob3.cost_entry1,ob3.weight_entry1,ob3.amount_entry1),
    (ob4.num_entry1,ob4.code_entry1,ob4.description_entry1,ob4.cost_entry1,ob4.weight_entry1,ob4.amount_entry1),
    (ob5.num_entry1,ob5.code_entry1,ob5.description_entry1,ob5.cost_entry1,ob5.weight_entry1,ob5.amount_entry1),
    (ob6.num_entry1,ob6.code_entry1,ob6.description_entry1,ob6.cost_entry1,ob6.weight_entry1,ob6.amount_entry1),
    (ob7.num_entry1,ob7.code_entry1,ob7.description_entry1,ob7.cost_entry1,ob7.weight_entry1,ob7.amount_entry1),
    (ob8.num_entry1,ob8.code_entry1,ob8.description_entry1,ob8.cost_entry1,ob8.weight_entry1,ob8.amount_entry1)
         ]



#change focus throug left right keys----------------------->
prss_list = []
for old_tup in entries:
    for bn in old_tup:
        prss_list.append(bn)


def press(event):
    current_entry = table_frame.focus_get()
    next_indx = prss_list.index(current_entry) + 1
    prev_indx = prss_list.index(current_entry) -1
    if event.keycode == 37:
        prss_list[prev_indx].focus_set()
    elif event.keycode == 39:
        prss_list[next_indx].focus_set()
    else:
        pass

for evn in entries:
    for wdg in evn:
        wdg.bind("<KeyPress>", press)



def direct_cost_zero(event):
    if var_direct_sale == True:
        twofields.var_cost.set("")
    else:
        pass

# todo New Entry Button----------------------------------------------------------------------------->


def new_entry_click():
    main_window.update_idletasks()
    global TestList,var_direct_sale
    global gobackvar
    global  var_initial
    var_partner_back = 0

    if gobackvar == 0:
        if TestList != ["","",""]:
            x = True
            if after_print == 0:
                x = messagebox.askokcancel("cancel", "Are You Sure")
            if x == True:
                TestList = ["","",""]
                var_addr.set("")
                twofields.var_cost.set("")
                twofields.var_weight.set("")
                order_sale.configure(state='normal')
                table_frame_style.configure('q.TFrame', background='#bbd5d7')
                var_direct_sale = False
                for x in var_initial:
                    x.set("")
                var_obj_phone.set("")
                var_obj_name.set("")

                for z in entries:
                    for x in z:
                        x.grid_forget()

                table_frame.grid_columnconfigure(12, weight=0)
                for q in EditDoneDict:
                    q.grid_forget()

                for t in entries:
                    x = (t[1], t[3], t[4])
                    for j in x:
                        j.configure(state="normal")
            else:
                return False


    if gobackvar == 0:
        obj_info.var_p_name.set('')
        obj_info.var_p_phone.set('')
        var_obj_name.set('')
        var_obj_phone.set('')
        var_addr.set("")
        twofields.var_weight.set("")
        twofields.var_cost.set("")
        var_partner_back = 0
        order_sale.configure(state='normal')


    process_window.forget()
    top_frame.pack(fill = X)
    top_frame.configure(height = 150)
    table_frame.pack(fill=BOTH, expand = True)

    obj_info.p_name.configure(text="")
    obj_info.p_phone.configure(text="")

    heading_count.grid(row=0, column=5, sticky=E, ipady=10)
    heading_code.grid(row=0, column=6, sticky=EW, ipady=10)
    heading_description.grid(row=0, column=7, columnspan=2, sticky=EW, ipady=10)
    heading_cost.grid(row=0, column=9, sticky=EW, ipady=10)
    heading_weight.grid(row=0, column=10, sticky=EW, ipady=10)
    heading_amount.grid(row=0, column=11, sticky=EW, ipady=10)



    main_window.geometry("%dx%d+30+10" % (main_window_width, main_window_height))
    ob1.add()
    twofields.add()



    # todo NewEntryValication object---------------------------------------------------------------------------------------------------------------->

    ValidatOb1 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob1.var_code,
                                                 var_cost = ob1.var_cost,var_weight=ob1.var_weight,
                                                 obj = ob2, done_label = done_label1, fr = table_frame, ind =3,code_entry=ob1.code_entry1,
                                                 cost_entry=ob1.cost_entry1,weight_entry = ob1.weight_entry1, desc_var = ob1.var_desc,
                                                 amount_var = ob1.var_amount, row = 1,)

    ValidatOb2 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob2.var_code,
                                                 var_cost = ob2.var_cost,var_weight =ob2.var_weight,
                                                 obj = ob3, done_label = done_label2, fr = table_frame, ind = 4,code_entry=ob2.code_entry1,
                                                 cost_entry=ob2.cost_entry1,weight_entry = ob2.weight_entry1, desc_var = ob2.var_desc,
                                                 amount_var = ob2.var_amount, row = 2)

    ValidatOb3 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob3.var_code,
                                                 var_cost = ob3.var_cost, var_weight= ob3.var_weight,
                                                 obj = ob4, done_label = done_label3, fr = table_frame, ind =5,code_entry=ob3.code_entry1,
                                                 cost_entry=ob3.cost_entry1,weight_entry = ob3.weight_entry1, desc_var = ob3.var_desc,
                                                 amount_var = ob3.var_amount, row = 3)

    ValidatOb4 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob4.var_code,
                                                 var_cost = ob4.var_cost, var_weight = ob4.var_weight,
                                                 obj = ob5, done_label = done_label4, fr = table_frame, ind = 6,code_entry=ob4.code_entry1,
                                                 cost_entry=ob4.cost_entry1,weight_entry = ob4.weight_entry1, desc_var = ob4.var_desc,
                                                 amount_var = ob4.var_amount, row = 4)

    ValidatOb5 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob5.var_code,
                                                 var_cost = ob5.var_cost, var_weight = ob5.var_weight,
                                                 obj = ob6, done_label = done_label5, fr = table_frame, ind = 7,code_entry=ob5.code_entry1,
                                                 cost_entry=ob5.cost_entry1,weight_entry = ob5.weight_entry1, desc_var = ob5.var_desc,
                                                 amount_var = ob5.var_amount, row = 5)

    ValidatOb6 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob6.var_code,
                                                 var_cost = ob6.var_cost, var_weight = ob6.var_weight,
                                                 obj = ob7, done_label = done_label6, fr = table_frame, ind = 8,code_entry=ob6.code_entry1,
                                                 cost_entry=ob6.cost_entry1,weight_entry = ob6.weight_entry1, desc_var = ob6.var_desc,
                                                 amount_var = ob6.var_amount, row = 6)

    ValidatOb7 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob7.var_code,
                                                 var_cost = ob7.var_cost, var_weight = ob7.var_weight,
                                                 obj = ob8, done_label = done_label7, fr = table_frame, ind = 9,code_entry=ob7.code_entry1,
                                                 cost_entry=ob7.cost_entry1,weight_entry = ob7.weight_entry1, desc_var = ob7.var_desc,
                                                 amount_var = ob7.var_amount, row = 7)

    ValidatOb8 = entry_module.NewEntryValidation(TestList,twofields.var_weight,twofields.var_cost,var_code = ob8.var_code,
                                                 var_cost = ob8.var_cost, var_weight = ob8.var_weight,
                                                 done_label = done_label8, fr = table_frame, ind = 10, obj = "",code_entry=ob8.code_entry1,
                                                 cost_entry = ob8.cost_entry1,weight_entry = ob8.weight_entry1, desc_var = ob8.var_desc,
                                                 amount_var = ob8.var_amount, row = 8)




    #binding Enter to all entries

    ValDict = {ValidatOb1:entries[0], ValidatOb2:entries[1], ValidatOb3:entries[2],
               ValidatOb4:entries[3], ValidatOb5:entries[4], ValidatOb6:entries[5],
               ValidatOb7:entries[6], ValidatOb8:entries[7]}
    for key,value in ValDict.items():
        for ki in value:
            ki.bind("<Return>", key.validate)


    ValDict = [ValidatOb1,ValidatOb2,ValidatOb3,ValidatOb4,ValidatOb5,ValidatOb6,ValidatOb7,ValidatOb8]
    t = 0
    for val in entries:
        val[4].bind("<Tab>", ValDict[t].FocOutWeight)
        val[1].bind("<Tab>", ValDict[t].FocOutCode)
        val[1].bind("<Tab>", direct_cost_zero, add="+")
        val[3].bind("<Tab>", ValDict[t].FocusCostOut)

        t +=1



#----------------------------------------------<NewEntryValidation finishes>------------------------------------------->
    Clickedit1 = entry_module.EditClicked(TestList, 3, var_code=ob1.var_code, var_cost=ob1.var_cost, var_weight=ob1.var_weight,
                                          lb=done_label1,
                                          code_entry=ob1.code_entry1, cost_entry=ob1.cost_entry1,
                                          weight_entry=ob1.weight_entry1, desc_var=ob1.var_desc,
                                          amount_var=ob1.var_amount)

    Clickedit2 = entry_module.EditClicked(TestList, 4, var_code=ob2.var_code, var_cost=ob2.var_cost, var_weight=ob2.var_weight,
                                          lb=done_label2,
                                          code_entry=ob2.code_entry1, cost_entry=ob2.cost_entry1,
                                          weight_entry=ob2.weight_entry1, desc_var=ob2.var_desc,
                                          amount_var=ob2.var_amount)

    Clickedit3 = entry_module.EditClicked(TestList, 5, var_code=ob3.var_code, var_cost=ob3.var_cost, var_weight=ob3.var_weight,
                                          lb=done_label3,
                                          code_entry=ob3.code_entry1, cost_entry=ob3.cost_entry1,
                                          weight_entry=ob3.weight_entry1, desc_var=ob3.var_desc,
                                          amount_var=ob3.var_amount)

    Clickedit4 = entry_module.EditClicked(TestList, 6, var_code=ob4.var_code, var_cost=ob4.var_cost, var_weight=ob4.var_weight,
                                          lb=done_label4,
                                          code_entry=ob4.code_entry1, cost_entry=ob4.cost_entry1,
                                          weight_entry=ob4.weight_entry1, desc_var=ob4.var_desc,
                                          amount_var=ob4.var_amount)

    Clickedit5 = entry_module.EditClicked(TestList, 7, var_code=ob5.var_code, var_cost=ob5.var_cost, var_weight=ob5.var_weight,
                                          lb=done_label5,
                                          code_entry=ob5.code_entry1, cost_entry=ob5.cost_entry1,
                                          weight_entry=ob5.weight_entry1, desc_var=ob5.var_desc,
                                          amount_var=ob5.var_amount)

    Clickedit6 = entry_module.EditClicked(TestList, 8, var_code=ob6.var_code, var_cost=ob6.var_cost, var_weight=ob6.var_weight,
                                          lb=done_label6,
                                          code_entry=ob6.code_entry1, cost_entry=ob6.cost_entry1,
                                          weight_entry=ob6.weight_entry1, desc_var=ob6.var_desc,
                                          amount_var=ob6.var_amount)

    Clickedit7 = entry_module.EditClicked(TestList, 9, var_code=ob7.var_code, var_cost=ob7.var_cost, var_weight=ob7.var_weight,
                                          lb=done_label7,
                                          code_entry=ob7.code_entry1, cost_entry=ob7.cost_entry1,
                                          weight_entry=ob7.weight_entry1, desc_var=ob7.var_desc,
                                          amount_var=ob7.var_amount)

    Clickedit8 = entry_module.EditClicked(TestList, 10, var_code=ob8.var_code, var_cost=ob8.var_cost, var_weight=ob8.var_weight,
                                          lb=done_label8,
                                          code_entry=ob8.code_entry1, cost_entry=ob8.cost_entry1,
                                          weight_entry=ob8.weight_entry1, desc_var=ob8.var_desc,
                                          amount_var=ob8.var_amount)

    EditDict = {
        done_label1: Clickedit1, done_label2: Clickedit2, done_label3: Clickedit3, done_label4: Clickedit4,
        done_label5: Clickedit5,
        done_label6: Clickedit6, done_label7: Clickedit7, done_label8: Clickedit8
    }
    for key, value in EditDict.items():
        key.bind("<ButtonPress>", value.clicked)

    # -----------------------------------------<setting intial code values>------------------------------------------------->

    info_label_field.grid(row=0, column=0, pady=5, padx=10, ipady=70)
    info_label_field.grid_propagate(False)
    obj_info.add()





# todo customer information----------------------------------------------------------------------------------------------------------------------------------------------------->
    def business_partner_go(event,vls):
        global gobackvar
        nonlocal var_partner_back
        if var_obj_name.get() == "" and var_obj_phone.get() == "":
            obj_info.b_parter()
            var_obj_name.set('')
            var_obj_phone.set('')
            return 'break'
        else:
            ask1 = messagebox.askquestion("discard!","Are You Sure want to discard")
            if ask1 == 'yes':
                obj_info.b_parter()
                var_obj_name.set('')
                var_obj_phone.set('')
                var_b_partner_id.set('')
                return 'break'
            else:
                return 'break'

    obj_info.b_partner_btn.bind("<ButtonPress>", lambda event:business_partner_go(event,False))



    #adding next button
    process_btn.place(relx = 0.87, rely = 0.02)


    def businessid(event):
        nonlocal var_partner_back
        partner_id_val = data.Business_ids(var_b_partner_id.get())
        obj_info.var_p_name.set('')
        obj_info.var_p_phone.set('')
        var_obj_name.set('')
        var_obj_phone.set('')
        obj_info.p_name.configure(text="")
        obj_info.p_phone.configure(text="")

        if partner_id_val == None:
            messagebox.showerror("id", "Wrong partner id...")
            return False

        else:
            print(partner_id_val[4])
            if partner_id_val[4] == 'close':
                partner_ask = messagebox.askyesno('Open', "This partner account has been close, you want to open it?")
                if partner_ask == False:
                    return False
                else:
                    try:
                        partner_balance = data.partner_balance(var_b_partner_id.get())
                        if partner_balance != 0:
                            balance_ask = messagebox.askyesno('Clear','you want to clear, previous due/balance for this account')
                            if balance_ask == False:
                                x = data.openpartner(var_b_partner_id.get())
                                if x != True:
                                    raise Exception
                            else:
                                x_again = data.openpartnernew(var_b_partner_id.get())
                                if x != True:
                                    raise Exception
                    except Exception:
                        print("got here")
                        return False
            p_name = partner_id_val[1]
            p_phone = partner_id_val[2]
            p_addr = partner_id_val[3]
            var_obj_name.set(p_name)
            var_obj_phone.set(p_phone)
            var_addr.set(p_addr)

            obj_info.p_name.configure(text = "Name:", font="Courier 10")
            obj_info.var_p_name.set(p_name)
            obj_info.var_p_phone.set(p_phone)
            obj_info.p_phone.configure(text = "Phone", font="Courier 10")
            var_partner_back = 1

    obj_info.p_id_entry.bind("<Return>",businessid)



    def GoBack(event):
        nonlocal var_partner_back
        if var_partner_back == 1:
            ask = messagebox.askquestion("Go Back", "Are You Sure, want to discard.")
            if ask == 'yes':
                obj_info.add()
                var_b_partner_id.set('')

                obj_info.var_p_name.set('')
                obj_info.var_p_phone.set('')
                var_obj_name.set('')
                var_obj_phone.set('')

                obj_info.p_name.configure(text="")
                obj_info.p_phone.configure(text="")

                var_partner_back = 0
                return 'break'
            elif ask == 'no':
                return 'break'

        else:

            obj_info.add()


    obj_info.p_info_back.bind("<ButtonPress>", GoBack)
#---------------------------------------------------------------------------------------------------------------------->





#todo admin section------------------------------------------------------------------------------------------------------------------------------------------------------------>
admin_click = True
def admin():

        global admin_click
        if admin_click == True:
            pass
        else:
            return False


       #admin top level definition
        admin_top = Toplevel()
        admin_top.withdraw()

        var_username = StringVar()
        var_password = StringVar()

#todo login window ---------------------------------------------------------------------------->
        login_width = main_window_width / 2 - 200
        login_height = main_window_height / 2 - 100
        login_top = Toplevel(main_window)

        login_top.geometry("310x140+%d+%d"%(login_width,login_height))
        login_top.title("Log In")
        login_top.iconbitmap("Data/pics/login.ico")

        login_top.grab_set()
        prompt_user_name_label = Label(login_top, text = "UserName: ")
        prompt_user_name_label.place(relx = 0.1, rely = 0.25,)

        prompt_user_name_value = ttk.Entry(login_top, width = 20, textvariable = var_username)
        prompt_user_name_value.place(relx = .4, rely = 0.25, height = 26)

        prompt_pass_label = Label(login_top, text = "Password: ",)
        prompt_pass_label.place(relx = 0.1, rely = 0.5,)

        prompt_pass_value = ttk.Entry(login_top, width = 20, textvariable = var_password, show = '*')
        prompt_pass_value.place(relx = 0.4, rely = 0.5, height = 26 )


        prompt_btn = Button(login_top, text = "Log in")
        prompt_btn.place(relx = 0.4, rely = 0.75)

        prompt_quit_btn = Button(login_top, text = 'Cancel', )
        prompt_quit_btn.place(relx = 0.6, rely = 0.75)

        login_err = Label(login_top,)
        login_err.place(relx = 0.15, rely = 0.01)
        login_err.pack(side = 'top',fill = 'x')
        prompt_user_name_value.focus_set()



        #on closing login window
        def on_closing():
            global admin_click
            login_top.destroy()
            login_top.grab_release()
            admin_click = True

        #on closing admin window
        def on_admin_closing():
            global admin_click
            admin_top.destroy()
            # admin_top.grab_release()
            admin_click = True

        #defining window's closing protocols
        login_top.protocol("WM_DELETE_WINDOW", on_closing)
        admin_top.protocol("WM_DELETE_WINDOW", on_admin_closing)

        #function for clicking cancel in login window
        def login_quit(event):
            global admin_click
            login_top.destroy()
            admin_click = True
            # main_window.grab_set()



        #checking username and password
        def LogIn(event):
            user = var_username.get()
            passw = var_password.get()
            # admin_top.deiconify()
            # login_top.destroy()
            login_top.grab_release()

            admin_info = data.admin_login()
            if admin_info == None:
                data.InsertAdminInfo('saifullah','root')
                username = 'saifullah'
                password = 'root'
            else:
                username = admin_info[0]
                password = admin_info[1]


            if user.lower() == username and passw == password:
                admin_top.deiconify()
                login_top.destroy()
            else:
                login_err.configure(text = "Wrong username or password...", bg = 'red')
                return False


        prompt_btn.bind("<ButtonPress>", LogIn)
        prompt_pass_value.bind("<Return>", LogIn, add = "+")
        prompt_quit_btn.bind("<ButtonPress>", login_quit)

        admin_width = main_window_width / 2 - 380
        admin_height = main_window_height / 2 -250
        admin_top.title("Admin")
        admin_top.geometry("850x550+%d+%d"%(admin_width,admin_height))
        admin_top.configure(bg = '#6b238f')
        # admin_top.grab_set()





        # admin_top.grab_set()
        admin_click = False
    #---------------------------------------------------->


        #-----------<making admin objects----------------->

        obj_admin_left = ad.AdminLeftFrame(admin_top)
        obj_admin_top = ad.AdminTopFrame(admin_top)
        obj_admin_middle = ad.AdminMiddleFrame(admin_top)
        obj_admin_left.add()

        items_bar = ad.AdminItems(obj_admin_middle.admin_middle_frame)

        admin_business_left_btn = ad.BusinessPartners(obj_admin_middle.admin_middle_frame)
        admin_dashboard = ad.Dashboard(obj_admin_middle.admin_middle_frame)

        admin_orders = ad.Orders(obj_admin_middle.admin_middle_frame)
        admin_settings = ad.Settings(obj_admin_middle.admin_middle_frame)
        admin_profit = ad.Profits(obj_admin_middle.admin_middle_frame)
        #------------------<event functions>------------------------>
        admin_dashboard.add()


       #----------------<Items>------------------------->
        def func_admin_left_items_click(event):
            obj_admin_middle.forget()
            items_bar.add()
            items_bar.view_items(event)
            items_bar.chang_bg(event)


            # obj_admin_middle.add()

            try:
                set_img = Image.open('Data/pics/admin/item.png')
                set_img.thumbnail((80,60))
                img = ImageTk.PhotoImage(set_img)
                obj_admin_top.message_image.configure(image = img)
                obj_admin_top.message_image.image = img

            except FileNotFoundError:
                obj_admin_top.message_image = Label(obj_admin_top, text = "image not found", font = 'arial 8')
            obj_admin_top.message_label.configure(text = "Items", font = "arial 22 bold", fg = 'red')







       #dashboard image
        try:
            set_img = Image.open('Data/pics/dashboard.png')
            set_img.thumbnail((80, 60))
            img = ImageTk.PhotoImage(set_img)
            obj_admin_top.message_image.configure(image=img)
            obj_admin_top.message_image.image = img

        except FileNotFoundError:
            obj_admin_top.message_image = Label(obj_admin_top, text="image not found", font='arial 8')
        obj_admin_top.message_label.configure(text="Dashboard", font="arial 22 bold", fg='red')

        def func_admin_dashboard(event):
            try:
                set_img = Image.open('Data/pics/dashboard.png')
                set_img.thumbnail((80, 60))
                img = ImageTk.PhotoImage(set_img)
                obj_admin_top.message_image.configure(image=img)
                obj_admin_top.message_image.image = img

            except FileNotFoundError:
                obj_admin_top.message_image = Label(obj_admin_top, text="image not found", font='arial 8')
            obj_admin_top.message_label.configure(text="Dashboard", font="arial 22 bold", fg='red')

            admin_dashboard.add()






     #-------------------------<event assigning>--------------------------------->

        obj_admin_left.admin_left_itmes_btn.bind("<ButtonPress>", func_admin_left_items_click)
        obj_admin_left.dasboard_btn.bind("<ButtonPress>", func_admin_dashboard)

        #----------------------------------<Business partner>--------------------------------
        # functions
        def func_business_partner(event):
            obj_admin_middle.forget()
            admin_business_left_btn.add()

            admin_business_left_btn.partners(event)
            admin_business_left_btn.chang_bg(event)

            try:
                set_img = Image.open('Data/pics/partner.png')
                set_img.thumbnail((80, 60))
                img = ImageTk.PhotoImage(set_img)
                obj_admin_top.message_image.configure(image=img)
                obj_admin_top.message_image.image = img

            except FileNotFoundError:
                obj_admin_top.message_image = Label(obj_admin_top, text="image not found", font='arial 8')
            obj_admin_top.message_label.configure(text="Partners", font="arial 22 bold", fg='red')


        obj_admin_left.partners_btn.bind("<ButtonPress>", func_business_partner)




#----------------------------------------------------------------------------------------------------->
        def func_admin_orders(event):
            obj_admin_middle.forget()
            admin_orders.add()


            admin_orders.Order_Logs_Show(event)
            admin_orders.chang_bg(event)

            try:
                set_img = Image.open('Data/pics/orders.png')
                set_img.thumbnail((80, 60))
                img = ImageTk.PhotoImage(set_img)
                obj_admin_top.message_image.configure(image=img)
                obj_admin_top.message_image.image = img

            except FileNotFoundError:
                obj_admin_top.message_image = Label(obj_admin_top, text="image not found", font='arial 8')
            obj_admin_top.message_label.configure(text="Orders", font="arial 22 bold", fg='red')




        obj_admin_left.orders_btn.bind("<ButtonPress>", func_admin_orders)




        #admin settings
        def Admin_Settings_Func(event):
            obj_admin_middle.forget()
            admin_settings.add()

            try:
                set_img = Image.open('Data/pics/settings.png')
                set_img.thumbnail((80, 60))
                img = ImageTk.PhotoImage(set_img)
                obj_admin_top.message_image.configure(image=img, background = '#6b238f')
                obj_admin_top.message_image.image = img

            except FileNotFoundError:
                obj_admin_top.message_image = Label(obj_admin_top, text="image not found", font='arial 8',bg = '#6b238f')
            obj_admin_top.message_label.configure(text="Settings", font="arial 22 bold", fg='red')

        obj_admin_left.settings_btn.bind("<ButtonPress>", Admin_Settings_Func)



        #admin profit

        def Admin_Profit_Func(event):
            obj_admin_middle.forget()
            admin_profit.add()

        obj_admin_left.profit_btn.bind("<ButtonPress>", Admin_Profit_Func)








#todo defining and placing button on left frames............................................................................................................


try:
    add_img = Image.open('Data/pics/new1.png')
    add_img.thumbnail((100, 25))
    new_entry_img = ImageTk.PhotoImage(add_img)

except FileNotFoundError:
    new_entry_img = ""

try:
    admin_add_img = Image.open('Data/pics/admin1.png')
    admin_add_img.thumbnail((100, 25))
    admin_img = ImageTk.PhotoImage(admin_add_img)

except FileNotFoundError:
    admin_img = ""


try:
    bill_add_img = Image.open('Data/pics/bill1png.png')
    bill_add_img.thumbnail((100, 25))
    bill_img = ImageTk.PhotoImage(bill_add_img)

except FileNotFoundError:
    bill_img = ""


#peding image
try:
    pend_img = Image.open('Data/pics/pending.png')
    pend_img.thumbnail((100, 25))
    pending_img = ImageTk.PhotoImage(pend_img)

except FileNotFoundError:
    pending_img = ""



#discount image
try:
    dis_img = Image.open('Data/pics/discount.png')
    dis_img.thumbnail((100, 25))
    discount_img = ImageTk.PhotoImage(dis_img)

except FileNotFoundError:
    discount_img = ""





#bill return image

try:
    ret_img = Image.open('Data/pics/return.png')
    ret_img.thumbnail((100, 25))
    return_img = ImageTk.PhotoImage(ret_img)

except FileNotFoundError:
    return_img = ""




#return funciton
def return_bill_func():
    return_bill = entry_module.ReturnBill(main_window,)
    return_bill.add()
    return_bill.return_top.grab_set()

    def on_return_closing():
        return_bill.return_top.destroy()
        return_bill.return_top.grab_release()
        var_obj_bill.set(data.bill_id())
    return_bill.return_top.protocol("WM_DELETE_WINDOW", on_return_closing)



#Pending function
def func_pending():
    entry_module.CashPending(main_window)





view_bill = entry_module.View_Bill(table_frame)
discount = entry_module.AddDiscount(table_frame)


#button styles
bts = ttk.Style()
bts.configure('bt.TButton', background ='#fffcf1')
# bts.configure('bt.TButton', background ='#db7093')



try:
    top_pc = Image.open('Data/pics/monogram.png')
    top_pc.thumbnail((400, 200))
    top_img = ImageTk.PhotoImage(top_pc)

except FileNotFoundError:
    top_img = ""

top_img_label = Label(left_frame, image = top_img, bg = '#fffcf1')
top_img_label.image = top_img
top_img_label.pack(side = 'top')


#direct sale
try:
    dirct = Image.open('Data/pics/bill.png')
    dirct.thumbnail((55, 25))
    direct_img = ImageTk.PhotoImage(dirct)

except FileNotFoundError:
    direct_img = ""



#dropbox pic
try:
    drop = Image.open('Data/pics/dropbox_icon.png')
    drop.thumbnail((55, 25))
    dropbox_img = ImageTk.PhotoImage(drop)

except FileNotFoundError:
    dropbox_img = ""

def make_backup():
    
    ask = Toplevel(main_window)
    ask_width = main_window_width / 2 - 200
    ask_height = main_window_height / 2 - 100
    ask.geometry("310x140+%d+%d" % (ask_width, ask_height))
    ask.title("Log In")
    ask.iconbitmap("Data/pics/login.ico")
    ask.title("Password")
    ask.iconbitmap("Data/pics/login.ico")
    ask.grab_set()

    var_password = StringVar()

    def dest():
        ask.destroy()
        ask.grab_release()
        return False

    def on_closing():
        ask.grab_release()
        ask.destroy()

    ask.protocol("WM_DELETE_WINDOW", on_closing)

    err = Label(ask, font="arial 11 italic", justify='center')
    pass_label = Label(ask, text="Password: ", )
    pass_value = ttk.Entry(ask, width=20, textvariable=var_password, show='*')
    ask_backup = Button(ask, text="Backup", width=10)
    ask_quit = Button(ask, text="Quit", width=10, command=dest)

    err.pack(side='top', fill='x')

    pass_label.place(relx=0.1, rely=0.3)
    pass_value.place(relx=0.37, rely=0.3, height=27)

    ask_backup.place(relx=0.15, rely=0.6)
    ask_quit.place(relx=0.5, rely=0.6)

    pass_value.focus_set()

    def call_the_backup():
        try:
            backup_btn.configure(state = 'disabled')
            ask.destroy()     
            Call_Backup()              
            backup_btn.configure(state = 'normal')
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Internet", "Please, check your internet connection and try again")
            ask.destroy()
            backup_btn.configure(state = 'normal')

        

    
    def Call_Make_Backup(event):  
        try:
            if var_password.get() == data.admin_login()[1]:
                ask.destroy()
                thread.start()

            else:
                err.configure(text = 'Wrong password...', bg = 'red')
                return False                   
                messagebox.showinfo("seccess", "Successfully completed backup!")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Internet", "Please, check your internet connection and try again")
            ask.destroy()

    thread = threading.Thread(target = call_the_backup)
    ask_backup.bind("<ButtonRelease>",Call_Make_Backup)
    pass_value.bind("<Return>",Call_Make_Backup)




# process_btn.configure(command=lambda: process(False))
def DirectSale():
    global var_direct_sale

    if var_direct_sale == True:
        var_direct_sale = False
        # process_btn.configure(command=lambda: process(False))
        table_frame_style.configure('q.TFrame', background='#bbd5d7')
        twofields.cost_value.configure(state='readonly')
        return False



    ask = Toplevel(main_window)
    ask_width = main_window_width / 2 - 200
    ask_height = main_window_height / 2 - 100
    ask.geometry("310x140+%d+%d" % (ask_width, ask_height))
    ask.title("Log In")
    ask.iconbitmap("Data/pics/login.ico")
    ask.title("Password")
    ask.iconbitmap("Data/pics/login.ico")
    ask.grab_set()

    var_password = StringVar()

    def dest():
        ask.destroy()
        ask.grab_release()
        return False

    def on_closing():
        ask.grab_release()
        ask.destroy()

    ask.protocol("WM_DELETE_WINDOW", on_closing)



    def change_to_direct(event):
        global var_direct_sale
        if var_password.get() == data.admin_login()[1]:
            twofields.cost_value.configure(state = 'normal')
            var_direct_sale = True
            table_frame_style.configure('q.TFrame', background='red')
            ask.destroy()
        else:
            err.configure(text = 'Wrong password...', bg = 'red')
            return False

    err = Label(ask, font="arial 11 italic", justify='center')
    pass_label = Label(ask, text="Password: ", )
    pass_value = ttk.Entry(ask, width=20, textvariable=var_password, show='*')
    ask_cancel = Button(ask, text="Order-Sale", width=10)
    ask_quit = Button(ask, text="Quit", width=10, command=dest)

    err.pack(side='top', fill='x')

    pass_label.place(relx=0.1, rely=0.3)
    pass_value.place(relx=0.37, rely=0.3, height=27)

    ask_cancel.place(relx=0.15, rely=0.6)
    ask_quit.place(relx=0.5, rely=0.6)

    pass_value.focus_set()
    ask_cancel.bind("<ButtonRelease>",change_to_direct)
    pass_value.bind("<Return>",change_to_direct)



new_entry_btn = ttk.Button(left_frame, text = "New Entry", command = new_entry_click, image = new_entry_img ,compound = 'left',
                           style = 'bt.TButton')

order_sale = ttk.Button(left_frame, text = 'Order-Sale', style = 'bt.TButton',command = DirectSale,
                        image = direct_img, compound = 'left')

admin_btn = ttk.Button(left_frame, text = "Admin Panel", command = admin, image = admin_img, compound = 'left', style = 'bt.TButton')

view_bill_btn = ttk.Button(left_frame, text = "View Bill", image = bill_img, compound = 'left', style = 'bt.TButton',
                           command = view_bill.add)

pending_btn = ttk.Button(left_frame, text = "Cash Pending", style = 'bt.TButton', image = pending_img, compound = 'left',
                         command = func_pending)
return_btn = ttk.Button(left_frame, text = 'Return Bill', style = 'bt.TButton', image = return_img, compound = 'left',
                        command = return_bill_func)

discount_btn = ttk.Button(left_frame, text = "Discount", style = "bt.TButton", image = discount_img, compound = 'left',
                          command = discount.add)


backup_btn = ttk.Button(left_frame, text = "BackUp", style= "bt.TButton", image = dropbox_img, compound = 'left', command = make_backup)

copywrite = Label(left_frame, text = "Copyright: New Ghanchi steels",  background ='#fffcf1', font = 'helvetica 8 italic')


#placing
left_frame.configure(padding = 5)
new_entry_btn.pack(fill = X, ipady = 2)
order_sale.pack(fill = X, ipady = 2)
view_bill_btn.pack(fill = X, ipady = 2)
discount_btn.pack(fill = X, ipady = 2)
pending_btn.pack(fill = X, ipady = 2)
return_btn.pack(fill = X, ipady = 2)
admin_btn.pack(fill = X, ipady = 2)
backup_btn.pack(fill = X, ipady = 2)
copywrite.pack(side = 'bottom')


new_entry_click()
splash_end_time = time.time()
splash_total_time = splash_end_time - splash_start_time
reappear(splash_total_time)
main_window.mainloop()

