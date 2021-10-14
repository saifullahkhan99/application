from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from PIL import Image, ImageOps, ImageDraw,ImageTk
from tkinter import messagebox
from tkinter import filedialog
import datetime
import os
import pdf
from database import Database as db
data = db("Data/database/database.db")

dt = datetime.datetime.now()
current_date = dt.date().strftime("%B %d, %Y")
current_time = dt.time().strftime("%I:%M")




class AdminLeftFrame:
    def __init__(self,frame):
        self.admin_left_frame = Frame(frame, width=180, bg = "white")
        self.admin_left_frame.pack(side=LEFT, fill=Y, padx = 10, pady = 10)
        self.admin_left_frame.pack_propagate(False)

        #buttons
        #admin imaga
        self.add_img = Image.open("Data/pics/admin/personal/current_image.png")
        self.add_img.thumbnail((180, 180))
        self.new_entry_img = ImageTk.PhotoImage(self.add_img)
        self.image_canvas = Canvas(self.admin_left_frame, width = 170, height = 150, bg = 'white')
        self.prof_pic = self.image_canvas.create_image(90, 80, image=self.new_entry_img, anchor='center')



        self.image_canvas.bind("<Enter>", self.show_img_chage)
        self.image_canvas.bind("<Leave>", self.remove_img_chang)
        self.image_canvas.bind("<ButtonRelease>", self.change_admin_pic)


        self.dasboard_btn = Label(self.admin_left_frame, text = "Dashboard", fg = "blue", font = "Arial 12", bg = "white",)
        self.admin_left_itmes_btn = Label(self.admin_left_frame, text = "Items", fg = "blue", font = "Arial 12", bg = "white")
        self.partners_btn = Label(self.admin_left_frame, text = 'Partners', fg = 'blue', font = 'Arial  12', bg = 'white')
        self.settings_btn = Label(self.admin_left_frame, text = 'Settings', fg = 'blue', font = 'Arial 12', bg = 'white')
        self.orders_btn = Label(self.admin_left_frame, text = "Orders", fg = 'blue', font = "arial 12", bg = 'white')
        self.profit_btn = Label(self.admin_left_frame, text = "Profit", fg = 'blue', font = "arial 12", bg = 'white')

    def add(self):
        self.image_canvas.pack(side = 'top', fill = X)
        self.dasboard_btn.pack(side = TOP, fill = X)
        self.dasboard_btn.pack_configure(ipady = 7, pady = 3)
        self.partners_btn.pack(side = TOP, fill = X, ipady = 7)
        self.admin_left_itmes_btn.pack(side = TOP, fill = X, ipady = 7)
        self.orders_btn.pack(side = TOP, fill = X, ipady = 7)
        self.profit_btn.pack(side = TOP, fill = X, ipady = 7)
        self.settings_btn.pack(side = TOP, fill = X, ipady = 7)



        self.dasboard_btn.bind("<Enter>", lambda event: self.dasboard_btn.configure(bg = '#d6d9d9', cursor = "hand2", relief = 'raised',
                                                                                    fg = 'black'))
        self.dasboard_btn.bind("<Leave>", lambda event: self.dasboard_btn.configure(bg = 'white', relief = 'flat',fg = 'blue',))
        self.admin_left_itmes_btn.bind("<Enter>", lambda event: self.admin_left_itmes_btn.configure(bg = '#d6d9d9', cursor = 'hand2', relief = 'raised',
                                                                                                    fg = 'black'))
        self.admin_left_itmes_btn.bind("<Leave>", lambda event: self.admin_left_itmes_btn.configure(bg = 'white', relief = 'flat',fg = 'blue'))

        self.partners_btn.bind("<Enter>",
                                       lambda event: self.partners_btn.configure(bg='#d6d9d9', cursor='hand2', relief = 'raised',
                                                                                 fg = 'black'))
        self.partners_btn.bind("<Leave>", lambda event: self.partners_btn.configure(bg='white', relief = 'flat',fg = 'blue'))


        self.settings_btn.bind("<Enter>", lambda event: self.settings_btn.configure(bg='#d6d9d9', cursor="hand2", relief = 'raised',
                                                                                    fg = 'black'))
        self.settings_btn.bind("<Leave>", lambda event: self.settings_btn.configure(bg='white', relief = 'flat',fg = 'blue'))

        self.orders_btn.bind("<Enter>",
                               lambda event: self.orders_btn.configure(bg='#d6d9d9', cursor="hand2", relief='raised',
                                                                         fg='black'))
        self.orders_btn.bind("<Leave>",
                               lambda event: self.orders_btn.configure(bg='white', relief='flat', fg='blue'))

        self.profit_btn.bind("<Enter>",
                             lambda event: self.profit_btn.configure(bg='#d6d9d9', cursor="hand2", relief='raised',
                                                                     fg='black'))
        self.profit_btn.bind("<Leave>",
                             lambda event: self.profit_btn.configure(bg='white', relief='flat', fg='blue'))




    def show_img_chage(self, event):
        self.image_canvas.configure(cursor='hand2', bg='SystemButtonFace')
        self.rect = self.image_canvas.create_rectangle(10, 123, 170, 150, fill='#dfdfe1')
        self.text = self.image_canvas.create_text(87, 135, text='Change Picture', font='arial 13 underline')

    def remove_img_chang(self, event):
        self.image_canvas.delete(self.rect)
        self.image_canvas.delete(self.text)

    def change_admin_pic(self,event):
        image = filedialog.askopenfile(initialdir = './', title = 'Select Image', filetypes = (("jpeg file","*.jpg"),("png file", "*.png")))
        image_path = image.name

        im = Image.open(image_path)
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        os.remove('./Data/pics/admin/personal/current_image.png')
        output.save('./Data/pics/admin/personal/current_image.png')

        self.image_canvas.delete(self.prof_pic)
        self.add_img = Image.open("Data/pics/admin/personal/current_image.png")
        self.add_img.thumbnail((180, 180))
        self.img = ImageTk.PhotoImage(self.add_img)
        self.canv_image = self.image_canvas.create_image(90, 80, image=self.img, anchor='center')






class AdminTopFrame:
    def __init__(self,frame):
        self.admin_top_frame = Frame(frame, height=80, bg = '#6b238f')
        self.admin_top_frame.pack(side=TOP, fill=X)
        self.message_image = Label(self.admin_top_frame, bg = '#6b238f')
        self.message_label = Label(self.admin_top_frame, bg = '#6b238f')

        self.message_image.place(relx = 0.35, rely = 0.23)
        self.message_label.place(relx = 0.45, rely = 0.38)







class AdminMiddleFrame:
    def __init__(self,frame):
        self.admin_middle_frame = Frame(frame,)
        self.admin_middle_frame.pack(fill=BOTH, expand=True)

    def forget(self):
        its = self.admin_middle_frame.pack_slaves()
        for z in its:
            z.pack_forget()

        its = self.admin_middle_frame.grid_slaves()
        for z in its:
            z.grid_forget()

        its = self.admin_middle_frame.place_slaves()
        for z in its:
            z.place_forget()









