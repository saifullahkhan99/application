from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from database import Database as db
import subprocess, shutil
import datetime,os
from pdf import call_printer,edit_pdf,AdminBill,Printer

data = db('Data/database/database.db')
items_codes_dict = {}
items_original_dict = {}

dt = datetime.datetime.now()
current_date = dt.date().strftime("%B %d, %Y")
current_time = dt.time().strftime("%I:%M")


#todo class for creating new Entry row----------------------------------------------------------------------------------------------------------------------------------------->

class Entry_object:
    obj_count = 0
    def __init__(self,frame,):
        self.frame = frame
        Entry_object.obj_count +=1
        self.obj_count = Entry_object.obj_count

        self.var_num = IntVar()
        self.var_code = IntVar()
        self.var_desc = StringVar()
        self.var_weight = DoubleVar()
        self.var_cost = DoubleVar()
        self.var_amount = DoubleVar()
        self.var_num.set(self.obj_count)


        self.num_entry1 = Entry(self.frame, textvariable=self.var_num,borderwidth = 0, width = 4,
                                               justify = CENTER, font = "Arial  11", state='readonly')
        self.code_entry1 = Entry(self.frame, textvariable=self.var_code, justify = CENTER, font = "Arial  11",width = 3,
                                 borderwidth = 0,)
        self.description_entry1 = Entry(self.frame,state='readonly',borderwidth = 0,
                                                   justify=CENTER, textvariable=self.var_desc, font = "Arial  11",)
        self.cost_entry1 = Entry(self.frame, textvariable=self.var_cost, justify=CENTER, font = "Arial 11",
                                borderwidth = 0,width = 3)
        self.weight_entry1 =Entry(self.frame, textvariable=self.var_weight, justify = CENTER, font = "Arial  11",
                                borderwidth = 0,width = 3)

        self.amount_entry1 = Entry(self.frame, state='readonly', textvariable=self.var_amount,borderwidth = 0,width =3,
                                                     justify = CENTER, font = "Arial 11",)



        cols = [self.num_entry1,self.code_entry1,self.description_entry1,self.cost_entry1,self.weight_entry1,self.amount_entry1]

        for y in cols:
            if self.obj_count%2 != 0:
                y.configure(background = '#fff2b6', readonlybackground = '#fff2b6')
            else:
                y.configure(background='white', readonlybackground='white')

        def focus_in(event):
            current_wid = event.widget
            for j in cols:
                if j == current_wid:
                        if self.obj_count%2 !=0:
                            current_wid.configure(background = '#fffbe9')
                        else:
                            current_wid.configure(background='#dadde5')

        def focus_out(event):
            current_wid = event.widget
            for j in cols:
                if j == current_wid:
                    if self.obj_count % 2 != 0:
                        current_wid.configure(background='#fff2b6')
                    else:
                        current_wid.configure(background='white')

        for curr_foc in cols:
            curr_foc.bind("<FocusIn>",focus_in)
            curr_foc.bind("<FocusOut>",focus_out)






    def add(self):
        self.num_entry1.grid(row=self.obj_count, column=5, sticky=E, ipady=10, ipadx = 1)
        self.code_entry1.grid(row=self.obj_count, column=6,sticky=EW, ipady=10)
        self.description_entry1.grid(row=self.obj_count, column=7, columnspan=2, sticky=EW, ipady=10)
        self.cost_entry1.grid(row=self.obj_count, column=9, sticky=EW, ipady=10)
        self.weight_entry1.grid(row=self.obj_count, column=10, sticky=EW, ipady=10)
        self.amount_entry1.grid(row=self.obj_count, column=11, sticky=EW, ipady=10)


    def next_forget(self):
        self.num_entry1.grid_forget()
        self.code_entry1.grid_forget()
        self.description_entry1.grid_forget()
        self.cost_entry1.grid_forget()
        self.weight_entry1.grid_forget()
        self.amount_entry1.grid_forget()

#---------------------------------------------------------------------------------------------------------------------->






#todo class for creating customer information field --------------------------------------------------------------------------------------------------------------------------->

class CustomerInfo:
    def __init__(self,frame,var_name, var_phone, var_bill_no,p_var,var_addr):
        self.frame = frame
        self.var_name = var_name
        self.var_phone = var_phone
        self.var_bill_no = var_bill_no
        self.partner_var = p_var
        self.var_addr = var_addr


        self.name_label = Label(self.frame, text = "Name: ", bg = '#fffcf1')
        self.phone_label = Label(self.frame, text = "Phone: ", bg = '#fffcf1')
        self.addr_label = Label(self.frame, text = "Address: ", bg = '#fffcf1')
        self.bill_no_label = Label(self.frame, text = "Bill No:", bg = '#fffcf1')

        self.name_entry = ttk.Entry(self.frame, textvariable = self.var_name)
        self.phone_entry = ttk.Entry(self.frame, textvariable = self.var_phone)
        self.bill_no_entry = Entry(self.frame, textvariable = self.var_bill_no, width= 10, state = 'readonly',
                                       justify = CENTER, readonlybackground = '#fffcf1')
        self.addr_entry = ttk.Entry(self.frame, textvariable = self.var_addr)

        self.or_label = Label(self.frame, text = "OR", font = "Arial 14 italic underline", fg = 'blue')
        self.b_partner_btn = Button(self.frame, text = "Business Partner >>", width =15, fg = "blue", relief = 'flat', cursor = "hand2", bg = '#fffcf1')
        self.b_partner_label = Label(self.frame, text = "Enter Partner ID:", bg = '#fffcf1')
        self.p_id_entry = Entry(self.frame, width = 10, justify= CENTER, textvariable = self.partner_var)
        self.p_info_back = Button(self.frame, text = "<< Go Back", fg = "blue", relief = 'flat', cursor = "hand2", bg = '#fffcf1')
        self.p_name = Label(self.frame, width = 6, bg = '#fffcf1')
        self.p_phone = Label(self.frame, width= 6, bg = '#fffcf1')


        self.var_p_name = StringVar()
        self.var_p_phone = StringVar()
        self.p_name_show = Label(self.frame,width = 20, textvariable = self.var_p_name, font="Courier 12", anchor = W, bg = '#fffcf1')
        self.p_phone_show = Label(self.frame,width = 20, textvariable = self.var_p_phone, font="Courier 12", anchor = W, bg = '#fffcf1')
    def add(self):
        self.frame.configure(width = 450, text = "Customer Info")
        self.b_partner_btn.grid_forget()
        self.p_id_entry.grid_forget()
        self.or_label.grid_forget()
        self.b_partner_label.grid_forget()
        self.p_info_back.grid_forget()
        self.p_name.grid_forget()
        self.p_name_show.grid_forget()
        self.p_phone.grid_forget()
        self.p_phone_show.grid_forget()
        self.name_label.grid(row = 1, column =0, padx = 5)
        self.name_entry.grid(row = 1, column = 1, ipady =3,ipadx =20, sticky = EW, pady = 5, padx = 5)
        self.phone_label.grid(row = 2, column =0, padx = 5)
        self.phone_entry.grid(row = 2, column =1, ipady =3, ipadx = 10, sticky = EW, pady =5, padx  =5)
        self.bill_no_label.place(relx = 0.73, rely = -0.05)
        self.bill_no_entry.place(relx = 0.85, rely = -0.05, height = 26)
        # self.or_label.grid(row = 3, column = 5)
        self.b_partner_btn.place(relx = 0.65, rely = 0.7)

        self.addr_label.grid(row = 3, column = 0)
        self.addr_entry.grid(row = 3, column = 1, ipady = 3, ipadx = 10, sticky = EW, pady = 5, padx = 5)

    def b_parter(self):
        self.name_label.grid_forget()
        self.name_entry.grid_forget()
        self.phone_entry.grid_forget()
        self.phone_label.grid_forget()
        self.b_partner_btn.grid_forget()
        self.or_label.grid_forget()
        self.b_partner_btn.place_forget()
        self.addr_label.grid_forget()
        self.addr_entry.grid_forget()

        self.b_partner_label.grid(row = 0, column = 0 , padx = 22)
        self.frame.configure(width= 450, text = "Business Partner")
        self.p_id_entry.grid(row = 1, column = 0, ipady = 5, pady = 3)
        self.p_info_back.grid(row = 3, column = 0, sticky = W)

        self.p_name.grid(row = 2, column = 2)
        self.p_name_show.grid(row = 2, column = 3, columnspan = 2)
        self.p_phone.grid(row = 3, column = 2)
        self.p_phone_show.grid(row = 3, column = 3, columnspan = 2)





#---------------------------------------------------------------------------------------------------------------------->







#todo class for validating new entries ---------------------------------------------------------------------------------------------------------------------------------------->

class NewEntryFilter:
    def __init__(self,var1,var2,var3):
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def validate(self, ls):
        try:
            self.x = (self.var1,self.var2,self.var3)
        except TclError:
            pass
        else:
            ls.append(self.x)

#---------------------------------------------------------------------------------------------------------------------->







#todo class for edit button behavior ------------------------------------------------------------------------------------------------------------------------------------------>

class TickEdit:

    def __init__(self,fr,lb,tick_img,cross_img):
        self.fr  = fr
        self.lb = lb
        self.tick_img = tick_img
        self.cross_img = cross_img

    def HoverEnter(self,event):
        self.lb.configure(image = self.cross_img, text = "",relief = 'flat')

    def HoverLeave(self,event):
        self.lb.configure(image = self.tick_img, relief = 'flat', text = "")

#---------------------------------------------------------------------------------------------------------------------->







#todo class for validating new entries further -------------------------------------------------------------------------------------------------------------------------------->