#todo ITEMS Button ------------------------------------------------------------------------------------------------------------------------------------------>
class AdminItems:
    def __init__(self, fr):

        #frames
        self.items_frame = Frame(fr, height=40, width=300, bg = "white")
        self.show_frame = Frame(fr, width = 700, height = 400, bg = '#ffffff')


        #buttons
        self.admin_view_items = Label(self.items_frame, text="View", bg = "white", fg = "blue",)
        self.admin_update_items = Label(self.items_frame, text="Updates", bg = "white", fg = "blue")
        self.admin_delete_items = Label(self.items_frame, text="Delete", bg = "white", fg = "blue")
        self.admin_add_items = Label(self.items_frame, text="Add", bg = "white", fg = "blue")
        self.admin_return_item = Label(self.items_frame, text = "Return", bg = 'white',fg = 'blue')
        self.item_message = Label(self.items_frame, image = '')



        #binding events to buttons---------------------->
        self.admin_view_items.bind("<Enter>", lambda event: self.admin_view_items.configure(fg = 'black', cursor = "hand2",font = "arial 11 underline"))
        self.admin_view_items.bind("<Leave>", lambda event: self.admin_view_items.configure(fg = 'blue', cursor = "hand2", font = "arial 11"))
        self.admin_view_items.bind("<ButtonPress>", self.view_items)

        self.admin_update_items.bind("<Enter>", lambda event: self.admin_update_items.configure(fg='black', cursor="hand2",font = "arial 11 underline"))
        self.admin_update_items.bind("<Leave>", lambda event: self.admin_update_items.configure(fg='blue', cursor="hand2", font = "arial 11"))
        self.admin_update_items.bind("<ButtonPress>", self.items_update)


        self.admin_delete_items.bind("<Enter>", lambda event: self.admin_delete_items.configure(fg='black', cursor="hand2", font = "arial 11 underline"))
        self.admin_delete_items.bind("<Leave>", lambda event: self.admin_delete_items.configure(fg='blue', cursor="hand2", font = "arial 11"))
        self.admin_delete_items.bind("<ButtonPress>", self.item_delete)

        self.admin_add_items.bind("<Enter>", lambda event: self.admin_add_items.configure(fg='black', cursor="hand2",font = "arial 11 underline"))
        self.admin_add_items.bind("<Leave>", lambda event: self.admin_add_items.configure(fg='blue', cursor="hand2", font = "arial 11"))
        self.admin_add_items.bind("<ButtonPress>", self.add_item)

        self.admin_return_item.bind("<Enter>", lambda event: self.admin_return_item.configure(fg='black', cursor="hand2",
                                                                                          font="arial 11 underline"))
        self.admin_return_item.bind("<Leave>", lambda event: self.admin_return_item.configure(fg='blue', cursor="hand2",
                                                                                          font="arial 11"))
        self.admin_return_item.bind("<ButtonPress>", self.ReturnItem)





        #changing background color of buttons on click---------------------------------->
        self.bg_current_list = []
        self.bg_list = [self.admin_view_items,self.admin_add_items, self.admin_update_items,
                        self.admin_delete_items,self.admin_return_item]
        for x in self.bg_list:
            x.bind("<ButtonRelease>", self.chang_bg)

    def chang_bg(self,event):
        if len(self.bg_current_list) >=2:
            for i in self.bg_current_list[0:-1]:
                i.configure(bg = 'white')
                self.bg_current_list.remove(i)








    #adding item frame and show frame in admin middle frame------------------------------>
    def add(self):
        self.items_frame.pack_propagate(False)
        self.items_frame.pack(side=TOP, pady=5,)
        self.show_frame.pack(side=TOP, padx=10, pady=5)
        self.admin_view_items.pack(side=LEFT, ipadx = 7, ipady = 6)
        self.admin_add_items.pack(side=LEFT, ipadx = 7, ipady = 6)
        self.admin_update_items.pack(side=LEFT, ipadx = 7, ipady = 6)
        self.admin_delete_items.pack(side=LEFT, ipadx = 7, ipady = 6)
        self.admin_return_item.pack(side = LEFT, ipadx = 7, ipady = 6)




    #forgeting widgets in show frames--------------------------->
    def forget(self):
        x = self.show_frame.place_slaves()
        for i in x:
            i.place_forget()

        y = self.show_frame.pack_slaves()
        for j in y:
            j.pack_forget()

        z = self.show_frame.grid_slaves()

        for m in z:
            m.grid_forget()




    #view items tab------------------------------>
    def view_items(self,event):
        self.admin_view_items.configure(bg = '#9fa59a')
        if self.admin_view_items not in self.bg_current_list:
            self.bg_current_list.append(self.admin_view_items)

        self.tree = ttk.Treeview(self.show_frame)
        self.tree['column'] = ("one", "two", "three")
        self.tree.column('#0', width=60, anchor = 'center')
        self.tree.column('one', width=100, anchor = 'center')
        self.tree.column('two', width=120, anchor = 'center')
        self.tree.column('three', width=180, anchor = 'center')

        self.tree.heading("#0", text="No", )
        self.tree.heading("one", text="Code")
        self.tree.heading("two", text="Size")
        self.tree.heading("three", text="Company")

        self.tree.pack_propagate(False)
        self.scr = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scr.set)
        self.scr.pack(side=RIGHT, fill=Y)

        self.cost_label = Label(self.show_frame, text="Cost:", bg="white", font="Arial 12 bold")
        self.cost_value = Label(self.show_frame, text="", bg="white", font="Arial 12 bold")

        self.weight_label = Label(self.show_frame, text="Weight:", bg="white", font="Arial 12 bold")
        self.weight_value = Label(self.show_frame, text="", bg="white", font="Arial 12 bold")
        self.no_items_label = Label(self.show_frame, text="Total Items:", bg="white")
        self.no_items_values = Label(self.show_frame, text="", bg="white")


        self.current_tab = Label(self.show_frame, text="View Items", bg='white', font='Weight 22 bold underline', fg='#f6546a')
        try:
            set_img = Image.open('Data/pics/admin/views.png')
            set_img.thumbnail((50, 40))
            img = ImageTk.PhotoImage(set_img)
            self.current_img = Label(self.show_frame, image=img, bg='white')
            self.current_img.image = img
        except FileNotFoundError:
            self.current_img = Label(self.show_frame, text='image not found', font='arila 8', bg='white')


        # adding items to show frame----------------------------->

        # self.list_box.pack(side = TOP, pady = 50)
        self.show_frame.pack_propagate(False)
        self.forget()
        self.tree.pack(side=TOP, pady=70)
        # self.cost_label.place(relx=0.3, rely=0.75)
        # self.cost_value.place(relx=0.5, rely=0.75)
        # self.weight_label.place(relx=0.3, rely=0.8)
        # self.weight_value.place(relx=0.5, rely=0.8)

        self.current_tab.place(relx=0.3, rely=0.01)
        self.current_img.place(relx = 0.56, rely = 0.03)

        data.admin_view_items(self.tree)






    #add item tab------------------------------>
    def add_item(self,event):
        self.admin_add_items.configure(bg = '#9fa59a')
        if self.admin_add_items not in self.bg_current_list:
            self.bg_current_list.append(self.admin_add_items)


        self.var_code = IntVar()
        self.var_size = StringVar()
        self.comp = StringVar()
        self.compvar = 0
        self.company_back = 0
        self.combo_var = StringVar()

        self.code_label = Label(self.show_frame, text="Code: ", bg="white")
        self.code_entry = ttk.Entry(self.show_frame, width=15, textvariable=self.var_code, justify=CENTER)

        self.size_label = Label(self.show_frame, text="Size: ", bg="white")
        self.size_entry = ttk.Entry(self.show_frame, width=15, textvariable=self.var_size, justify=CENTER)
        self.size_info = Label(self.show_frame, text="(In mm)", bg="White")

        self.company_list = []
        data.add_new_item_id(self.var_code, self.company_list)

        self.company_label = Label(self.show_frame, text="Company: ", bg="white")
        self.company_combo = ttk.Combobox(self.show_frame, values=self.company_list, width=14, textvariable=self.combo_var)

        if self.company_list:
            self.company_combo.set(self.company_list[0])
        self.add_company_btn = Button(self.show_frame, image="", text="add", )

        self.err = Label(self.show_frame, text='', font='Arial 14 italic', width=50, bg='white')

        self.x = 0

        def submit(event):
            if self.compvar == 0:
                try:
                    self.x = 1
                    code = self.var_code.get()
                    self.x = 2
                    size = self.var_size.get()
                    self.x = 3
                    combo = self.combo_var.get()
                    self.x = 4

                except TclError:
                    if self.x == 1:
                        self.err.configure(text="Failed: Only 4 Digit Code Is Accepted", bg='red')
                        pass

                else:
                    data.add_new_item(self.var_code.get(), self.var_size.get(), self.combo_var.get().title(),
                                   self.err,current_date)
                    data.add_new_item_id(self.var_code, self.company_list)
                    self.var_size.set("")
                    self.combo_var.set(self.company_list[0])
            else:
                try:
                    self.x = 1
                    code = self.var_code.get()
                    self.x = 2
                    size = self.var_size.get()
                    self.x = 3
                    comp = self.comp.get()

                except TclError:
                    if self.x == 1:
                        self.err.configure(text="Failed: Only 4 Digit Code Is Accepted", bg='red')
                        pass

                else:
                    data.add_new_item(self.var_code.get(), self.var_size.get(), self.comp.get().title(),
                                      self.err, current_date)
                    data.add_new_item_id(self.var_code, self.company_list)
                    self.var_size.set("")
                    self.combo_var.set(self.company_list[0])

        self.submit_btn = ttk.Button(self.show_frame, text='Submit', )
        self.submit_btn.bind("<ButtonPress>", submit)

        self.add_company_entry = ttk.Entry(self.show_frame, width=15, textvariable=self.comp)

        self.current_tab = Label(self.show_frame, text="Add New Item", bg='white', font='Weight 22 bold underline', fg='#f6546a')
        try:
            set_img = Image.open('Data/pics/admin/dbadd.png')
            set_img.thumbnail((50, 40))
            img = ImageTk.PhotoImage(set_img)
            self.current_img = Label(self.show_frame, image=img, bg='white')
            self.current_img.image = img
        except FileNotFoundError:
            self.current_img = Label(self.show_frame, text='image not found', font='arila 8', bg='white')



        #adding items to show frame--------------------------->
        self.forget()

        self.code_label.place(relx=0.15, rely=0.32, )
        self.code_entry.place(relx=0.27, rely=0.32, height=25)

        self.size_label.place(relx=0.15, rely=0.42)
        self.size_entry.place(relx=0.27, rely=0.42, height=25)
        self.size_info.place(relx=0.45, rely=0.42)

        self.company_label.place(relx=0.15, rely=0.52)
        self.company_combo.place(relx=0.27, rely=0.52, height=25)
        self.add_company_btn.place(relx=0.45, rely=0.51)

        self.current_tab.place(relx=0.3, rely=0.01)
        self.current_img.place(relx=0.62, rely=0.01)

        self.err.place(relx=0.05, rely=0.92)

        self.submit_btn.place(relx=0.4, rely=0.7)

        def company_func(event):
            if self.company_back == 0:
                self.compvar = 1
                self.company_combo.place_forget()
                self.add_company_entry.place(relx=0.27, rely=0.52, height=25)
                self.add_company_btn.configure(text='<<', fg='blue')
                self.company_back = 1
            else:
                self.compvar = 0
                self.add_company_entry.place_forget()
                self.add_company_btn.configure(text="Add", fg='black')
                self.company_combo.place(relx=0.27, rely=0.52, height=25)
                self.company_back = 0

        self.add_company_btn.bind("<ButtonPress>", company_func)








    #update items tab --------------------------------->
    def items_update(self, event):
        self.admin_update_items.configure(bg = '#9fa59a')
        if self.admin_update_items not in self.bg_current_list:
            self.bg_current_list.append(self.admin_update_items)



        self.var_id = StringVar()

        self.var_name = StringVar()
        self.var_old_cost = StringVar()
        self.var_old_weight = StringVar()

        self.var_add_cost = DoubleVar()
        self.var_add_weight = DoubleVar()

        self.var_add_cost.set("")
        self.var_add_weight.set("")

        self.code_label = Label(self.show_frame, text="Enter Code: ", bg="white")
        self.code_value = ttk.Entry(self.show_frame, width=10, textvariable=self.var_id)


        self.add_cost_label = Label(self.show_frame, text="Add Cost: ", bg="white")
        self.add_cost_value = ttk.Entry(self.show_frame, width=20, textvariable=self.var_add_cost,
                                        state = 'readonly')
        press_enter = Label(self.show_frame, text = '(Press Enter to continue)', font = 'helvetica 8 italic',bg = 'white')

        self.add_wieght_label = Label(self.show_frame, text="Add Weight: ", bg="white")
        self.add_weight_value = ttk.Entry(self.show_frame, width=20, textvariable=self.var_add_weight,
                                          state = 'readonly')

        self.name = Label(self.show_frame, text="", bg='white')
        self.name_value = Label(self.show_frame, bg='white', textvariable=self.var_name)

        self.old_cost_label = Label(self.show_frame, text='', bg='white')
        self.old_cost_value = Label(self.show_frame, bg='white', textvariable=self.var_old_cost)

        self.old_weight_label = Label(self.show_frame, text='', bg='white')
        self.old_weight_value = Label(self.show_frame, bg='white', textvariable=self.var_old_weight)

        self.err = Label(self.show_frame, text='', font='Arial 14 italic', width=50, bg='white')

        self.update_btn = ttk.Button(self.show_frame, text="Update")

        def upd_func(event):
            try:
                self.var_old_cost.set("")
                self.var_old_weight.set("")
                self.var_name.set("")
                self.name.configure(text="")
                self.add_weight_value.configure(state = 'readonly')
                self.add_cost_value.configure(state = 'readonly')
                self.old_weight_label.configure(text='')
                self.old_cost_label.configure(text="")
                self.err.configure(text = '', bg = 'white')

                val  = data.upd_func_values(self.var_id.get())
                if val == None:
                    self.err.configure(text = 'Wrong item id...', bg = 'red')
                    return False
                else:
                    self.name.configure(text="Name: ")
                    self.add_cost_value.configure(state = 'normal')
                    self.add_weight_value.configure(state = 'normal')

                    self.old_weight_label.configure(text = 'Current Weight: ')
                    self.old_cost_label.configure(text = 'Average cost: ')
                    self.var_name.set(val[2] + " " + val[1])
                    self.var_old_cost.set(val[4])
                    self.var_old_weight.set(val[3])
            except EXCEPTION as e:
                print('something went wrong...')



        self.code_value.bind("<Return>", upd_func)

        def update(event):
            done_dict = {}
            if self.var_id.get() == '':
                return False
            else:
                try:
                    cost = self.var_add_cost.get()
                    done_dict['cost'] = cost
                except TclError:
                    done_dict['cost'] = ''
                try:
                    weight = self.var_add_weight.get()
                    done_dict['weight'] = weight
                except TclError:
                    done_dict['weight'] = ''

                if done_dict['cost'] == '' and done_dict['weight'] == '':
                    return False
                else:
                    data.admin_update(done_dict['cost'], done_dict['weight'], int(self.var_id.get()),current_date)
                    self.var_add_weight.set("")
                    self.var_add_cost.set("")
                    self.err.configure(text = "Successfully updated item...", bg = 'green')

        self.update_btn.bind("<ButtonPress>", update)

        self.current_tab = Label(self.show_frame, text="Update Item", bg='white', font='Weight 22 bold underline', fg='#f6546a')

        try:
            set_img = Image.open('Data/pics/admin/validpng.png')
            set_img.thumbnail((50, 40))
            img = ImageTk.PhotoImage(set_img)
            self.current_img = Label(self.show_frame, image=img, bg='white')
            self.current_img.image = img
        except FileNotFoundError:
            self.current_img = Label(self.show_frame, text='image not found', font='arila 8', bg='white')



        #adding items to show frame ----------------------------->
        self.forget()
        self.code_label.place(relx=0.105, rely=0.15, )
        self.code_value.place(relx=0.25, rely=0.15, height=35)
        press_enter.place(relx = 0.37, rely = 0.17)

        self.add_cost_label.place(relx=0.1, rely=0.3)
        self.add_cost_value.place(relx=0.25, rely=0.3, height=25)

        self.add_wieght_label.place(relx=0.1, rely=0.4)
        self.add_weight_value.place(relx=0.25, rely=0.4, height=25)

        self.name.place(relx=0.65, rely=0.2)
        self.name_value.place(relx=0.75, rely=0.2)

        self.old_cost_label.place(relx=0.65, rely=0.3)
        self.old_cost_value.place(relx=0.85, rely=0.3)

        self.old_weight_label.place(relx=0.65, rely=0.4)
        self.old_weight_value.place(relx=0.85, rely=0.4)

        self.update_btn.place(relx=0.23, rely=0.55)

        self.current_tab.place(relx=0.3, rely=0.01)
        self.current_img.place(relx=0.58, rely=0.01)

        self.err.pack(side = 'bottom', fill = X)






    #delete items tab ----------------------------------------------------->
    def item_delete(self,event):
        self.admin_delete_items.configure(bg = '#9fa59a')
        if self.admin_delete_items not in self.bg_current_list:
            self.bg_current_list.append(self.admin_delete_items)



        self.var_code = StringVar()
        self.var_item = StringVar()

        self.code_label = Label(self.show_frame, text="Enter your code: ", bg="white")
        self.code_value = ttk.Entry(self.show_frame, width=10, textvariable=self.var_code)
        press_enter = Label(self.show_frame, text = '(Press Enter to continue)', font = 'helvetica 8 italic',bg = 'white')


        self.item = Label(self.show_frame, bg='white', textvariable=self.var_item)

        self.err = Label(self.show_frame, text='', font='Arial 14 italic', width=50, bg='white')

        self.delete_btn = ttk.Button(self.show_frame, text="Delete")


        def del_show(event):
            try:
                id = int(self.var_code.get())
            except ValueError:
                pass
            else:
                data.delete_items_show(id, self.var_item)

        self.code_value.bind("<Return>", del_show)

        def delete(event):
            try:
                id = int(self.var_code.get())
            except ValueError:
                messagebox.showerror("Code Error", "Wrong Code...",parent = self.show_frame)
                pass
            else:
                data.delete(id, self.err)

        self.delete_btn.bind("<ButtonPress>", delete)

        self.current_tab = Label(self.show_frame, text="Delete Item", bg='white', font='Weight 22 bold underline', fg='#f6546a')
        try:
            set_img = Image.open('Data/pics/admin/del1.png')
            set_img.thumbnail((50, 40))
            img = ImageTk.PhotoImage(set_img)
            self.current_img = Label(self.show_frame, image=img, bg='white')
            self.current_img.image = img
        except FileNotFoundError:
            self.current_img = Label(self.show_frame, text='image not found', font='arial 8', justify=CENTER, bg='white')



        #adding widgets to show frame -------------------------------->
        self.forget()
        self.code_label.place(relx=0.37, rely=0.2)
        self.code_value.place(relx=0.4, rely=0.3, height=35)
        press_enter.place(relx = 0.54,rely = 0.32)

        self.item.place(relx=0.4, rely=0.43)
        self.delete_btn.place(relx=0.35, rely=0.55)

        self.current_tab.place(relx=0.33, rely=0.011)
        self.current_img.place(relx=0.58, rely=0.01)

        self.err.place(relx=0.05, rely=0.92)




    def ReturnItem(self,event):
        self.admin_return_item.configure(bg='#9fa59a')
        if self.admin_return_item not in self.bg_current_list:
            self.bg_current_list.append(self.admin_return_item)

        self.forget()
        var_bill = IntVar()
        var_item = IntVar()
        var_weight = DoubleVar()
        var_item.set("")
        var_weight.set("")
        err = Label(self.show_frame, bg = 'white')
        err.pack(side = 'bottom', fill = X)




        show_label_frame = LabelFrame(self.show_frame, width = 600, height = 280, text = 'Return Item')
        bill_label = Label(show_label_frame, text = 'Bill No: ', font = 'helvetica 12 italic')
        bill_value = ttk.Entry(show_label_frame, width = 10, textvariable = var_bill,justify = 'center')
        press_enter = Label(show_label_frame, text='(Press Enter to continue)', font='helvetica 8 italic',)

        item_labe = Label(show_label_frame,text = 'Item No: ', font = 'helvetica 12 italic')
        item_value = ttk.Entry(show_label_frame, width = 10,state = 'readonly', textvariable = var_item,justify = 'center')

        weight_label = Label(show_label_frame, text = 'Weight: ', font = 'helvetica 12 italic')
        weight_value = ttk.Entry(show_label_frame, width = 10, textvariable = var_weight, justify = 'center', state = 'readonly')

        return_btn = ttk.Button(show_label_frame, text = 'Return')

        tot_items_frame = Frame(show_label_frame, width = 250, height = 300, bg = '#67d3ff',relief = 'raised', bd = 3)
        tot_items_label = Label(tot_items_frame,bg = '#67d3ff', font = 'arial 13 bold', text = 'Bill Items')
        tot_items_label.pack(side = 'top')
        tot_items_frame.pack_propagate(False)


        show_label_frame.pack(side = 'top', pady = 20)
        bill_label.place(relx = 0.1, rely = 0.1)
        bill_value.place(relx = 0.1, rely = 0.2,height = 35)
        press_enter.place(relx = 0.22, rely = 0.22)

        item_labe.place(relx = 0.1, rely = 0.5)
        item_value.place(relx = 0.1, rely = 0.6, height = 35)

        weight_label.place(relx = 0.25, rely = 0.5)
        weight_value.place(relx = 0.25, rely = 0.6, height = 35)

        return_btn.place(relx = 0.1, rely = 0.8)
        tot_items_frame.place(relx=0.55, rely=0.05)


        def ReturnShow(event):
            try:
                tot_children = tot_items_frame.pack_slaves()
                for j in tot_children:
                    j.pack_forget()

                item_value.configure(state = 'readonly')
                err.configure(text = '', bg = 'white')
                item_value.configure(state = 'readonly')
                weight_value.configure(state = 'readonly')
                val = data.admin_return_show(var_bill.get())
                if val == []:
                    err.configure(text='Wrong bill id...', bg='red')
                    return False
                else:
                    for items_tup in val:
                        name_ls = data.admin_return_item_name(items_tup[1])
                        name = name_ls[0].title() + " " + name_ls[1]
                        tot_items_label.pack(side = 'top')
                        Label(tot_items_frame, text = f"{items_tup[1]}" + " - " + name,bg = '#67d3ff').pack()

                        item_value.configure(state = 'normal')
                        weight_value.configure(state = 'normal')
                        return_btn.bind("<ButtonPress>", ReturnItemFinish)


            except TclError:
                err.configure(text = 'enter bill id...', bg = 'red')
                return False
            except EXCEPTION as e:
                print(e)


        bill_value.bind("<Return>", ReturnShow)


        def ReturnItemFinish(event):
            try:
                err.configure(text = '', bg = 'white')
                data.admin_return_finish(var_bill.get(),var_item.get(),var_weight.get(),err)
                var_item.set("")
                var_weight.set("")
                item_value.configure(state = 'readonly')
                weight_value.configure(state = 'readonly')
                val = data.retriev_bill(var_bill.get())
                pdf.Printer(val, current_time, False)
            except TclError:
                err.configure(text = 'enter item id...',bg = 'red')
                return False
            except EXCEPTION as e:
                return False