class NewEntryValidation:

    row_counter = 0

    def __init__(self,DataList,weight,cost, **kwargs):
        self.orignal_cost = cost
        self.orignal_weight = weight
        self.var_code = kwargs['var_code']
        self.var_cost = kwargs['var_cost']
        self.var_weight = kwargs['var_weight']
        self.fr = kwargs['fr']
        self.obj = kwargs['obj']
        self.done_label = kwargs['done_label']
        self.ind = kwargs['ind']
        self.code_entry = kwargs['code_entry']
        self.cost_entry = kwargs['cost_entry']
        self.weight_entry = kwargs['weight_entry']
        self.description_var = kwargs['desc_var']
        self.amount_var = kwargs['amount_var']
        self.row = kwargs['row']


        self.DataList = DataList
        NewEntryValidation.row_counter +=1
        self.row_counter = NewEntryValidation.row_counter



    def validate(self,event):

        try:
            self.en = (self.var_code.get(), self.var_cost.get(), self.var_weight.get())
            self.amount_var.get()
        except TclError:
            messagebox.showerror("Error","Fill all entries correctly...",)
        else:
            try:
                self.obj.add()
            except AttributeError:
                messagebox.showerror("Error", "Can not add more entries")

    def FocOutWeight(self,event,):
        try:
            if self.var_code.get() not in data.items_codes_list():
                return False
        except TclError:
            return False

        try:
            avg_cost = data.Code_focus_Original()[self.var_code.get()]['cost']
            en1 = (self.var_code.get(), self.var_cost.get(), self.var_weight.get(),)
            if len(str(self.var_code.get())) != 4:
                raise Warning
            # elif self.var_cost.get()< avg_cost:
            #     return False
            try:
                if self.orignal_cost.get() < 0 or self.orignal_cost.get() == '':
                    messagebox.showerror("Cost", "Insert original cost for direct sale")
                    return False
            except TclError:
                messagebox.showerror("Cost", "Insert original cost for direct sale")
                return False


        except TclError:
            return False
        except Warning:
            messagebox.showerror("Code error", "Code must be 4 digit")
        else:

            try:
                self.DataList[self.ind]
            except IndexError:

                self.cost_entry.configure(state="readonly")
                self.code_entry.configure(state="readonly")
                self.weight_entry.configure(state="readonly")
                self.amount_var.set(float(f"%.2f"%(self.var_cost.get()*self.var_weight.get())))
                self.done_label.grid(row=self.row, column=12,)
                # self.fr.grid_columnconfigure(12, weight=1)
                self.tup = (float(f"%.2f"%self.amount_var.get()),)
                self.data = en1 + self.tup + (self.orignal_cost.get(),)

                self.DataList.insert(self.ind, self.data)




            else:
                if self.DataList[self.ind] == ("",):
                    self.DataList.pop(self.ind)
                    self.amount_var.set(self.var_cost.get() * self.var_weight.get())
                    self.tup = (float(f"%.2f" % self.amount_var.get()),)
                    self.data = en1 + self.tup + (self.orignal_cost.get(),)
                    self.DataList.insert(self.ind, self.data)
                    self.cost_entry.configure(state="readonly")
                    self.code_entry.configure(state="readonly")
                    self.weight_entry.configure(state="readonly")
                    self.done_label.grid(row=self.row, column=12)
                    # self.fr.grid_columnconfigure(12, weight=1)

    def FocOutCode(self,event):
        codes_orig = data.Code_focus_Original()
        codes_ls = data.items_codes_list()
        try:

          if len(str(self.var_code.get())) != 4:
             raise Warning

        except TclError:
            messagebox.showerror("Code Error", "Please Enter code number")
        except Warning:
            messagebox.showerror("Code Error", "Code should be 4 digit")
        else:
            if self.var_code.get() not in codes_ls:
                self.description_var.set("No such items")
                pass
            else:
                self.orignal_cost.set(f"%.2f"%codes_orig[self.var_code.get()]['cost'])
                self.orignal_weight.set(f"%.2f"%codes_orig[self.var_code.get()]['weight'])
                self.description_var.set(codes_ls[self.var_code.get()]['company'] + " Steels Grade-60 " + codes_ls[self.var_code.get()]['name'].replace(" ", ""))
                if codes_ls[self.var_code.get()]['company'].lower() == 'commercial':
                    self.description_var.set(
                        codes_ls[self.var_code.get()]['company'] + " Steels " + codes_ls[self.var_code.get()][
                            'name'].replace(" ", ""))
                elif codes_ls[self.var_code.get()]['company'].lower() == 'binding wire':
                    self.description_var.set(codes_ls[self.var_code.get()]['company'])
                elif codes_ls[self.var_code.get()]['company'].lower() == 'loading-unloading':
                    self.description_var.set(codes_ls[self.var_code.get()]['company'])
                
                elif codes_ls[self.var_code.get()]['company'].lower() == 'transportation':
                    self.description_var.set(codes_ls[self.var_code.get()]['company'])

    def FocusCostOut(self,event):
        try:
            avg_cost = data.Code_focus_Original()[self.var_code.get()]['cost']
            if self.var_cost.get()< self.orignal_cost.get():
                raise Warning
        except Warning:
            messagebox.showerror("Cost Error", "Cost is Less than the original cost")
        except TclError:
            pass





#---------------------------------------------------------------------------------------------------------------------->








#todo class for Edit Button when clicked -------------------------------------------------------------------------------------------------------------------------------------->

class EditClicked:
    def __init__(self,ls,ind,**kwargs):

        self.ls = ls
        self.ind = ind
        self.var_code = kwargs['var_code']
        self.var_cost = kwargs['var_cost']
        self.var_weight = kwargs['var_weight']
        self.desc_var = kwargs['desc_var']
        self.amount_var = kwargs['amount_var']
        self.lb = kwargs['lb']
        self.code_entry = kwargs['code_entry']
        self.cost_entry = kwargs['cost_entry']
        self.weight_entry = kwargs['weight_entry']


    def clicked(self,event):
        self.var_code.set("")
        self.var_cost.set("")
        self.var_weight.set("")
        self.desc_var.set("")
        self.amount_var.set("")
        self.lb.grid_forget()
        self.code_entry.configure(state = "normal")
        self.cost_entry.configure(state = "normal")
        self.weight_entry.configure(state = "normal")
        self.ls.pop(self.ind)
        self.ls.insert(self.ind,("",))


#---------------------------------------------------------------------------------------------------------------------->






#todo two fields--------------------------------------------------------------------------------------------------------------------------------------------------------------->
class TwoFields:
    def __init__(self,fr):
        self.frame = fr
        self.s = ttk.Style()
        self.var_cost = DoubleVar()
        self.var_weight = DoubleVar()
        self.s.configure("t.TFrame",background = "#e8e8e8",)
        self.bottom_field = Frame(self.frame,relief = 'raised', height = 130, background = '#e8e8e8', borderwidth = 5)

        self.weight_label = Label(self.bottom_field, text = 'weight', background = '#e8e8e8')
        self.weight_value = Entry(self.bottom_field, width = 18, readonlybackground = 'white',borderwidth = 4, state = 'readonly',
                                  textvariable = self.var_weight, justify = 'center')

        self.cost_label = Label(self.bottom_field, text = 'Cost', background = '#e8e8e8')
        self.cost_value = Entry(self.bottom_field, width = 18, readonlybackground = 'white',borderwidth = 4, state = 'readonly',
                                textvariable = self.var_cost, justify = 'center')



        self.var_current_date = StringVar()
        self.date_field = Entry(self.bottom_field, width = 22, justify = 'center', textvariable = self.var_current_date)
        
        # self.current_date = Label(self.bottom_field,textvariable = self.var_current_date, background = '#e8e8e8')
    def add(self):
        self.bottom_field.pack(side = LEFT, fill = X,expand = True, pady = 5,padx = 25)
        # self.current_date.place(relx = 0.01, rely = 0.8)
        self.date_field.place(relx=0.01, rely = 0.74, height = 26)

        self.weight_label.place(relx = 0.65, rely = 0.1)
        self.weight_value.place(relx = 0.62, rely = 0.35,height= 35)

        self.cost_label.place(relx = 0.78, rely = 0.1)
        self.cost_value.place(relx = 0.75, rely = 0.35, height = 35)


#---------------------------------------------------------------------------------------------------------------------->







#todo processing window------------------------------------------------------------------------------------------------------------------------------------------------------->

class proceeing_window():
    def __init__(self,fr):

        self.main_frame = fr
        self.conf_top_frame = Frame(self.main_frame, height=120, bg="#F8ECC2")
        self.conf_top_frame.grid_columnconfigure(0, pad=20)

        self.conf_desc_frame = Frame(self.main_frame,bg="#F8ECC2")
        self.conf_desc_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),pad= 3)
        self.conf_desc_frame.grid_columnconfigure((1,2,3,4), pad = 2, weight = 1)

        self.conf_cash_frame = Frame(self.main_frame,bg="#F8ECC2",height = 150)


        self.conf_top_frame.grid_propagate(False)
        self.conf_cash_frame.grid_propagate(False)
        self.conf_desc_frame.grid_propagate(False)


        self.var_cust_name = StringVar()
        self.var_cust_phone = StringVar()
        self.var_bp_id = IntVar()

        self.cust_name_label = Label(self.conf_top_frame, text="Name:", anchor=S, bg="#F8ECC2", font="Courier 14")
        self.cust_name = Label(self.conf_top_frame, anchor=S, bg="#F8ECC2", font="Courier 12",
                               textvariable = self.var_cust_name)

        self.cust_phone_label = Label(self.conf_top_frame, text="Phone:", bg="#F8ECC2", anchor=N, font="Courier 14")
        self.cust_phone = Label(self.conf_top_frame, anchor=N, bg="#F8ECC2", font="Courier 12",
                                textvariable=self.var_cust_phone)

        self.bp_id_label = Label(self.conf_top_frame, text="Bill No:", bg="#F8ECC2", font="Courier 14")
        self.bp_id = Label(self.conf_top_frame, textvariable = self.var_bp_id, font="Courier 12",
                           bg = '#F8ECC2')


        self.item_label = Label(self.conf_desc_frame, text = "Item(s)", bg="#F8ECC2", font="Courier  12")
        self.cost_label = Label(self.conf_desc_frame, text = "Cost(Kg)",  bg="#F8ECC2", font="Courier  12",)
        self.weight_label= Label(self.conf_desc_frame, text = "Weight(Kg)",  bg="#F8ECC2", font="Courier  12",)
        self.amount_label = Label(self.conf_desc_frame, text = "Amount", bg="#F8ECC2", font="Courier  12")
        self.sn = Label(self.conf_desc_frame, text = "#SN", bg="#F8ECC2", font="Courier  12", width = 2)

        self.label_sep = ttk.Separator(self.conf_desc_frame, orient = HORIZONTAL)
        self.cash_sep = ttk.Separator(self.conf_desc_frame, orient = HORIZONTAL)


        self.total_var = DoubleVar()

        self.total_name_label = Label(self.conf_cash_frame, bg="#F8ECC2", font="Courier 12 bold")
        self.total_value_label = Label(self.conf_cash_frame, bg="#F8ECC2", font="Courier 12 ",
                                       textvariable = self.total_var)



        self.var_paid = StringVar()
        self.paid_label = Label(self.conf_cash_frame, bg="#F8ECC2", font="Courier 12 bold")
        self.paid_entry = ttk.Entry(self.conf_cash_frame, width = 15,
                                textvariable = self.var_paid, justify = 'center')


        self.var_balance = DoubleVar()
        self.balance_due_label = Label(self.conf_cash_frame,bg="#F8ECC2", font="Courier 12 bold")
        self.balance_due_value = Label(self.conf_cash_frame, text = "",bg="#F8ECC2", font="Courier 12",
                                       textvariable = self.var_balance)

        self.print_btn = ttk.Button(self.conf_cash_frame, text = "Submit & Print")
        self.go_back_btn = ttk.Button(self.conf_cash_frame, text = "<<Back")

        self.prev_label = Label(self.conf_top_frame, text = 'Previewe',bg="#F8ECC2", font="Courier 22 underline bold", fg = '#f6546a')


    def add(self):
        self.prev_label.place(relx = 0.4, rely = 0.01)

        self.conf_top_frame.pack(fill=X, side=TOP)
        self.conf_desc_frame.pack(side=TOP, fill=BOTH,expand = True)
        self.conf_cash_frame.pack(side=BOTTOM, fill= X)


        self.cust_name_label.place(relx = 0.02, rely = 0.4)
        self.cust_name.place(relx = 0.11, rely = 0.4)

        self.cust_phone_label.place(relx = 0.02, rely = 0.559)
        self.cust_phone.place(relx = 0.11, rely = 0.559)

        self.bp_id_label.place(relx=.8, rely = .01)
        self.bp_id.place(relx = 0.95,rely = 0.02)

        self.sn.grid(row = 0, column = 0)
        self.item_label.grid(row = 0, column = 1)
        self.cost_label.grid(row = 0, column = 2, ipadx = 10, sticky = EW)
        self.weight_label.grid(row = 0, column = 3, ipadx = 18, sticky = EW)
        self.amount_label.grid(row = 0, column = 4)

        self.label_sep.place(y = 40, relwidth = 500)
        self.cash_sep.place(rely = .99, relwidth=500)


        self.total_name_label.place(relx = 0.4,rely = 0.05)
        self.total_value_label.place(relx = 0.6, rely = 0.05)

        self.print_btn.place(relx = 0.86,rely = 0.75)
        self.go_back_btn.place(relx = 0.01,rely = 0.75)


    def forget(self):
        self.conf_top_frame.pack_forget()
        self.conf_desc_frame.pack_forget()
        self.conf_cash_frame.pack_forget()

    def desc_forget(self):
        var = self.conf_desc_frame.grid_slaves()
        for x in var:
            x.grid_forget()