#todo business Partner Button ------------------------------------------------------------------------------------------------------------------------>
class BusinessPartners:
    def __init__(self,fr):
        self.show_frame = Frame(fr, width=700, height=400, bg='#ffffff')
        self.bar_frame = Frame(fr, height=40, width= 281, bg = "white")

        #buttons
        self.bar_partners = Label(self.bar_frame, text = 'Partners', bg= 'white', fg = 'blue')
        self.bar_add = Label(self.bar_frame, text = 'Add', bg = 'white', fg = 'blue')
        self.bar_edit = Label(self.bar_frame, text = 'Edit', bg = 'white', fg = 'blue')
        self.bar_credit = Label(self.bar_frame, text = 'Credit', bg = 'white', fg = 'blue')
        self.bar_debit = Label(self.bar_frame, text = 'Debit', bg = 'white', fg = 'blue')




        #binding buttons with events--------------------------->
        self.bar_partners.bind("<Enter>", lambda event: self.bar_partners.configure(fg='black', cursor="hand2",
                                                                                            font="arial 11 underline"))
        self.bar_partners.bind("<Leave>", lambda event: self.bar_partners.configure(fg='blue', cursor="hand2",
                                                                                            font="arial 11"))
        self.bar_partners.bind("<ButtonPress>", self.partners)


        self.bar_add.bind("<Enter>", lambda event: self.bar_add.configure(fg='black', cursor="hand2",
                                                                                            font="arial 11 underline"))
        self.bar_add.bind("<Leave>", lambda event: self.bar_add.configure(fg='blue', cursor="hand2",
                                                                                            font="arial 11"))
        self.bar_add.bind("<ButtonPress>", self.add_partner)


        self.bar_edit.bind("<Enter>", lambda event: self.bar_edit.configure(fg='black', cursor="hand2",
                                                                                            font="arial 11 underline"))
        self.bar_edit.bind("<Leave>", lambda event: self.bar_edit.configure(fg='blue', cursor="hand2",
                                                                                            font="arial 11"))
        self.bar_edit.bind("<ButtonPress>", self.partner_edit)



        self.bar_credit.bind("<Enter>", lambda event: self.bar_credit.configure(fg='black', cursor="hand2",
                                                                            font="arial 11 underline"))
        self.bar_credit.bind("<Leave>", lambda event: self.bar_credit.configure(fg='blue', cursor="hand2",
                                                                            font="arial 11"))
        self.bar_credit.bind("<ButtonPress>", self.partner_credit)


        # self.bar_debit.bind("<Enter>", lambda event: self.bar_debit.configure(fg='black', cursor="hand2",
        #                                                                     font="arial 11 underline"))
        # self.bar_debit.bind("<Leave>", lambda event: self.bar_debit.configure(fg='blue', cursor="hand2",
        #                                                                     font="arial 11"))
        # self.bar_debit.bind("<ButtonPress>", self.partner_debit)
        #<------------------------------------------------------------------------------------------------->



        #changing buttons backgrounds on click-------------------------->
        self.bg_current_list = []
        self.bg_list = [self.bar_partners, self.bar_add, self.bar_edit, self.bar_credit, self.bar_debit]
        for x in self.bg_list:
                x.bind("<ButtonRelease>", self.chang_bg)





        self.tab = Label(self.show_frame,font='Weight 22 bold underline', fg='#f6546a', bg='white')
        self.err_label = Label(self.show_frame,)
        self.show_frame.pack_propagate(False)




   #function for changing button background-------------------------------->
    def chang_bg(self,event):
        if len(self.bg_current_list) >= 2:
            for i in self.bg_current_list[0:-1]:
                i.configure(bg='white')
                self.bg_current_list.remove(i)





    def add(self):
        self.bar_frame.pack_propagate(False)
        self.show_frame.pack_propagate(False)
        self.bar_frame.pack(side = TOP, pady = 5)
        self.show_frame.pack(padx = 10, pady = 5)
        self.bar_partners.pack(side = 'left', ipadx = 7, ipady =6)
        self.bar_add.pack(side = 'left', ipadx = 7, ipady = 6)
        self.bar_edit.pack(side = 'left', ipadx = 7, ipady = 6)
        self.bar_credit.pack(side = 'left', ipadx = 7, ipady = 6)
        self.bar_debit.pack(side = 'left', ipadx = 7, ipady = 6)
        self.err_label.pack(side='bottom', fill='x')
        self.tab.pack(side = 'top')



    #forgetting all widgets in show frame-------------------------->
    def forget_childs(self):
        its = self.show_frame.pack_slaves()
        for x in its:
            x.pack_forget()

        its_grid = self.show_frame.grid_slaves()
        for j in its_grid:
            j.grid_forget()

        its_place = self.show_frame.place_slaves()

        for z in its_place:
            z.place_forget()






    def partners(self,event):
        self.err_label.configure(text = '', bg = 'SystemButtonFace')
        self.forget_childs()
        self.tab.configure(text = 'Partners')
        self.tab.pack(side = 'top')

        self.bar_partners.configure(bg='#9fa59a')
        if self.bar_partners not in self.bg_current_list:
            self.bg_current_list.append(self.bar_partners)


        #partner tree view------------------------------------->
        self.tree = ttk.Treeview(self.show_frame)
        self.tree['column'] = ("one", "two", "three",'four','five')
        self.tree.column('#0', width=30, anchor = 'center')
        self.tree.column('one', width=80, anchor = 'center')
        self.tree.column('two', width=140, anchor = 'center')
        self.tree.column('three', width= 140, anchor = 'center')
        self.tree.column('four', width=110, anchor = 'center')
        self.tree.column('five', width = 110, anchor = 'center')

        self.tree.heading("#0", text="No", )
        self.tree.heading("one", text="ID")
        self.tree.heading("two", text="Name")
        self.tree.heading('three', text = 'Phone')
        self.tree.heading("four", text="Balance")
        self.tree.heading('five', text = 'Due')

        self.tree.pack_propagate(False)
        self.scr = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scr.set)
        self.scr.pack(side=RIGHT, fill=Y)
        #<--------------------------------------------------------------------------------->




        self.tree.pack(side = 'top', pady = 20, padx =5 )
        self.err_label.pack(side='bottom', fill='x')

        data.ShowPartners(self.tree)

        close_val = None
        vals = []
        def get_id(event):
            nonlocal vals, close_val
            curItem = self.tree.focus()
            item = self.tree.item(curItem)
            close_val = item['values'][-1]
            val = item['values'][0:3]
            print(item['values'])
            address = data.partner_balance(val[0])[1]
            val.append(address)
            vals = val
            print_ledger.configure(state = "normal")
            close_partner.configure(state = 'normal')
        
        def close(event):
            print(vals[-2])
            if float(close_val) > 500:
                return False
            else:
                x = data.closepartner(vals[0])
                if x != True:
                    messagebox.showerror("failed", "something went wrong")
                    return False


        print_ledger = ttk.Button(self.show_frame, text = "Print Ledger", state = 'disabled', command=lambda: pdf.ledger(self.show_frame,vals,current_date))
        close_partner = ttk.Button(self.show_frame, text = "Close Partner", state = 'disabled',)
        
        close_partner.bind("<ButtonRelease>",close)


        print_ledger.place(relx = 0.78, rely = 0.85)
        close_partner.place(relx = 0.02, rely = 0.85)
        self.tree.bind("<<TreeviewSelect>>", get_id)
        








    def add_partner(self,event):
        self.err_label.configure(text = '', bg = 'SystemButtonFace') 
        self.forget_childs()
        self.err_label.configure(text='', bg='white')
        self.err_label.pack(side='bottom', fill=X)
        self.tab.pack(side = 'top')
        self.tab.configure(text = 'Add Partner')

        self.bar_add.configure(bg='#9fa59a')
        if self.bar_add not in self.bg_current_list:
            self.bg_current_list.append(self.bar_add)

        self.p_id_var = StringVar()
        self.p_name_var = StringVar()
        self.p_phone_var = StringVar()
        self.p_address_var = StringVar()
        self.p_credit_var = DoubleVar()
        self.p_ref_no_var = StringVar()



        # self.tab = Label(self.show_frame, text='Add Partner', font='Weight 22 bold underline', fg='#f6546a', bg='white')
        self.id = Label(self.show_frame, text = 'Enter Id: ', bg = 'white')
        self.id_value = ttk.Entry(self.show_frame, width = 10, textvariable = self.p_id_var)

        self.name = Label(self.show_frame, text = 'Name: ', bg = 'white')
        self.name_value = ttk.Entry(self.show_frame, width = 25, textvariable = self.p_name_var)

        self.phone = Label(self.show_frame, text = 'Phone: ', bg = 'white')
        self.phone_value = ttk.Entry(self.show_frame, width = 25, textvariable = self.p_phone_var)

        self.address = Label(self.show_frame, text = 'Address: ', bg = 'white')
        self.address_value = ttk.Entry(self.show_frame, width = 25, textvariable = self.p_address_var)

        self.credit_label = Label(self.show_frame, text = 'Credit: ', bg = 'white')
        self.credit_value = ttk.Entry(self.show_frame, width = 25, textvariable = self.p_credit_var, justify = 'center')

        self.add_ref_label = Label(self.show_frame, text = 'Ref No: ', bg = 'white')
        self.add_ref_value = ttk.Entry(self.show_frame, width = 25, textvariable = self.p_ref_no_var)


        self.submit_btn = ttk.Button(self.show_frame, text = 'Submit')

        self.tab.pack(side = 'top',)

        self.id.place(relx = 0.3, rely = 0.22)
        self.name.place(relx = 0.05, rely = 0.37)
        self.phone.place(relx = 0.45, rely = 0.37)
        self.address.place(relx = 0.05, rely =0.47)
        self.credit_label.place(relx = 0.45, rely = 0.47)
        self.add_ref_label.place(relx = 0.05, rely = 0.55)


        self.id_value.place(relx = 0.4, rely = 0.2, height = 35)
        self.name_value.place(relx = 0.15, rely = 0.37, height = 25)
        self.phone_value.place(relx = 0.55, rely = 0.37, height = 25)
        self.address_value.place(relx = 0.15, rely = 0.47, height = 25)
        self.credit_value.place(relx = 0.55, rely = 0.47, height = 25)
        self.add_ref_value.place(relx = 0.15, rely = 0.55, height = 25)

        self.submit_btn.place(relx = 0.3, rely = 0.7)


        def add_partner_funct(event):

            id = self.p_id_var.get()
            name = self.p_name_var.get()
            phone = self.p_phone_var.get()
            address = self.p_address_var.get()
            credit = self.p_credit_var.get()
            ref = self.p_ref_no_var.get()

            if id != '' and name != '':
                data.AddPartner(id, name, phone, address, current_date, credit, ref,self.err_label)


        self.submit_btn.bind("<ButtonPress>",add_partner_funct)







    def partner_edit(self,event):
        self.forget_childs()
        self.err_label.configure(text='', bg='white')
        self.err_label.pack(side='bottom', fill=X)
        self.tab.configure(text = ' Edit Partner')

        self.bar_edit.configure(bg='#9fa59a')
        if self.bar_edit not in self.bg_current_list:
            self.bg_current_list.append(self.bar_edit)


        var_id = StringVar()
        var_name = StringVar()
        var_phone = StringVar()
        var_address = StringVar()

        # self.tab = Label(self.show_frame, text='Edit Partner', font='Weight 22 bold underline', fg='#f6546a', bg='white')
        self.id = Label(self.show_frame, text = 'Enter Id: ', bg = 'white')
        self.id_value = ttk.Entry(self.show_frame, width = 10, textvariable = var_id)
        press_enter = Label(self.show_frame, text = '(Press Enter to continue)', font = 'helvetica 8 italic',bg = 'white')


        self.name = Label(self.show_frame, text = 'Name: ', bg = 'white')
        self.name_value = ttk.Entry(self.show_frame, width = 20, state = 'readonly', textvariable = var_name)

        self.phone = Label(self.show_frame, text = 'Phone: ', bg = 'white')
        self.phone_value = ttk.Entry(self.show_frame, width = 20, state = 'readonly', textvariable = var_phone)

        self.address = Label(self.show_frame, text = 'Address: ', bg = 'white')
        self.address_value = ttk.Entry(self.show_frame, width = 20, state = 'readonly', textvariable = var_address)


        self.submit_btn = ttk.Button(self.show_frame, text = 'Submit')

        self.tab.pack(side = 'top',)

        self.id.place(relx=0.3, rely=0.22)
        self.name.place(relx=0.3, rely=0.35)
        self.phone.place(relx=0.3, rely=0.43)
        self.address.place(relx=0.3, rely=0.53)

        self.id_value.place(relx=0.4, rely=0.2, height=35)
        press_enter.place(relx = 0.53, rely = 0.22)
        self.name_value.place(relx=0.4, rely=0.35, height=25)
        self.phone_value.place(relx=0.4, rely=0.43, height=25)
        self.address_value.place(relx=0.4, rely=0.53, height=25)
        self.submit_btn.place(relx=0.4, rely=0.7)

        self.err_label.pack(side='bottom', fill='x')

        def partner_edit_show(event):
            try:
                self.err_label.configure(text = '', bg = 'white')
                val = data.PartnerEditShow(var_id.get())
                if val == None:
                    self.err_label.configure(text = "Wrong partner Id...", bg = 'red')
                    return False
                else:
                    var_name.set(val[0])
                    var_phone.set(val[1])
                    var_address.set(val[2])


                self.name_value.configure(state = 'normal')
                self.phone_value.configure(state = 'normal')
                self.address_value.configure(state = 'normal')
            except EXCEPTION:
                return False


        def edit_partner_funct(event):
            data.EditPartner(var_id.get(),var_name.get(),var_phone.get(),var_address.get(),self.err_label)


        self.id_value.bind("<Return>", partner_edit_show)
        self.submit_btn.bind("<ButtonPress>", edit_partner_funct)





    def partner_credit(self,event):
        self.forget_childs()
        self.err_label.configure(text = '', bg = 'white')
        self.err_label.pack(side = 'bottom', fill = X)
        self.tab.configure(text = 'Credits',)
        self.tab.pack(side = 'top')

        self.bar_credit.configure(bg='#9fa59a')
        if self.bar_credit not in self.bg_current_list:
            self.bg_current_list.append(self.bar_credit)

        var_id = StringVar()
        var_name = StringVar()
        var_credit = DoubleVar()
        var_ref = StringVar()
        var_date = StringVar(value= current_date)

        self.id_label = Label(self.show_frame, text = 'Enter Id: ', bg = 'white')
        self.id_value = ttk.Entry(self.show_frame, width=10, textvariable = var_id)
        press_enter = Label(self.show_frame, text = '(Press Enter to continue)', font = 'helvetica 8 italic',bg = 'white')


        self.credit_label = Label(self.show_frame, text = 'Add Credit: ', bg = 'white')
        self.credit_value = ttk.Entry(self.show_frame, width = 20, stat = 'readonly', textvariable = var_credit)

        self.partner_name_label = Label(self.show_frame, bg = 'white')
        self.partner_name_value = Label(self.show_frame,bg= 'white', textvariable = var_name)

        self.ref_label = Label(self.show_frame, text = 'Ref No: ', bg = 'white')
        self.ref_value = ttk.Entry(self.show_frame, width = 20, state = 'readonly', textvariable = var_ref)

        self.date_label = Label(self.show_frame, text = 'Date: ', bg = 'white')
        self.date_value = ttk.Entry(self.show_frame, width = 20, state = 'readonly', textvariable = var_date)

        self.add_btn = ttk.Button(self.show_frame, text = 'Submit')




        #adding widgets to show frame -------------------------------->
        self.id_label.place(relx = 0.05, rely = 0.2)
        self.id_value.place(relx = 0.23, rely = 0.2, height = 35)
        press_enter.place(relx = 0.35, rely = 0.22)

        self.credit_label.place(relx = 0.05, rely = 0.3,)
        self.credit_value.place(relx = 0.23, rely = 0.3, height = 26)

        self.ref_label.place(relx = 0.05, rely = 0.4)
        self.ref_value.place(relx = 0.23, rely = 0.4, height = 26)

        self.partner_name_label.place(relx = 0.6, rely = 0.2)
        self.partner_name_value.place(relx = 0.7, rely = 0.2)

        self.date_label.place(relx = 0.05, rely = 0.5,)
        self.date_value.place(relx = 0.23, rely = 0.5)

        self.add_btn.place(relx = 0.23, rely = 0.6)

        self.err_label.pack(side='bottom', fill='x')

        def credit_show(event):
            try:
                self.partner_name_label.configure(text="")
                self.credit_value.configure(state='readonly')
                self.ref_value.configure(state='readonly')
                self.date_value.configure(state = 'readonly')
                self.err_label.configure(text = "", bg = 'white')
                val = data.EditCreditShow(var_id.get(),)
                if val == None:
                    self.err_label.configure(text = "Wrong partner id...", bg = 'red')
                    return False
                else:
                    var_name.set(val[0])
                    self.partner_name_label.configure(text = "Name: ")
                    self.credit_value.configure(state = 'normal')
                    self.ref_value.configure(state = 'normal')
                    self.date_value.configure(state = 'normal')
            except EXCEPTION:
                pass


        def add_credit_funct(event):
            data.AddCredit(var_id.get(),var_credit.get(),var_ref.get(),var_date.get(), self.err_label)
            self.partner_name_label.configure(text="")
            self.credit_value.configure(state='readonly')
            self.ref_value.configure(state='readonly')
            self.date_value.configure(state='readonly')
            var_name.set("")
            var_ref.set("")
            var_credit.set("")
            var_id.set("")
            var_date.set(current_date)


        self.id_value.bind("<Return>", credit_show)
        self.add_btn.bind("<ButtonPress>", add_credit_funct)



    # def partner_debit(self,event):
    #     self.err_label.configure(text = '', bg = 'SystemButtonFace')  

    #     var_partner = StringVar()
    #     var_bill = IntVar()
    #     self.forget_childs()
    #     self.err_label.configure(text = '', bg = 'white')
    #     self.err_label.pack(side = 'bottom', fill = X)
    #     self.tab.configure(text = 'debit',)
    #     self.tab.pack(side = 'top')

    #     self.bar_debit.configure(bg='#9fa59a')
    #     if self.bar_debit not in self.bg_current_list:
    #         self.bg_current_list.append(self.bar_debit)

    #     def debit_procceed():
    #         try:
    #             self.err_label.configure(text = '', bg = 'SystemButtonFace')
    #             p_id = var_partner.get()
    #             b_id = var_bill.get()
    #             msg = data.AddDebit(p_id,b_id)
    #             if msg == True:
    #                 self.err_label.configure(text = 'Debit has been successfully added', bg = 'green')
    #                 var_partner.set("")
    #                 var_bill.set(0)
    #             else:
    #                 self.err_label.configure(text = 'something went wrong...', bg = 'red') 
    #         except TclError:
    #             self.err_label.configure(text = 'Wrong Inputs...', bg = 'red')  

    #     show_frame = LabelFrame(self.show_frame, width = 450, height = 200, text = 'Debit')
    #     show_frame.pack(side = 'top', pady = 10)
    #     show_frame.pack_propagate(False)

    #     id_label = Label(show_frame, text = "Partner Id: ", )
    #     id_entry = ttk.Entry(show_frame, width = 20, justify = 'center', textvariable = var_partner)

    #     bill_label = Label(show_frame, text = "Bill No")
    #     bill_entry = ttk.Entry(show_frame, width = 15, justify = 'center', textvariable = var_bill)

    #     submit_btn = ttk.Button(show_frame, text = 'Submit', command = debit_procceed)

    #     id_label.place(relx = 0.01, rely = 0.25)
    #     id_entry.place(relx = 0.2, rely = 0.25, height = 26) 

    #     bill_label.place(relx = 0.01, rely = 0.4)
    #     bill_entry.place(relx = 0.2, rely = 0.4, height = 26)

    #     submit_btn.place(relx = 0.15, rely = 0.7)

        