class View_Bill:
    def __init__(self,fr):
        self.var_code = IntVar()
        self.frame = fr
        self.var_radio = IntVar()

        try:
            img = Image.open('Data/pics/cancel.png')
            img.thumbnail((30, 20))
            canc_img = ImageTk.PhotoImage(img)

        except FileNotFoundError:
            canc_img = ""

        self.view_frame = Frame(fr, width = 250, height = 300, relief = 'raised', borderwidth = 3)
        self.msg = Label(self.view_frame, text = "Customer's Bill", font="arial 16 underline bold",fg = '#f6546a')
        self.cancel = Label(self.view_frame, image = canc_img)

        self.cancel.image = canc_img
        self.cancel.bind("<Enter>",lambda event: self.cancel.configure(bg = '#f6546a', cursor = 'hand2',))
        self.cancel.bind("<Leave>",lambda event: self.cancel.configure(bg = 'SystemButtonFace',cursor = 'hand2'))

        self.code_label = Label(self.view_frame, text = 'Enter Bill No:', background = 'SystemButtonFace')
        self.code_value = ttk.Entry(self.view_frame, width = 10, textvariable = self.var_code, justify = 'center')
        self.code_err = Label(self.view_frame, text = '', anchor = 'center',
                              font = 'Arial 15 bold italic')

        self.bill_show_btn = ttk.Button(self.view_frame, text = 'Show Bill',)
        self.bill_print_btn = ttk.Button(self.view_frame, text = "Print Bill")

        self.bill_show_btn.bind("<ButtonPress>", self.ShowBill)
        self.bill_print_btn.bind("<ButtonPress>", self.PrintBill)




    def add(self,):
        x = self.frame.place_slaves()
        for j in x:
            j.place_forget()

        self.var_code.set("")
        self.view_frame.place(relx = 0.01, rely = 0.2)


        def cancel_func(event):
            self.view_frame.place_forget()

        self.cancel.bind("<ButtonPress>",cancel_func)




        self.cancel.place(relx = 0.9, rely = 0)
        self.view_frame.pack_propagate(False)
        self.msg.pack(side = 'top',)


        self.r1 = ttk.Radiobutton(self.view_frame, text = 'admin', value = 1, variable = self.var_radio)
        self.r2 = ttk.Radiobutton(self.view_frame, text = 'Customer', value = 2, variable = self.var_radio)
        self.r1.place(relx = 0.57, rely = 0.4)
        self.r2.place(relx = 0.57, rely = 0.47)
        self.code_label.place(relx = 0.07, rely = 0.3)
        self.code_value.place(relx = 0.1, rely = 0.4, height = 35)

        self.bill_show_btn.place(relx = 0.45, rely = 0.75)
        self.bill_print_btn.place(relx = 0.45, rely = 0.85)

        self.code_err.pack(side = BOTTOM, fill = X, pady = 5, padx = 5)



    def ShowBill(self,event):
        datas = data.retrieve_bill(self.var_code.get())

        if self.var_radio.get() == 1:
            try:
                datas = data.retrieve_bill(self.var_code.get())
                tx = datetime.datetime.today().time().strftime("%H:%M:%S")
                AdminBill(datas,tx,False)

            except EXCEPTION:
                messagebox.showerror("close","Please close the pdf reader")
                return False

        elif self.var_radio.get() == 2:
            path = data.ShowBillPath(self.var_code.get())
            try:
                if path == False:
                    return 'break'
                file_chk = os.path.isfile(path)
                
                tx = datetime.datetime.today().time().strftime("%H:%M:%S")
                Printer(datas,tx,False)
                subprocess.Popen([f'{path}'], shell=True)
            except EXCEPTION as e:
                pass

        return 'break'


    def PrintBill(self,event):
        datas = data.retrieve_bill(self.var_code.get())
        tx = datetime.datetime.today().time().strftime("%H:%M:%S")
        if self.var_radio.get() == 1:
            try:
                AdminBill(datas,tx,True)

            except EXCEPTION:
                messagebox.showerror("close", "Please close the pdf reader")
                return False

        elif self.var_radio.get() == 2:
            path = data.ShowBillPath(self.var_code.get())
            if path == False:
                return 'break'
            file_chk = os.path.isfile(path)
            if file_chk == True:
                call_printer(path)
            else:
                Printer(datas, tx, False)
                call_printer(path)
        return 'break'





#todo Return Bill---------------------------------------------------->

class ReturnBill:
    def __init__(self,fr):
        #variables............>
        self.var_id = IntVar()
        self.var_name = StringVar()
        self.var_phone = StringVar()
        self.var_amount = StringVar()
        self.var_paid = StringVar()
        self.var_due = StringVar()
        self.var_date = StringVar()
        self.password = StringVar()

        main_window_width = fr.winfo_screenwidth() - 100
        main_window_height = fr.winfo_screenheight() - 100
        splash_width = main_window_width / 2 - 280
        splash_height = main_window_height / 2 - 250

        self.return_top = Toplevel(fr)
        self.return_top.geometry("600x500+%d+%d"%(splash_width,splash_height))
        self.return_top.configure(bg = '#a8c8d4')
        self.return_top.title("Bill Cancellation")
        self.return_msg = Label(self.return_top, text = 'Bill Cancellation', font = "arial 24 bold underline", bg = '#a8c8d4')

        self.bill_id = Label(self.return_top, text = 'Bill Id: ', font = 'arial 15', justify = 'center', bg = '#a8c8d4')
        self.bill_value = ttk.Entry(self.return_top, width = 15, textvariable = self.var_id, justify = 'center')
        self.press_enter = Label(self.return_top, text='(Press Enter to continue)', font='helvetica 8 italic', bg = '#a8c8d4')


        # Bill informations after entering bill id
        self.bill_name_label = Label(self.return_top, text = 'Name: ', font = 'arial 12', bg = '#a8c8d4')
        self.bill_name_value = Label(self.return_top, text = 'name goes here', font = 'helvetica 11 bold italic', bg = '#a8c8d4',
                                     textvariable = self.var_name)

        self.bill_phone_label = Label(self.return_top, text = 'Phone: ', font = 'arial 12', bg = '#a8c8d4')
        self.bill_phone_value = Label(self.return_top, text = 'phone goes here', font = 'helvetica 11 bold italic', bg = '#a8c8d4',
                                      textvariable = self.var_phone)

        self.bill_amount_label = Label(self.return_top, text = "Amount: ", font = 'arial 12', bg = '#a8c8d4')
        self.bill_amount_value = Label(self.return_top, font = 'helvetica 11 bold italic', bg = '#a8c8d4',
                                       textvariable = self.var_amount)

        self.bill_paid_label = Label(self.return_top, text = "Paid: ", font = 'arial 12', bg = '#a8c8d4')
        self.bill_paid_value = Label(self.return_top, font = 'helvetica 11 bold italic', bg = '#a8c8d4',
                                     textvariable = self.var_paid)

        self.bill_due_label = Label(self.return_top, text = 'Due: ', font = 'arial 12', bg = '#a8c8d4')
        self.bill_due_value = Label(self.return_top, font = 'helvetica 11 bold italic', bg = '#a8c8d4',
                                    textvariable = self.var_due)

        self.bill_date_label = Label(self.return_top, text = "Date: ", font = "arial 12", bg = '#a8c8d4')
        self.bill_date_value = Label(self.return_top, font = "helvetida 11 bold italic",bg = '#a8c8d4',
                                     textvariable = self.var_date)

        self.cause_label = Label(self.return_top, text = "Cause:", font = "arial 15", bg = '#a8c8d4')
        self.cause_value = Text(self.return_top, width = 35, height = 5,)
        self.canc_btn = Button(self.return_top, text = 'Cancel Bill', width = 15,cursor = 'hand2')

        self.err = Label(self.return_top, bg = '#a8c8d4', justify = 'center', font = "arial 14 italic")
        self.err.pack(side = 'bottom', fill= X)



        self.bill_value.bind("<Return>", self.bill_info)
        self.canc_btn.bind("<ButtonPress>", self.CancelBill)


    def add(self):
        self.return_msg.pack()
        self.var_id.set("")
        self.bill_id.place(relx=0.45, rely=0.15)
        self.bill_value.place(relx=0.42, rely=0.21, height = 30)
        self.press_enter.place(relx = 0.58,rely = 0.22)


    def forget(self):
        self.var_id.set("")
        vals = self.return_top.place_slaves()
        rem_not = (self.bill_id,self.bill_value,self.return_msg)
        for x in vals:
            if x not in rem_not:
                x.place_forget()




    def bill_info(self,event):

        if self.var_id.get() not in data.bill_ids():
            self.forget()
            self.err.configure(text = "The Bill Does Not Exists...", bg = 'red')
            return False

        self.bill_name_label.place(relx = 0.15, rely = 0.4)
        self.bill_name_value.place(relx = 0.25, rely = 0.4)

        self.bill_phone_label.place(relx = 0.55, rely = 0.4)
        self.bill_phone_value.place(relx = 0.65, rely = 0.4)

        self.bill_amount_label.place(relx = 0.15, rely = 0.5)
        self.bill_amount_value.place(relx = 0.25, rely = 0.5)

        self.bill_paid_label.place(relx = 0.55, rely = 0.5)
        self.bill_paid_value.place(relx = 0.65, rely = 0.5)

        self.bill_due_label.place(relx = 0.15, rely = 0.6)
        self.bill_due_value.place(relx = 0.25, rely = 0.6)

        self.bill_date_label.place(relx = 0.55, rely = 0.6,)
        self.bill_date_value.place(relx= 0.65, rely = 0.6)

        self.cause_label.place(relx = 0.15, rely = 0.75,)
        self.cause_value.place(relx = 0.3, rely = 0.7)

        self.canc_btn.place(relx = 0.4, rely = 0.88)

        self.err.configure(text = "" , bg = '#a8c8d4')

       #getting bill information
        self.info = data.retrieve_bill(self.var_id.get())

        #setting pdf file path to cancellation folder
        pdf_file_name = self.info[-2].split('\\')[-1]
        canc_path_pre = ".\\Data\\bills\\cancelled"
        self.canc_path = canc_path_pre + f"\\{pdf_file_name}"

        #getting bill information from self.info
        self.bill_no = self.info[0]
        name = self.info[1]
        phone = self.info[2]
        amount = self.info[5]
        paid = self.info[5] - self.info[6]
        date = self.info[4]
        due = self.info[6]


        self.var_name.set(name)
        self.var_phone.set(phone)
        self.var_amount.set(amount)
        self.var_paid.set(paid)
        self.var_due.set(due)
        self.var_date.set(date)

        self.canc_info = list(self.info)
        self.canc_info.pop(-2)
        self.canc_info.insert(-2,self.canc_path)



    #bill cancellation
    def CancelBill(self,event):
        ask = Toplevel(self.return_top)
        main_window_width = ask.winfo_screenwidth() - 100
        main_window_height = ask.winfo_screenheight() - 100
        splash_width = main_window_width / 2 - 160
        splash_height = main_window_height / 2 - 70
        ask.geometry("310x140+%d+%d"%(splash_width,splash_height))
        ask.title("Password")
        ask.iconbitmap("Data/pics/login.ico")

        #on closing password window....
        def dest():
            ask.destroy()
            return False


        #clicking on cancel bill in password window
        def Cancel():

            if self.password.get() != data.admin_login()[1]:
                err.configure(text = 'Wrong Password...', bg = 'red')
                return False
            cause = self.cause_value.get(1.0, END)
            x = data.CancelBill(self.bill_no, self.canc_info, cause, current_date)
            if x != True:
                self.err.configure(text = f"failed to cancell...", bg = 'red')
                return
            shutil.move(self.info[-2], self.canc_path)
            ask.destroy()
            self.err.configure(text = f"bill No: {self.bill_no} has been successfully cancelled", bg = 'green')


            # messagebox.showinfo("Cancelled", f"Successfully Cancelled the bill, #No: {self.bill_no}")
            self.forget()



        #password window widgets and settings
        err = Label(ask, font = "arial 11 italic", justify = 'center')
        pass_label = Label(ask, text = "Password: ", )
        pass_value = ttk.Entry(ask, width = 20, textvariable = self.password, show = '*')
        ask_cancel = Button(ask, text = "Cancel Bill", width = 10, command = Cancel)
        ask_quit = Button(ask, text = "Quit", width = 10, command = dest)

        err.pack(side = 'top', fill = 'x')

        pass_label.place(relx = 0.13, rely = 0.3)
        pass_value.place(relx = 0.37, rely = 0.3, height = 27)

        ask_cancel.place(relx = 0.15, rely = 0.6)
        ask_quit.place(relx = 0.5, rely = 0.6)