#todo Dashboard ------------------------------------------------------------------------------------------------------------------------------------------------->

class Dashboard:
    def __init__(self,fr):
        self.frame = fr
        self.bar = Frame(self.frame, height = 45, bg = 'red')
        self.show_frame = Frame(self.frame, bg = 'blue')
        self.graph_frame1 = Frame(self.show_frame,  bg = 'gray')
        self.graph_frame2 = Frame(self.show_frame,  bg = 'gray')




    def add(self):

        self.forget_main()
        self.bar.pack(side = 'top', fill = X,)
        self.show_frame.pack(side = 'top', fill = 'both', expand = 1)
        self.graph_frame1.pack(side = 'left', fill = 'both', expand = True)
        self.graph_frame2.pack(side = 'left',fill = 'both', expand = True)
        

    def forget_main(self):
        vals = self.frame.pack_slaves()
        for x in vals:
            x.pack_forget()

        vals1 = self.frame.place_slaves()
        for x in vals1:
            x.place_forget()

        vals2 = self.frame.place_slaves()
        for x in vals2:
            x.place_forget()

    def forget(self):
        its = self.show_frame.pack_slaves()
        for x in its:
            x.pack_forget()

        its_grid = self.show_frame.grid_slaves()
        for j in its_grid:
            j.grid_forget()

        its_place = self.show_frame.place_slaves()

        for z in its_place:
            z.place_forget()