#todo CashPending------------------------------------------------------------------------------------------------------------------>


class CashPending:
    def __init__(self,fr):
        self.var_id = IntVar()
        self.var_id.set("")
        self.var_pay = DoubleVar(value = "")

        main_window_width = fr.winfo_screenwidth() - 100
        main_window_height = fr.winfo_screenheight() - 100
        splash_width = main_window_width / 2 - 450
        splash_height = main_window_height / 2 - 250

        self.cash_frame = Toplevel(fr)
        self.cash_frame.geometry("970x500+%d+%d"%(splash_width,splash_height))
        # self.cash_frame.configure(bg='#a8c8d4')
        self.cash_frame.title("Cash Pending")
        self.cash_msg = Label(self.cash_frame, text='Cash Pending', font="arial 24 bold underline", bg='#a8c8d4')

        self.tree = ttk.Treeview(self.cash_frame)
        self.tree['column'] = ("one", "two", "three",'four', 'five','six')
        self.tree.column('#0', width=60, anchor='center')
        self.tree.column('one', width=100, anchor='center')
        self.tree.column('two', width=180, anchor='center')
        self.tree.column('three', width=180, anchor='center')
        self.tree.column('four', width=140, anchor='center')
        self.tree.column('five', width=140, anchor='center')
        self.tree.column('six', width=140, anchor='center')

        self.tree.heading("#0", text="SN", )
        self.tree.heading("one", text="Bill No")
        self.tree.heading("two", text="Name")
        self.tree.heading("three", text="Phone",)
        self.tree.heading("four", text="Amount",)
        self.tree.heading("five", text="Paid",)
        self.tree.heading("six", text="Due",)

        self.tree.pack_propagate(False)
        self.tree.pack()
        self.scr = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scr.set)
        self.scr.pack(side=RIGHT, fill=Y)


        self.id_label = Label(self.cash_frame, text = "ID: ", font = "arial 14")
        self.id_value = ttk.Entry(self.cash_frame, width = 10, stat = 'readonly', justify = 'center',
                                  textvariable = self.var_id)

        self.pay_label = Label(self.cash_frame, text = "Pay: ", font = "arial 14")
        self.pay_value = ttk.Entry(self.cash_frame, width = 20, justify = 'center',
                                   textvariable = self.var_pay)

        self.pay_btn = ttk.Button(self.cash_frame, text = "Pay", command = self.pay_func,
                                  stat = 'disabled')
        self.clear_due_btn = ttk.Button(self.cash_frame, text = "Clear Due", command = self.clear_func,
                                        stat = 'disabled')

        self.err = Label(self.cash_frame, font = "helvetica 14 italic", justify = 'center')
        self.err.pack(side = "bottom", fill = X)


        self.id_label.place(relx = 0.05, rely = 0.5,)
        self.id_value.place(relx = 0.13, rely = 0.5, height = 35)

        self.pay_label.place(relx = 0.05, rely = 0.6)
        self.pay_value.place(relx = 0.13, rely = 0.6, height = 26)

        self.pay_btn.place(relx = 0.13, rely = 0.7)
        self.clear_due_btn.place(relx = 0.85, rely = 0.5)

        data.CashPendingShow(self.tree)
        self.tree.bind("<<TreeviewSelect>>", self.ClickShow)



    def ClickShow(self,event):
        curItem = self.tree.focus()
        item = self.tree.item(curItem)
        self.bill_no = item['values'][0]
        val = data.retriev_bill(self.bill_no)
        self.var_id.set(self.bill_no)
        self.pay_btn.configure(state = 'normal')
        self.clear_due_btn.configure(state = 'normal')
        self.err.configure(text = '', bg = 'SystemButtonFace')

    def selection(self):
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.var_pay.set("")
        self.var_id.set("")
        self.pay_btn.configure(state = 'disabled',)
        self.clear_due_btn.configure(state = 'disabled')
    def pay_func(self):
        tx = datetime.datetime.today().time().strftime("%H:%M:%S")
        try:
            if (data.retriev_bill(self.bill_no)[6])-(data.retriev_bill(self.bill_no)[-1]) - self.var_pay.get() < 0:
                self.err.configure(text = "Payment is more then due...", bg = 'red')
                return False
            rem_due = data.CashPendingPay(self.bill_no,self.var_pay.get())

            if rem_due == 0:
                val = data.retriev_bill(self.bill_no)
                Printer(val,current_date,False)
                self.err.configure(text = "Bill has been successfully cleared", bg = 'green')
                self.tree.delete(*self.tree.get_children())
                data.CashPendingShow(self.tree)
                self.var_pay.set("")
                self.var_id.set("")
                self.selection()

            else:
                self.err.configure(text = "Bill Successfully Updated", bg = 'green')
                self.tree.delete(*self.tree.get_children())
                data.CashPendingShow(self.tree)
                self.selection()
        except EXCEPTION as e:
            self.err.configure(text="Failed: Something went wrong", bg='red')
            print(e)


    def clear_func(self,):
        data.CashPendingClearDue(self.var_id.get())
        self.err.configure(text="Bill has been successfully cleared", bg='green')
        self.tree.delete(*self.tree.get_children())
        data.CashPendingShow(self.tree)
        val = data.retriev_bill(self.bill_no)
        Printer(val, tx, False)
        self.selection()










class AddDiscount:
    def __init__(self,fr):
        self.var_code = IntVar()
        self.var_discount = DoubleVar()
        self.var_name = StringVar()
        self.var_amount = StringVar()
        self.frame = fr

        try:
            img = Image.open('Data/pics/cancel.png')
            img.thumbnail((30, 20))
            canc_img = ImageTk.PhotoImage(img)

        except FileNotFoundError:
            canc_img = ""

        self.discount_frame = Frame(fr, width=350, height=337, relief='raised', borderwidth=3)
        self.msg = Label(self.discount_frame, text="Adding Discount", font="arial 16 underline bold", fg='#f6546a')
        self.cancel = Label(self.discount_frame, image=canc_img)

        self.cancel.image = canc_img
        self.cancel.bind("<Enter>", lambda event: self.cancel.configure(bg='#f6546a', cursor='hand2', ))
        self.cancel.bind("<Leave>", lambda event: self.cancel.configure(bg='SystemButtonFace', cursor='hand2'))

        self.code_label = Label(self.discount_frame, text='Enter Bill No:', background='SystemButtonFace')
        self.code_value = ttk.Entry(self.discount_frame, width=10, textvariable=self.var_code, justify='center')
        self.code_err = Label(self.discount_frame, text='', anchor='center',
                              font='Arial 15 bold italic')

        self.add_disc_label = Label(self.discount_frame, text = "Discount: ", bg = 'SystemButtonFace')
        self.add_disc_value = ttk.Entry(self.discount_frame, width = 15, justify = 'center',
                                        textvariable = self.var_discount, state = 'readonly')




        self.code_value.bind("<Return>",self.Discount_GetBill)
        self.show_var = 0

    def add(self, ):
        x = self.frame.place_slaves()
        for j in x:
            j.place_forget()
        self.var_code.set("")
        self.var_discount.set("")
        self.var_amount.set("")
        self.var_name.set("")
        self.code_err.configure(text = '', bg = 'SystemButtonFace')
        self.add_disc_value.configure(state = 'readonly')
        self.discount_frame.place(relx=0.01, rely=0.1)

        self.bill_name_label = Label(self.discount_frame,font="arial 12 italic", text = 'Name: ')
        self.bill_name_value = Label(self.discount_frame, textvariable=self.var_name, font="helvetica 12 bold")

        self.bill_amount_label = Label(self.discount_frame,font="arial 12 italic", text = "Amount: " )
        self.bill_amount_value = Label(self.discount_frame, textvariable=self.var_amount, font="helvetica 12 bold")

        self.add_discount_btn = ttk.Button(self.discount_frame, text='Add Discount', state='disabled')



        self.cancel.place(relx = 0.9, rely = 0)
        self.discount_frame.pack_propagate(False)
        self.msg.pack(side = 'top',)


        self.code_label.place(relx = .1, rely = 0.26)
        self.code_value.place(relx = 0.38, rely = 0.25, height = 35)

        self.add_disc_label.place(relx = .1, rely = 0.4)
        self.add_disc_value.place(relx = 0.34, rely = 0.4, height = 26)

        self.bill_name_label.place(relx = .2, rely = 0.52)
        self.bill_name_value.place(relx = 0.4, rely = 0.52)

        self.bill_amount_label.place(relx = .2, rely = .61)
        self.bill_amount_value.place(relx = 0.4, rely = 0.61)

        self.add_discount_btn.place(relx = 0.3, rely = 0.75)

        self.code_err.pack(side = BOTTOM, fill = X, pady = 5, padx = 5)

        def cancel_func(event):
            self.discount_frame.place_forget()

        self.cancel.bind("<ButtonPress>", cancel_func)





    def Discount_GetBill(self,event):
        try:
            vals = data.retrieve_bill(self.var_code.get())
            self.code_err.configure(text='', bg='SystemButtonFace')
            if vals == None:
                self.code_err.configure(text = "The bill does not exists...", bg = 'red')
                return False
            self.code_err.configure(text = "", bg = "SystemButtonFace")
            name = vals[1]
            amount = vals[5]

            self.var_name.set(name)
            self.var_amount.set(amount)
            self.add_disc_value.configure(state = 'normal')
            self.add_discount_btn.configure(state = 'normal')
            self.add_discount_btn.bind("<ButtonRelease>", self.AddDicount)
        except TclError:
            self.code_err.configure(text = 'wrong bill id..', bg = 'red')

    def AddDicount(self,event):
        try:
            data.add_discount(self.var_code.get(),self.var_discount.get())
            self.add()
            self.code_err.configure(text = "Discount applied successfully....", bg = 'green')
        except TclError:
            self.code_err.configure(text = "enter some amount", bg = 'red')
        except EXCEPTION:
            self.code_err.configure(text = "something went wrong", bg = 'red')