class Orders:
    def __init__(self, fr):
        self.show_frame = Frame(fr, width=700, height=400, bg='#ffffff')
        self.bar_frame = Frame(fr, height=40, width=280, bg="white")




        # buttons
        self.log_orders_btn = Label(self.bar_frame, text='Orders Log', bg='white', fg='blue')
        self.add_order_btn = Label(self.bar_frame, text='add Order', bg='white', fg='blue')
        self.cancel_order_btn = Label(self.bar_frame, text='Cancel Order', bg='white', fg='blue')


        # binding buttons with events--------------------------->
        self.log_orders_btn.bind("<Enter>", lambda event: self.log_orders_btn.configure(fg='black', cursor="hand2",
                                                                                    font="arial 11 underline"))
        self.log_orders_btn.bind("<Leave>", lambda event: self.log_orders_btn.configure(fg='blue', cursor="hand2",
                                                                                    font="arial 11"))
        self.log_orders_btn.bind("<ButtonPress>", self.Order_Logs_Show)

        self.add_order_btn.bind("<Enter>", lambda event: self.add_order_btn.configure(fg='black', cursor="hand2",
                                                                          font="arial 11 underline"))
        self.add_order_btn.bind("<Leave>", lambda event: self.add_order_btn.configure(fg='blue', cursor="hand2",
                                                                          font="arial 11"))
        self.add_order_btn.bind("<ButtonPress>", self.add_orders_show)

        self.cancel_order_btn.bind("<Enter>", lambda event: self.cancel_order_btn.configure(fg='black', cursor="hand2",
                                                                            font="arial 11 underline"))
        self.cancel_order_btn.bind("<Leave>", lambda event: self.cancel_order_btn.configure(fg='blue', cursor="hand2",
                                                                            font="arial 11"))
        self.cancel_order_btn.bind("<ButtonPress>", self.order_cancel_show)


        self.data_list = []
        self.companies_list = []

        # <------------------------------------------------------------------------------------------------->

    # changing buttons backgrounds on click-------------------------->
        self.bg_current_list = []
        self.bg_list = [self.log_orders_btn, self.add_order_btn, self.cancel_order_btn,]

        for x in self.bg_list:
            x.bind("<ButtonRelease>", self.chang_bg)

        self.tab = Label(self.show_frame, font='Weight 22 bold underline', fg='#f6546a', bg='white')
        self.err_label = Label(self.show_frame, )
        self.show_frame.pack_propagate(False)

    # function for changing button background-------------------------------->


    def chang_bg(self, event):
        if len(self.bg_current_list) >= 2:
            for i in self.bg_current_list[0:-1]:
                i.configure(bg='white')
                self.bg_current_list.remove(i)


    def add(self):
        self.bar_frame.pack_propagate(False)
        self.show_frame.pack_propagate(False)
        self.bar_frame.pack(side=TOP, pady=5)
        self.show_frame.pack(padx=10, pady=5)
        self.log_orders_btn.pack(side='left', ipadx=7, ipady=6)
        self.add_order_btn.pack(side='left', ipadx=7, ipady=6)
        self.cancel_order_btn.pack(side='left', ipadx=7, ipady=6)
        self.err_label.pack(side='bottom', fill='x')
        self.tab.pack(side='top')

    # forgetting all widgets in show frame-------------------------->


    def forget_childs(self):
        its = self.show_frame.pack_slaves()
        for x in its:
            x.pack_forget()

        its_grid = self.show_frame.grid_slaves()
        for j in its_grid:
            j.grid_forget()

        its_place = self.show_frame.place_slaves()

        for z in its_place:
            z.place_forget()




    def add_orders_show(self,event):
        self.add_order_btn.configure(bg='#9fa59a')
        if self.add_order_btn not in self.bg_current_list:
            self.bg_current_list.append(self.add_order_btn)

        if len(self.data_list) != 0:
            f = messagebox.askyesno("Cancel", "Are you sure,want to cancel...",parent = self.show_frame)
            if f == False:
                return False

        #adding companies to list
        try:
            self.companies_list = []
            for c in data.companies_for_orders():
                self.companies_list.append(c[0])
        except EXCEPTION as e:
            pass

        self.forget_childs()
        self.data_list = []
        self.dict_count = 0
        self.var_order_no = IntVar(value = data.order_id())
        self.var_company = StringVar()
        self.var_date = StringVar()

        add_show_frame = LabelFrame(self.show_frame, width = 600, height = 250, text = 'Order Information')
        add_show_frame.pack(pady= 50)



        self.order_label = Label(add_show_frame, text = "Order No:", font = 'arial 13')
        self.order_no = ttk.Entry(add_show_frame, width = 10, state = 'readonly', textvariable = self.var_order_no, justify = 'center')

        self.company_label = Label(add_show_frame, text = "Company:", font = 'arial 13')
        self.company_combo = ttk.Combobox(add_show_frame, values=self.companies_list, width=15, textvariable = self.var_company)
        if self.companies_list:
            self.company_combo.set(self.companies_list[0])
        else:
            self.company_combo.set("No company")

        self.date_label = Label(add_show_frame, text = "Date:", font = 'arial 13')
        self.date_value = ttk.Entry(add_show_frame, width = 18, textvariable = self.var_date)

        self.cancel_btn = ttk.Button(self.show_frame, text = "Cancel",)
        self.cancel_btn.bind("<ButtonPress>", self.add_orders_show)
        self.continue_btn = ttk.Button(self.show_frame, text = 'Continue', command = self.add_orders_continue)


        self.order_label.place(relx = 0.2,rely = 0.2)
        self.order_no.place(relx = 0.35, rely = 0.2, height = 35)

        self.company_label.place(relx = 0.2, rely = 0.43)
        self.company_combo.place(relx = 0.35, rely = 0.43, height = 26)

        self.date_label.place(relx = 0.2, rely = 0.6)
        self.date_value.place(relx = 0.35, rely = 0.6, height = 26)

        self.cancel_btn.place(relx = 0.2, rely = 0.85)
        self.continue_btn.place(relx = 0.4, rely = 0.85)





    def add_orders_continue(self):
        self.var_code = IntVar(value = '')
        self.var_cost = DoubleVar(value = '')
        self.var_weight = DoubleVar(value = '')

        if self.var_company.get() == "" or self.var_date.get() == "":
            return False
        if self.dict_count == 0:
            self.data_list.append({'order_no': self.var_order_no.get(), 'company': self.var_company.get(),'date':self.var_date.get()})
        self.forget_childs()


        show_frame = LabelFrame(self.show_frame, width = 380, height = 200, text = "Insert Items")
        show_frame.place(relx = 0.01, rely = 0.2)
        self.ord_label = Label(self.show_frame, text = "Order Id: ", bg = 'white')
        self.ord_id = ttk.Entry(self.show_frame, width = 8, state = 'readonly', textvariable = self.var_order_no,
                                justify = 'center')


        self.comp_label = Label(self.show_frame, text = "Company: ", bg = 'white')
        self.comp_value = Label(self.show_frame, bg = 'white', textvariable = self.var_company)

        self.item_label = Label(show_frame, text = "Item Code: ", font = "arial 13")
        self.item_value = ttk.Entry(show_frame, width = 16, justify = 'center', textvariable = self.var_code)

        self.weight_label = Label(show_frame, text = 'Weight: ', font = "arial 13")
        self.weight_value = ttk.Entry(show_frame, width = 16, justify = 'center', textvariable = self.var_weight)

        self.cost_label = Label(show_frame, text="Cost: ", font="arial 13")
        self.cost_value = ttk.Entry(show_frame, width=16, justify='center', textvariabl=self.var_cost)


        self.next_item_btn = Button(show_frame, text = "Next Item", command = self.next_item_func)
        self.confirm_btn = ttk.Button(self.show_frame, text = "Confirm Order", command = self.confirm_order_funct)
        self.insert_btn = Button(show_frame, text = "Insert item", command = self.insert_item_func, cursor = 'hand2')



        self.no_frame = Frame(self.show_frame, width = 230, height = 280, bg = '#99d6db', relief = 'raised', bd = 3)
        self.no_frame.pack_propagate(False)
        self.no_items = Label(self.no_frame, text = "Items added so far: ", bg = '#99d6db', font = 'Arial 15 italic underline')
        self.no_frame.place(relx = 0.63, rely = 0.28)
        self.no_items.pack()


        self.ord_label.place(relx = 0.7, rely = 0.02)
        self.ord_id.place(relx = 0.9, rely = 0.01, height = 30)

        self.comp_label.place(relx = 0.7, rely = 0.1)
        self.comp_value.place(relx = 0.9, rely = 0.1,)

        self.item_label.place(relx = 0, rely = 0.1)
        self.item_value.place(relx = 0.25, rely = 0.1,height = 26)

        self.weight_label.place(relx = 0, rely = 0.28)
        self.weight_value.place(relx = 0.25, rely = 0.28, height = 26)

        self.cost_label.place(relx = 0, rely = 0.46)
        self.cost_value.place(relx = 0.25, rely = 0.46, height = 26)
        self.insert_btn.place(relx = 0.25, rely = 0.75)


        self.cancel_btn.place(relx = 0.01, rely =  0.9)
        # self.next_item_btn.place(relx = 0.7, rely = 0.75)
        self.confirm_btn.place(relx = 0.41, rely = 0.9)

        codes_ls = data.items_codes_list()
        if len(self.data_list) > 1:
            print("here")
            for dicts in self.data_list[1:]:
                j = codes_ls[dicts['code']]['company'] + " Steels Grade-60 " + codes_ls[dicts['code']]['name'].replace(
                    " ", "")
                Label(self.no_frame, text=j, bg='#99d6db', font='arial 10 bold').pack(side='top')

    def next_item_func(self):
        # self.add_orders_continue()
        self.var_cost.set("")
        self.var_code.set("")
        self.var_weight.set("")


    def insert_item_func(self):
        try:
            codes_ls = data.items_codes_list()

            for v in self.data_list:
                if self.var_code.get() in v.values():
                    return False
                elif codes_ls[self.var_code.get()]['company'] != self.var_company.get():
                    return False

            j = codes_ls[self.var_code.get()]['company'] + " Steels Grade-60 " + codes_ls[self.var_code.get()]['name'].replace(" ", "")
            Label(self.no_frame, text = j, bg = '#99d6db', font = 'arial 10 bold').pack(side = 'top')


            self.data_list.append({'code':self.var_code.get(),'cost':self.var_cost.get(),'weight':self.var_weight.get()})
            self.dict_count += 1
            self.var_cost.set("")
            self.var_code.set("")
            self.var_weight.set("")
            self.ord_id.focus_set()


        except TclError:
            self.err_label.configure(text = "Fill all entries correctly...", bg = 'red')
            return False
        except KeyError:
            messagebox.showerror("Code","Wrong item code...",parent = self.show_frame)
            return False





    def confirm_order_funct(self):
        if len(self.data_list) <= 1:
            return False

        self.forget_childs()
        codes_ls = data.items_codes_list()

        self.var_tot_weight = DoubleVar()
        self.var_tot_amount = DoubleVar()
        self.var_extra = DoubleVar()
        self.var_total_amount = DoubleVar()
        self.var_extra_amount = DoubleVar()


        self.tree = ttk.Treeview(self.show_frame)
        self.tree['column'] = ("one", "two", "three","four","five")
        self.tree.column('#0', width=40, anchor='center')
        self.tree.column('one', width=70, anchor='center')
        self.tree.column('two', width=210, anchor='center')
        self.tree.column('three', width=100, anchor='center')
        self.tree.column('four', width=80, anchor='center')
        self.tree.column('five', width=110, anchor='center')

        self.tree.heading("#0", text="No", )
        self.tree.heading("one", text="Code")
        self.tree.heading("two", text="Item")
        self.tree.heading("three", text="Weight")
        self.tree.heading("four", text="Cost")
        self.tree.heading("five", text="Amount")

        self.tree.pack_propagate(False)
        self.scr = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scr.set)
        self.scr.pack(side=RIGHT, fill=Y)

        self.tree.pack(side = 'top', pady = 30)

        self.extra_label = Label(self.show_frame, text = "Extra Charges: ", bg = 'white', font = "arial 13 bold")
        self.extra_value = ttk.Entry(self.show_frame, width = 18, justify = 'center', textvariable = self.var_extra_amount)
        self.extra_info = Label(self.show_frame, text = "(Press Enter to continue)", bg = 'white', font = 'helvetica 8')

        self.order_weight_label = Label(self.show_frame, text = "Order Weight: ", bg = 'white', font = "helvetica 12 italic")
        self.order_weight_value = Label(self.show_frame,textvariable = self.var_tot_weight, font = "arial 13 bold", bg = 'white')

        self.order_amount_label = Label(self.show_frame, text = "Order Amount: ", bg = 'white', font = 'helvetica 12 italic')
        self.order_amount_value = Label(self.show_frame,textvariable = self.var_tot_amount, font = "arial 13 bold", bg = 'white')

        self.total_amount_label = Label(self.show_frame, text="Total Amount: ", font = "helvetica 12 italic", bg = 'white')
        self.total_amount_value = Label(self.show_frame, textvariable=self.var_total_amount, font = "arial 13 bold", bg = 'white')

        self.finish_btn = ttk.Button(self.show_frame, text = "Finish!", state = 'disabled',)
        self.back_btn = ttk.Button(self.show_frame, text = 'Back', command = self.add_orders_continue)

        self.order_weight_label.place(relx = 0.6, rely = 0.68)
        self.order_weight_value.place(relx = 0.8, rely = 0.68)

        self.order_amount_label.place(relx = 0.6, rely = 0.739)
        self.order_amount_value.place(relx = 0.8, rely = 0.739, height = 30)

        self.total_amount_label.place(relx = 0.6, rely = 0.8)
        self.total_amount_value.place(relx = 0.8, rely = 0.8)

        self.extra_label.place(relx = 0.01, rely = 0.68)
        self.extra_value.place(relx = 0.21, rely = 0.68, height = 27)
        self.extra_info.place(relx = 0.17, rely = 0.77)

        self.finish_btn.place(relx = 0.78, rely = 0.9)
        self.back_btn.place(relx = 0.01,rely = 0.9)



        self.finish_btn.bind("<ButtonPress>", self.Put_Order)



        #values for tree and database---------------------------------->
        self.weight_total = 0
        self.amount_total = 0
        count = 1
        for n in self.data_list[1:]:
            code = n['code']
            item = codes_ls[n['code']]['company'] + " Steels Grade-60 " + codes_ls[n['code']]['name'].replace(" ", "")
            weight = n['weight']
            cost = n['cost']
            self.weight_total = self.weight_total + weight
            self.amount_total = self.amount_total + (cost*weight)
            amt = float(f"%.2f"%(cost*weight))
            val = (code,item,weight,cost,amt)

            self.tree.insert('', 'end', text=count, values=val)
            count +=1

            self.var_tot_weight.set(self.weight_total)
            self.var_tot_amount.set(self.amount_total)



            def extra_func(event):
                self.var_total_amount.set(self.var_tot_amount.get() + self.var_extra_amount.get())
                self.finish_btn.configure(state = 'normal')
            self.extra_value.bind("<Return>", extra_func)



    def Put_Order(self, event):
        try:
            data.PutOrderDetail(self.data_list,self.weight_total,self.amount_total,self.var_extra_amount.get())
            m = messagebox.showinfo("Order Loaded", "Successfully loaded the order", parent = self.show_frame)
            if m == 'ok':
                self.data_list = []
                self.add_orders_show(event)

        except EXCEPTION as e:
            print(e)




    def order_cancel_show(self,event):
        self.forget_childs()
        self.data_list = []

        var_id = IntVar()
        var_id.set("")
        self.cancel_order_btn.configure(bg='#9fa59a')
        if self.cancel_order_btn not in self.bg_current_list:
            self.bg_current_list.append(self.cancel_order_btn)

        show_frame = LabelFrame(self.show_frame,width = 550, height = 200, text = 'Order Cancellations')
        show_frame.pack(side = 'top',pady = 10)
        order_id_label = Label(show_frame, text = "Enter Order Id: ")
        press_enter_label = Label(show_frame, text = "(Press Enter to continue)", font = 'helvetica 8')
        order_id_value = ttk.Entry(show_frame, width = 10,justify = 'center', textvariable = var_id)


        var_com_name = StringVar()
        var_ord_weight = StringVar()
        var_ord_amount = StringVar()
        var_ord_date = StringVar()

        com_name = Label(self.show_frame, bg = 'white', textvariable = var_com_name, font = 'helvetica 15 bold')

        ord_weight_label = Label(self.show_frame, bg = 'white', text ='Order Weight: ', font = "helvetica 12 italic")
        ord_weight_value = Label(self.show_frame, bg = 'white',  font = "arial 14 bold", textvariable = var_ord_weight)

        ord_amount_label = Label(self.show_frame, bg = 'white', text = 'Order amount: ', font = "helvetica 12 italic")
        ord_amount_value = Label(self.show_frame, bg = 'white',  font = "arial 14 bold", textvariable = var_ord_amount)

        ord_date_label = Label(self.show_frame, bg = 'white', text = 'Order date: ', font = "helvetica 12 italic")
        ord_date_value = Label(self.show_frame, bg = 'white', font = "arial 14 bold", textvariable = var_ord_date)


        canc_btn = ttk.Button(self.show_frame, text = "Cancel Order", state = 'disabled',)


        order_id_label.place(relx = 0.1, rely = 0.1)
        order_id_value.place(relx = 0.126, rely = 0.28, height = 35)
        press_enter_label.place(relx = 0.25, rely = 0.288)

        canc_btn.place(relx = 0.15, rely = 0.35)


        def show_order_info(event):
            try:

                vals = data.order_info(var_id.get())
                if vals[-1] == 'Cancelled':
                    messagebox.showerror("Cancelled", "This order has been already cancelled", parent = self.show_frame)
                    return False
                name = vals[1].title() + "'s " + "Order"
                weight = vals[2]
                amount = vals[3]
                date = vals[5]
                var_com_name.set(name)
                var_ord_weight.set(weight)
                var_ord_amount.set(amount)
                var_ord_date.set(date)
            except TypeError:
                messagebox.showerror("Code", "Wrong order id...",parent = self.show_frame)
                return False
            except TclError:
                messagebox.showerror("Code", "Wrong order id...",parent = self.show_frame)
                return False

            com_name.place(relx = 0.7, rely = 0.6)

            ord_weight_label.place(relx = 0.63, rely = 0.7)
            ord_weight_value.place(relx = 0.8, rely = 0.7)

            ord_amount_label.place(relx = 0.63, rely = 0.8)
            ord_amount_value.place(relx = 0.8, rely = 0.8)

            ord_date_label.place(relx = 0.63, rely = 0.9)
            ord_date_value.place(relx = 0.8, rely = 0.9)

            canc_btn.configure(state = 'normal')
            canc_btn.bind("<ButtonPress>", Cancel_funct)

        order_id_value.bind("<Return>",show_order_info)


        def Cancel_funct(event):
            ask = Toplevel(self.show_frame)
            main_window_width = ask.winfo_screenwidth() - 100
            main_window_height = ask.winfo_screenheight() - 100
            splash_width = main_window_width / 2 - 150
            splash_height = main_window_height / 2 - 70
            ask.geometry("310x140+%d+%d"%(splash_width,splash_height))
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
            pass_value = ttk.Entry(ask, width=20, textvariable = var_password, show = '*')
            ask_cancel = Button(ask, text="Cancel Order", width=10,)
            ask_quit = Button(ask, text="Quit", width=10, command = dest)

            err.pack(side='top', fill='x')

            pass_label.place(relx=0.13, rely=0.3)
            pass_value.place(relx=0.37, rely=0.3, height=27)

            ask_cancel.place(relx=0.15, rely=0.6)
            ask_quit.place(relx=0.5, rely=0.6)

            def Cancel(event):
                if var_password.get() != data.admin_login()[1]:
                    err.configure(text='Wrong Password...', bg='red')
                    return False

                data.CancelOrder(var_id.get())
                messagebox.showinfo("Cancelled", "Successfully cancelled the order",parent = self.show_frame)
                self.order_cancel_show(event)

                ask.destroy()
                ask.grab_release()
                return 'break'

            ask_cancel.bind("<ButtonPress>", Cancel)






    def Order_Logs_Show(self,event):
        self.log_orders_btn.configure(bg='#9fa59a')
        if self.log_orders_btn not in self.bg_current_list:
            self.bg_current_list.append(self.log_orders_btn)

        self.forget_childs()
        self.data_list = []
        self.tab.configure(text = "Print Orders Log")

        #variables------------------->
        var_year = StringVar()
        var_month = StringVar()
        var_results = StringVar()
        var_id = IntVar()
        var_company = StringVar()
        var_results.set(f"({data.OrderResults('Since Start','All','All')[0]})")
        var_id.set("")


        companies_list = ["All"]
        for c in data.companies_for_orders():
            companies_list.append(c[0])

        years_list = ['Since Start']
        for y in range(2019,2051):
            years_list.append(y)

        months_list = ['All','January','february','march','April','May','June','July','August','September',
            'October','November','December']

        hist_frame = LabelFrame(self.show_frame, text = 'Order History', width = 600, height = 200)
        hist_frame.pack_propagate(False)
        detail_frame = LabelFrame(self.show_frame, text = "Order Details", width = 600, height = 200)
        detail_frame.pack_propagate(False)
        hist_frame.pack(side = 'top', pady = 10)
        detail_frame.pack(side = 'top', pady = 10)


        select_yr_label = Label(hist_frame, text = "Select Year: ", )
        select_yr_combo = ttk.Combobox(hist_frame, width = 15, values = years_list, textvariable = var_year)
        var_year.set(years_list[0])

        select_mth_label = Label(hist_frame, text = "Select Month:")
        select_mth_combo = ttk.Combobox(hist_frame, width = 15, values = months_list , textvariable = var_month)
        var_month.set(months_list[0])

        select_comp_label = Label(hist_frame, text="Select Company:")
        select_comp_combo = ttk.Combobox(hist_frame, width=15, values=companies_list, textvariable=var_company)
        var_company.set(companies_list[0])

        prnt_btn = ttk.Button(hist_frame, text = "Print Results")


        select_yr_label.place(relx = 0.05, rely = 0.2)
        select_yr_combo.place(relx = 0.23, rely = 0.2)

        select_mth_label.place(relx = 0.05, rely = 0.4)
        select_mth_combo.place(relx = 0.23, rely = 0.4)

        select_comp_label.place(relx = 0.05, rely = 0.6)
        select_comp_combo.place(relx = 0.23, rely = 0.6)

        results_label = Label(hist_frame, text = 'Results: ')
        results_value = Label(hist_frame, textvariable = var_results)

        results_label.place(relx = 0.8, rely = 0.2)
        results_value.place(relx = 0.83, rely = 0.35)

        prnt_btn.place(relx = 0.77, rely = 0.78)



        #filtering order result set----------------->
        def SetResults(event):
            var_results.set(f"({data.OrderResults(var_year.get(),var_month.get(),var_company.get())[0]})")


        select_yr_combo.bind("<<ComboboxSelected>>", SetResults)
        select_mth_combo.bind("<<ComboboxSelected>>", SetResults)
        select_comp_combo.bind("<<ComboboxSelected>>", SetResults)


        #printing the orders log------------------>
        def PrintOrdersLog(event):
            datas = data.OrderResults(var_year.get(),var_month.get(),var_company.get())[1]
            ask_msg = messagebox.askyesno("Print", "Are you sure want to print the log",parent = self.show_frame)
            if ask_msg == True:
                pdf.Orders(datas)
            else:
                return False
        prnt_btn.bind("<ButtonPress>", PrintOrdersLog)





        def OrderIdEnter(event):
            chk_order = data.order_info(var_id.get())
            if chk_order == None:
                messagebox.showerror("Id", "The order does not exists",parent = self.show_frame)
                return False
            else:
                prnt_detail_btn.configure(state = 'normal')
                prnt_detail_btn.bind("<ButtonPress>", PrintOrderDetail)




        def PrintOrderDetail(evetn):
            detail_order = data.order_info(var_id.get())
            pdf.OrderDetail(detail_order, current_time)



        #order_detail--------------->
        order_no_label = Label(detail_frame, text = "Order No: ")
        order_no_value = ttk.Entry(detail_frame, width = 10, textvariable = var_id, justify = 'center')
        prss_enter_info = Label(detail_frame, text = "(Press enter to continue)", font = 'helvetica 8')
        prnt_detail_btn = ttk.Button(detail_frame, text = "Print Order", state = 'disabled')

        order_no_label.place(relx = 0.35, rely = 0.1)
        order_no_value.place(relx = 0.35, rely = 0.3, height = 35)

        prss_enter_info.place(relx = 0.3, rely = 0.6)
        prnt_detail_btn.place(relx = 0.7, rely = 0.7)


        order_no_value.bind("<Return>", OrderIdEnter)






#todo admin settings -------------------------------------------------------------------------------------------------->


class Settings:
    def __init__(self,fr):
        self.var_username = StringVar()
        self.var_password = StringVar()


        self.show_frame = Frame(fr, width=700, height=400, bg='#ffffff')
        self.tab = Label(self.show_frame, font='Weight 22 bold underline', fg='#f6546a', bg='white')

        self.show_labelframe = LabelFrame(self.show_frame, width = 500, height = 270, text = 'Admin Info')

        self.username_label = Label(self.show_labelframe, text = 'UserName: ',font = "helvetica 12 italic",)
        self.username_value = ttk.Entry(self.show_labelframe, width = 20, justify = 'center',
                                        textvariable = self.var_username,state = 'readonly')

        self.password_label = Label(self.show_labelframe, text = 'Password: ',font = "helvetica 12 italic",)
        self.password_value = ttk.Entry(self.show_labelframe, width = 20, justify = 'center',
                                        textvariable = self.var_password,state = 'readonly')


        self.edit_btn = Button(self.show_labelframe, text = 'Edit',command = self.EditClick)
        self.change_btn = Button(self.show_labelframe, text = 'Save Changes', command = self.SaveChanges)

        self.err = Label(self.show_labelframe,)


    def add(self):
        try:
            log_in = data.admin_login()
            username = log_in[0]
            password = log_in[1]
            self.var_username.set(username)
            self.var_password.set(password)
        except TypeError:
            pass
        self.username_value.configure(state = 'readonly')
        self.password_value.configure(state = 'readonly')
        self.err.configure(text = "", bg = "SystemButtonFace")

        self.show_frame.pack(side = 'top', pady = 30,padx = 20)
        self.show_frame.pack_propagate(False)
        self.tab.pack(side = 'top')
        self.show_labelframe.pack(side = 'top', pady = 30)
        self.show_labelframe.pack_propagate(False)
        self.err.pack(side = 'bottom', fill = 'x')

        self.username_label.place(relx = 0.2, rely = 0.2)
        self.username_value.place(relx = 0.4, rely = 0.2,height = 28)

        self.password_label.place(relx = 0.2, rely = 0.35)
        self.password_value.place(relx = 0.4, rely = 0.35, height = 28)

        self.edit_btn.place(relx = 0.35, rely = 0.6)
        self.change_btn.place(relx = 0.45, rely = 0.6)


    def EditClick(self):
        self.username_value.configure(state = 'normal')
        self.password_value.configure(state = 'normal')


    def SaveChanges(self):
        try:
            data.UpdateAdminInfo(self.var_username.get().lower(),self.var_password.get())
            self.err.configure(text = 'Saved Changes ', bg ='green')
        except EXCEPTION:
            self.err.configure(text = "Something went wrong", bg = 'red')





#todo profits ----------------------------------------------------------------------------------------------------->


class Profits:
    def __init__(self,fr):
        self.var_year = StringVar()
        self.var_month = StringVar()
        self.var_profit = DoubleVar()
        self.years_list = ['Since Start']
        for y in range(2019, 2051):
            self.years_list.append(y)

        self.months_list = ['All', 'January', 'february', 'march', 'April', 'May', 'June', 'July', 'August', 'September',
                       'October', 'November', 'December']


        self.show_frame = Frame(fr, width=700, height=400, bg='#ffffff')
        self.tab = Label(self.show_frame, font='Weight 22 bold underline', fg='#f6546a', bg='white')

        self.show_labelframe = LabelFrame(self.show_frame, width = 550, height = 270, text = 'Admin Info')

        self.year_label = Label(self.show_labelframe, text = "Select Year: ",font = "helvetica 12 italic")
        self.year_combo = ttk.Combobox(self.show_labelframe, values = self.years_list, width = 15, textvariable = self.var_year)
        self.var_year.set(self.years_list[0])

        self.month_label = Label(self.show_labelframe, text = "Select Month: ",font = "helvetica 12 italic")
        self.month_combo = ttk.Combobox(self.show_labelframe, values = self.months_list, width = 15, textvariable = self.var_month)
        self.var_month.set(self.months_list[0])

        self.profit_label = Label(self.show_labelframe, text = "Profit: ", font = "helvetica 12 italic")
        self.profit_value = Label(self.show_labelframe, font = 'arial 14 bold', textvariable = self.var_profit)
        self.var_profit.set("(goes here)")

        self.err = Label(self.show_labelframe,)

        self.year_combo.bind("<<ComboboxSelected>>", self.FilterProfit)
        self.month_combo.bind("<<ComboboxSelected>>", self.FilterProfit)


    def add(self):
        profit = f"%.2f"%data.GetProfit(self.var_year.get(),self.var_month.get())
        self.var_profit.set(f'{float(profit):,}')
        self.show_frame.pack(side = 'top', pady = 30,padx = 20)
        self.show_frame.pack_propagate(False)
        self.tab.pack(side = 'top')
        self.show_labelframe.pack(side = 'top', pady = 30)
        self.show_labelframe.pack_propagate(False)
        self.err.pack(side = 'bottom', fill = 'x')

        self.year_label.place(relx = 0.05, rely = 0.2)
        self.year_combo.place(relx = 0.27, rely = 0.2, height = 30)

        self.month_label.place(relx = 0.05, rely = 0.35)
        self.month_combo.place(relx = 0.27, rely = 0.35, height = 30)

        self.profit_label.place(relx =0.2, rely = 0.71)
        self.profit_value.place(relx = 0.35, rely = 0.7)


    def FilterProfit(self,event):
        profit = f"%.2f" % data.GetProfit(self.var_year.get(), self.var_month.get())
        self.var_profit.set(f'{float(profit):,}')
