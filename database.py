import sqlite3
from tkinter import messagebox
from decimal import Decimal



class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")


        #-----<creating business partner table>--------->
        self.b_partner = """CREATE TABLE IF NOT EXISTS partner(
                            p_id Text UNIQUE NOT NULL,
                            p_name TEXT NOT NULL,
                            p_phone TEXT NOT NULL,
                            p_address TEXT DEFAULT 'Not Given',
                            current_balance float
                            
                            
                         )"""
        self.cursor.execute(self.b_partner)

        #creating partner account----------------------------------------------->
        self.partner_account = """CREATE TABLE IF NOT EXISTS partner_account(
                            p_id text,
                            dates text,
                            debit float,
                            credit float,                           
                            balance float,
                            due float,
                            ref_no text NOT NULL,
                            FOREIGN KEY(p_id) REFERENCES partner(p_id)
                            
                            )
        """

        self.cursor.execute(self.partner_account)





    # ---------------<creating bills table>----------------------------------->

        self.bill = """CREATE TABLE IF NOT EXISTS bills(
                        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        c_name TEXT NOT NULL,
                        c_phone TEXT,
                        address TEXT,
                        bill_date TEXT,
                        bill_amount float,
                        bill_due float,
                        bill_revenue float,
                        p_id Text ,
                        path_file text,
                        bill_discount float,
                        FOREIGN KEY(p_id) REFERENCES partner(p_id)
                        )"""

        self.cursor.execute(self.bill)






        #--------<creating sales table>-------------------------------------#

        self.sale = """CREATE TABLE IF NOT EXISTS sales(
                        
                        bill_id INT,
                        item_id INT,
                        cost float,
                        weight float,
                        amount float,
                        sale_profit float,
                        cost_at_time float,
                        FOREIGN KEY(bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE ,
                        FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE NO ACTION
                          )"""
        self.cursor.execute(self.sale)








        #-------------------<Creating items table>----------------------------------->

        self.items = """CREATE TABLE IF NOT EXISTS items(                        
                        item_id INTEGER PRIMARY KEY,
                        item_size TEXT NOT NULL,
                        company TEXT NOT NULL,
                        current_weight float,
                        avg_cost float
                         )"""
        self.cursor.execute(self.items)
        #-----------------<creating cost table>---------------------------------------->




        self.items_desc = """CREATE TABLE IF NOT EXISTS items_desc(
                            item_id INTEGER,
                            cost float,
                            weight float,
                            dates text,
                            order_id INTEGER,
                            status text,
                            FOREIGN KEY(item_id) REFERENCES items(item_id),
                            FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE
                             )"""
        self.cursor.execute(self.items_desc)


        self.admin = """CREATE TABLE IF NOT EXISTS admin(
                        admin_name text NOT NULL,
                        password text NOT NULL
                        )     
                        """
        self.cursor.execute(self.admin)

        self.canc_bill = """CREATE TABLE IF NOT EXISTS cancelled_bills(
                               bill_id INTEGER PRIMARY KEY,
                               c_name TEXT NOT NULL,
                               c_phone TEXT,
                               address TEXT,
                               bill_date TEXT,
                               bill_amount float,
                               bill_due float,
                               bill_revenue float,
                               p_id Text ,
                               path_file text, 
                               cause text,
                               canc_date text,
                               bill_discount float,
                               FOREIGN KEY(p_id) REFERENCES partner(p_id)
                               )"""
        self.cursor.execute(self.canc_bill)



    #making order table-------------------------------->
        self.order = """CREATE TABLE IF NOT EXISTS orders( 
                        order_id INTEGER primary key,
                        company text,
                        order_weight float,
                        order_cost float,
                        extra_charges float,
                        dates text,
                        status text
        )"""

        self.cursor.execute(self.order)

    def __del__(self):
        self.conn.close()


    def InsertBills(self,name,phone,date,bill_amount,due,bill_revenue,p_id,addr):
        self.p_id = p_id
        if p_id == '':
            self.p_id = None

        b_amount = float("%.2f"%bill_amount)
        b_due = float("%.2f"%due)
        b_revenue = float("%.2f"%bill_revenue)

        try:
            self.cursor.execute("""INSERT INTO bills(bill_id,c_name,address,c_phone,bill_date,bill_amount,bill_due,bill_revenue,p_id, path_file,bill_discount)
                                  VALUES(NULL,?,?,?,?,?,?,?,?,?,?)""",(name, addr, phone, date, b_amount, b_due, b_revenue,self.p_id,"",0))
        except sqlite3.IntegrityError:
            messagebox.showerror("Partner Id", "Please check partner id...")
            return False

        self.conn.commit()

    def bill_path(self, id, path):
        self.cursor.execute("UPDATE bills SET path_file = ? WHERE bill_id = ?", (path,id))
        self.conn.commit()

    #getting bill path for showing or printing:
    def ShowBillPath(self,id):
        try:
            self.cursor.execute("SELECT path_file FROM bills WHERE bill_id = ?",(id,))
            bill = self.cursor.fetchone()[0]
        except TypeError:
            messagebox.showerror("Bill","The bill does not exist")
            return False
        return bill

    def retriev_bill(self,id):
        self.cursor.execute("SELECT * FROM bills WHERE bill_id = ?", (id,))
        val = self.cursor.fetchone()
        return val
    def retriev_items_for_admin_bill(self,id):
        self.cursor.execute("SELECT item_size,company FROM items WHERE item_id = ?",(id,))
        val = self.cursor.fetchone()
        return val

    def bill_detail_for_admin(self,bill_no):
        self.cursor.execute("""SELECT * FROM sales WHERE bill_id = ?""",(bill_no,))
        vals = self.cursor.fetchall()
        return vals
 

    def InsertSales(self,ls, name, phone, date, bill_amount, due, p_id, addr):

        self.bill_revenue = 0

        x = self.InsertBills(name,phone,date,bill_amount,due,self.bill_revenue,p_id,addr)
        if x == False:
            return False
        self.bill_val = self.cursor.execute("SELECT MAX(bill_id) FROM bills")
        self.bill_no = self.cursor.fetchone()[0]
        for args in ls:
            self.id = args[0]
            self.cost = args[1]
            self.weight = args[2]
            self.amount = args[3]

            self.original = self.cursor.execute("SELECT avg_cost,current_weight,company FROM items WHERE item_id = ?", (self.id,))
            cost_weight = self.cursor.fetchone()

            self.original_cost = cost_weight[0]
            self.original_weight = cost_weight[1]

            self.sale_profit = self.amount - (self.original_cost*self.weight)
            if cost_weight[2].lower() == 'loading-unloading':
                self.sale_profit = self.sale_profit-self.amount

            if cost_weight[2].lower() == 'transportation':
                self.sale_profit = self.sale_profit-self.amount


            self.cursor.execute("""INSERT INTO sales(bill_id,item_id,cost,weight,amount,sale_profit,cost_at_time)
                                  VALUES(?,?,?,?,?,?,?) """,(self.bill_no,self.id,self.cost,self.weight,self.amount,self.sale_profit,self.original_cost))

        #updating weight------------------------------>
            self.red_weight = self.original_weight - self.weight
            self.cursor.execute("UPDATE items SET current_weight = ? WHERE item_id = ?",(self.red_weight,self.id))


            self.conn.commit()

            self.bill_revenue = self.bill_revenue + self.sale_profit


        self.cursor.execute("UPDATE bills SET bill_revenue = ? WHERE bill_id = ?",(self.bill_revenue,self.bill_no))
        self.conn.commit()


        if p_id != '':
            self.debit = bill_amount

            #getting Partner Current Balance ------------------------------>
            self.blnc = self.cursor.execute("SELECT current_balance FROM partner WHERE p_id = ?",(p_id,))
            self.part_balance = self.cursor.fetchone()[0]

            if self.part_balance == None:
                self.part_balance = 0
            self.current_balance = self.part_balance
            self.balance_upd = (self.current_balance - self.debit)


            #setting up ledger due-------------------->
            self.due = 0
            if (self.current_balance <= 0) or (self.current_balance < self.debit):
                self.due = -(self.current_balance - self.debit)


            #setting ledger balance ------------------->
            # self.ledg_balance = self.current_balance
            # if self.current_balance <= 0:
            #     self.ledg_balance = 0


            #updating partner current balance----------->
            self.ref = f'bill_{self.bill_no}'
            bill = self.bill_no
            self.cursor.execute("UPDATE partner SET current_balance = ? WHERE p_id = ?",(self.balance_upd,p_id))

            check_balance = self.cursor.execute("SELECT current_balance FROM partner WHERE p_id = ?",(p_id,))
            balance = self.cursor.fetchone()[0]

            if balance <= 0:
                self.cursor.execute("""INSERT INTO partner_account(p_id,dates,debit,balance,due,ref_no,bill_no) VALUES(?,?,?,?,?,?,?)""",
                                    (p_id,date,self.debit,0,self.due,self.ref,bill))
            else:
                 self.cursor.execute("""INSERT INTO partner_account(p_id,dates,debit,balance,due,ref_no,bill_no) VALUES(?,?,?,?,?,?,?)""",
                                    (p_id,date,self.debit,balance,0,self.ref,bill))

            self.conn.commit()








    def InsertItems(self,item_id,size,company):
        self.items = """INSERT INTO items(item_id,size, company)
                        VALUES(?,?,?)""",(item_id,size,company)


    def InsertItems_desc(self,id,desc_cost,desc_weight):
        self.items_desc = """INSERT INTO  items_desc(item_id,cost,weight)
                             VALUES(?,?,?)""",(id,desc_cost,desc_weight)

    def InsertPartner(self,p_id,p_name,p_phone,p_address,p_balance_due):
        self.partner = """INSERT INTO partner(p_id,p_name,p_phone,p_address,p_balance_due)
                          VALUES(?,?,?,?,?)""",(p_id,p_name,p_phone,p_address,p_balance_due)




    #setting current bill id------------------------>
    def bill_id(self,):
        # self.cursor.execute("""SELECT MAX(bill_id) FROM bills""")
        self.cursor.execute("""SELECT * FROM sqlite_sequence WHERE name='bills'""")
        val = self.cursor.fetchone()
        bill_id = 0
        if val == None:
            bill_id = 1
        else:
            bill_id = val[1]+1
        return bill_id

    def bill_ids(self):
        self.cursor.execute("SELECT bill_id FROM bills")
        vals = self.cursor.fetchall()
        ls = []
        for x in vals:
            ls.append(x[0])
        return ls


    def Business_ids(self,id):
        self.cursor.execute("SELECT p_id,p_name,p_phone,p_address, status FROM partner WHERE p_id = ?",(id,))
        val = self.cursor.fetchone()
        return val



    def items_codes_list(self):
        self.cursor.execute("""SELECT item_id,item_size,company FROM items""")
        val = self.cursor.fetchall()
        dicts = {}
        for x in val:
            dicts[x[0]] = {'name':x[1],'company': x[2]}
        return dicts

    def Code_focus_Original(self):
        self.cursor.execute("SELECT item_id, avg_cost, current_weight FROM items")
        j = self.cursor.fetchall()
        dicts = {}
        for x in j:
            dicts[x[0]] = {'cost' : x[1], 'weight' : x[2]}
        return dicts

#todo ------------------------------<Admin Panel>------------------------------------------------------------------------------------------------------------------------>




    #--------------<adding new items>----------------------------------
    def add_new_item_id(self,vars,company):
        self.cursor.execute("""SELECT MAX(item_id) FROM items""")
        new_item_id = self.cursor.fetchone()[0]
        if new_item_id == None:
            new_item_id = 1000
        vars.set(new_item_id + 1)

        self.cursor.execute("""SELECT DISTINCT company FROM items""")
        companies = self.cursor.fetchall()
        for x in companies:
            company.append(x[0])


    def add_new_item(self,code,size,company,err,date):
        self.cursor.execute("""SELECT item_id FROM items WHERE item_id = ?""",(code,))
        chk_code = self.cursor.fetchone()

        if chk_code == None:
            if len(str(code)) == 4:
                try:
                    if code == '' or size == '' or company == '':
                        err.configure(text = "Failed:   Fill The * Entries", bg = 'red')
                        return False
                    else:


                        self.cursor.execute("""INSERT INTO items(item_id, item_size, company,current_weight,avg_cost ) VALUES(?,?,?,?,?) """,
                                            (code,size + " mm", company,0,0))
                        self.conn.commit()


                except Exception:
                    err.configure(text="Failed: Unable To Load Data", bg='red')

                else:
                    self.conn.commit()
                    err.configure(text="Successfully Loaded Data", bg='green')

            else:
                err.configure(text="Failded: Code Should Four Digit", bg='red')
                return False

        else:
            print("Item exists")




    def admin_view_items(self,lbox):
        self.cursor.execute("""SELECT item_id,item_size,company FROM items""")
        tups = self.cursor.fetchall()
        chk = lbox.get_children()
        for x in chk:
            lbox.delete(x)
        for vals in tups:
                lbox.insert('', 'end',text = (tups.index(vals) + 1), values = vals)





    def upd_func_values(self,id):
        self.cursor.execute("""SELECT * FROM items WHERE item_id = ? """,(id,))
        name_tup = self.cursor.fetchone()
        name_val = 0
        if name_tup == None:
            name_val = name_tup
        else:
            name_val = name_tup

        return name_val






    def admin_update(self,cost,weight,id,date):
        try:
            if cost == '':
                cost = 0
            if weight == '':
                weight = 0

            self.cursor.execute("SELECT current_weight,avg_cost FROM items WHERE item_id = ?",(id,))
            w = self.cursor.fetchone()
            weig = w[0]
            cos = w[1]

            if weig > 0 and cost !=0 and weight != 0:
                nw_cost = ((weig*cos) + (weight *cost))/(weight+weig)
                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?), avg_cost = ?
                 WHERE item_id = ?""",(weight,nw_cost,id))
                self.cursor.execute("""INSERT INTO items_desc(item_id,cost,weight,status,dates) VALUES(?,?,?,?,?)""",
                                    (id,cost,weight,'updated',date))
                self.conn.commit()

            elif weig > 0 and cost == 0:
                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?)
                                 WHERE item_id = ?""", (weight,id))
                self.cursor.execute("""INSERT INTO items_desc(item_id,cost,weight,status,dates) VALUES(?,?,?,?,?)""",
                                    (id, cost, weight, 'updated', date))
                self.conn.commit()



            else:
                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?), avg_cost = ? WHERE item_id = ?""",(weight,cost,id))
                self.cursor.execute("""INSERT INTO items_desc(item_id,cost,weight,status,dates) VALUES(?,?,?,?,?)""",
                                    (id, cost, weight, 'updated', date))
                self.conn.commit()

        except Exception as e:
            print(e)




    def delete_items_show(self,id,name):
        self.cursor.execute("""SELECT item_size,company FROM items WHERE item_id = ?""",(id,))
        vals = self.cursor.fetchone()
        if vals == None:
            name.set("Enter Correct Id...")
        else:
            name.set(vals[1] + " " + vals[0])

    def delete(self,id, err):
        self.cursor.execute("""SELECT * FROM items WHERE item_id = ?""",(id,))
        vals = self.cursor.fetchone()
        if vals == None:
            err.configure(text = "Failed:   Wrong Code Id", bg = 'Red')

        else:
            self.cursor.execute("""DELETE FROM items WHERE item_id = ?""", (id,))
            self.conn.commit()
            err.configure(text=f"{vals[1]} {vals[2]} has been deleted", bg='green')



    def admin_return_show(self,id):
        self.cursor.execute("""SELECT * FROM sales WHERE bill_id = ?""",(id,))
        val = self.cursor.fetchall()
        return val
    def admin_return_item_name(self,id):
        self.cursor.execute("SELECT company,item_size FROM items WHERE item_id = ?",(id,))
        val = self.cursor.fetchone()
        return val

    def admin_return_finish(self,bill_id,item_id,canc_weight,err):
        try:
            self.cursor.execute("SELECT cost,weight,amount,sale_profit,cost_at_time FROM sales WHERE item_id = ? and bill_id = ?",(item_id,bill_id))
            sale_vals = self.cursor.fetchone()
            if sale_vals == None:
                err.configure(text = 'Wrong item id', bg = 'red')
                return False
            sale_cost = sale_vals[0]
            sale_weight = sale_vals[1]
            sale_amount = sale_vals[2]
            sale_revenue = sale_vals[3]
            sale_cost_at_time = sale_vals[4]
            revenue_by_weight = (sale_cost-sale_cost_at_time)*canc_weight
            canc_amount = sale_cost*canc_weight

            if canc_weight > sale_weight:
                err.configure(text = "Can not return more then the sold weight", bg = 'red')
                return False
            elif canc_weight <= 0:
                err.configure(text = "Can not return zero or negative weight", bg = 'red')
                return False

            self.cursor.execute("SELECT bill_amount,bill_due, p_id FROM bills WHERE bill_id = ?",(bill_id,))
            bill = self.cursor.fetchone()
            bill_amount = bill[0]
            bill_due = bill[1]
            p_id = bill[2]
            bill_paid = (bill_amount - bill_due)


            self.cursor.execute("SELECT current_weight,avg_cost FROM items WHERE item_id = ?",(item_id,))
            item_val = self.cursor.fetchone()

            avg_cost = item_val[1]

            if item_val[0] <= 0:
                print(canc_weight,canc_amount)
                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?),
                                    avg_cost = ? WHERE item_id = ?""",(canc_weight,sale_cost_at_time,item_id))

                self.cursor.execute("""UPDATE bills SET bill_amount = bill_amount-?,
                                    bill_revenue= bill_revenue-? WHERE bill_id = ?""",
                                    (canc_amount, revenue_by_weight, bill_id))
                self.cursor.execute("""UPDATE sales SET weight = (weight -?),amount = (amount-?) WHERE item_id = ? and bill_id = ?""",
                                    (canc_weight,canc_amount,item_id, bill_id))
                self.conn.commit()
            else:
                new_avg_cost = ((item_val[0] * item_val[1]) + (sale_cost_at_time * canc_weight)) / (item_val[
                    0] + canc_weight)

                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?),
                                    avg_cost = ? WHERE item_id = ?""",(canc_weight,new_avg_cost,item_id))

                self.cursor.execute("""UPDATE bills SET bill_amount = bill_amount-?,
                                    bill_revenue= bill_revenue-? WHERE bill_id = ?""" ,(canc_amount,revenue_by_weight,bill_id))
                self.cursor.execute("""UPDATE sales SET weight = (weight-?),sale_profit = (sale_profit - ?),amount = (amount-?)
                                    WHERE item_id = ? and bill_id = ?"""
                                    ,(canc_weight,revenue_by_weight,canc_amount,item_id,bill_id))
                # self.cursor.execute("DELETE FROM sales WHERE item_id = ? and bill_id = ?",(item_id,bill_id))
                self.conn.commit()


            self.cursor.execute("SELECT bill_amount FROM bills WHERE bill_id = ?",(bill_id,))
            amnt = self.cursor.fetchone()[0]

            due = amnt - bill_paid

            self.cursor.execute("UPDATE bills SET bill_due = ? WHERE bill_id = ?",(due,bill_id))

            if p_id != '' or p_id != None:
                self.cursor.execute("UPDATE partner SET current_balance = current_balance + ? WHERE p_id= ?", (canc_amount, p_id))

            self.conn.commit()


            err.configure(text = 'the item has been successfully returned...', bg = 'green')
        except Exception as e:
            print(e)








    #todo Business Partner------------------------------------------------------------------------------------------------------------------------------------------------->

    def partner_balance(self,id):
        self.cursor.execute("""SELECT current_balance,p_address FROM partner WHERE p_id = ?""",(id,))
        balance = self.cursor.fetchone()
        return balance
    def AddPartner(self,pid,pname,pphone,paddress,dates,credit,rep_no,err):
        balnc = credit

        try:
            self.cursor.execute("""INSERT INTO partner(p_id,p_name,p_phone,p_address,current_balance) VALUES(?,?,?,?,?)""",
                                (pid,pname,pphone,paddress,balnc))
            err.configure(bg = 'green', text = 'Successful:   Partner Successfully Added...')
        except sqlite3.IntegrityError:
            err.configure(bg = 'red', text = 'Failed:    Id Exists...')
            print("Id exists...")

        if (credit != '' or credit != 0) and rep_no != '':
            ref = f'StartingCredit{rep_no}'
            self.cursor.execute("""INSERT INTO partner_account(p_id,debit,credit,balance,dates,rep_no) VALUES(?,?,?,?,?,?)""",
                                (pid,None,credit,balnc,dates,ref))
            err.configure(bg='green', text='Successful:   Partner Successfully Added...')

        self.conn.commit()


    def ledger(self,id):
        self.cursor.execute("""SELECT * FROM partner_account WHERE p_id = ?""", (id,))
        val = self.cursor.fetchall()
        return val




    #Showing All partners in view tab---------------------->
    def ShowPartners(self,tr):
        self.cursor.execute("SELECT p_id, p_name,p_phone,current_balance FROM partner WHERE status = 'open' ")
        tups = self.cursor.fetchall()
        chk = tr.get_children()
        for x in chk:
            tr.delete(x)
        for vals in tups:
            j = list(vals)
            x = 0

            if j[-1] == None:
                j[-1] = 0

            if j[-1] < 0:
                x = -(vals[-1])
                j[-1] = 0

            j.append(x)
            tr.insert('', 'end', text=(tups.index(vals) + 1), values=j)
    
    def closepartner(self, id):
        try:
            self.cursor.execute("UPDATE partner SET status = 'close' WHERE p_id = ?",(id,))
            self.conn.commit()
            return True
        except Exception as e:
            messagebox.showerror("error", "something went wrong")
            return False
    def openpartner(self,id):
        try:
            self.cursor.execute("UPDATE partner SET status = 'open' WHERE p_id = ?",(id,))
            self.conn.commit()
            return True
        except Exception as e:
            messagebox.showerror("error", "something went wrong")
            return False
    def openpartnernew(self,id):
        try:
            self.cursor.execute("UPDATE partner SET status = 'open', current_balance = 0 WHERE p_id = ?",(id,))
            self.conn.commit()
            return True
        except Exception as e:
            messagebox.showerror("error", "something went wrong...")
            return False


    #show Partner information before editting----------------->
    def PartnerEditShow(self,id):
        self.cursor.execute("SELECT p_name,p_phone,p_address FROM partner WHERE p_id = ?",(id,))
        vals = self.cursor.fetchone()
        val = 0
        if vals == None:
            val = vals
        else:
            val = vals

        return val




    def EditPartner(self,id,name,phone,address,err):
        try:
            self.cursor.execute("UPDATE partner SET p_name = ?,p_phone = ?, p_address = ? WHERE p_id = ?",(name,phone,address,id))
            err.configure(text = 'Successfull:   Successfully Updated...', bg = 'green')
        except Exception as e:
            print(e)
            err.configure(text = 'Failed:   Something Went Wrong!...', bg = 'red')



    def EditCreditShow(self,id):
        self.cursor.execute("SELECT p_name FROM partner WHERE p_id = ?",(id,))
        nm = self.cursor.fetchone()
        val = 0
        if nm == None:
            val = nm
        else:
            val = nm

        return val



    #Add Credit To Business Partner--------------------------------->
    def AddCredit(self,id,credit,ref,date,err):
        try:
            if ref != '':
                
                due = 0
                self.cursor.execute("""SELECT current_balance FROM partner WHERE p_id = ?""", (id,))
                current_balance = self.cursor.fetchone()[0]
                if current_balance < 0:
                    due = -(current_balance)

                if credit >= due:
                    balance = (credit-due)
                    self.cursor.execute("""INSERT INTO partner_account(p_id,dates,credit,balance,due,ref_no) VALUES(?,?,?,?,?,?)""",
                                        (id, date, credit,balance,0,ref))
                else:
                    upd_due = (due-credit)
                    self.cursor.execute("""INSERT INTO partner_account(p_id,dates,credit,balance,due,ref_no) VALUES(?,?,?,?,?,?)""",
                                    (id, date, credit,0,upd_due,ref))


                self.cursor.execute("UPDATE partner SET current_balance = (current_balance + ?) WHERE p_id = ?",(credit,id))

                self.conn.commit()
                err.configure(text = 'Successful:   Credit Added...', bg = 'green')
            else:
                err.configure(text = 'Failed:   Please Enter Reference No...')
                return False
        except Exception as e:
            print(e)
            err.configure(text = 'Failed:   Something Went Wrong!...', bg = 'red')
            pass



    def admin_info_pic_path(self):
        self.cursor.execute("SELECT pic_path FROM admin")
        path = self.cursor.fetchone()[0]
        return path

    def admin_login(self):
        self.cursor.execute("SELECT admin_name,password FROM admin")
        vals = self.cursor.fetchone()
        return vals

    def InsertAdminInfo(self,username,password):
        self.cursor.execute("INSERT INTO admin(admin_name,password) VALUES(?,?)",(username,password))
        self.conn.commit()

    def UpdateAdminInfo(self,username, password):
        try:
            self.cursor.execute("""UPDATE admin SET admin_name =?, password = ?""",(username, password))
            self.conn.commit()
        except Exception as e:
            return e



#todo partner debit
    # def AddDebit(self,partner_id,bill_id):
    #     try:
    #         self.cursor.execute("SELECT bill_amount,bill_date, p_id FROM bills WHERE bill_id = ?", (bill_id,))
    #         vals = self.cursor.fetchone()
    #         bill_amount = vals[0]
    #         bill_date = vals[1]
    #         chk_p_id = vals[2]
    #         ref = f'bill_{bill_id}'
            

    #         if chk_p_id == partner_id:
    #             return False
    #         elif chk_p_id != '' or chk_p_id != None:
    #             self.cursor.execute("UPDATE partner SET current_balance = (current_balance + ?) WHERE p_id = ?", (bill_amount, chk_p_id))
    #             self.cursor.execute("DELETE FROM partner_account WHERE p_id =?", (chk_p_id,))
    #             self.cursor.execute("UPDATE partner SET current_balance = (current_balance - ?) WHERE p_id = ?", (bill_amount, partner_id))
    #         else:

    #             self.cursor.execute("UPDATE partner SET current_balance = (current_balance - ?) WHERE p_id = ?", (bill_amount, partner_id))
            

    #         self.cursor.execute("UPDATE bills SET p_id = ? WHERE bill_id = ?",(partner_id, bill_id))
    #         self.cursor.execute("SELECT current_balance FROM partner WHERE p_id = ?", (partner_id,))
    #         balance = self.cursor.fetchone()[0]

    #         due = 0
    #         if (balance <= 0):
    #             due = -(balance)

    #         if balance <= 0:
    #             self.cursor.execute("""INSERT INTO partner_account(p_id,dates,debit,balance,due,ref_no,bill_no) VALUES(?,?,?,?,?,?,?)""",
    #                                 (partner_id,bill_date,bill_amount,0,due,ref,bill_id))
    #         else:
    #             self.cursor.execute("""INSERT INTO partner_account(p_id,dates,debit,balance,due,ref_no,bill_no) VALUES(?,?,?,?,?,?,?)""",
    #                                 (partner_id,bill_date,bill_amount,balance,0,ref,bill_id))

    #         self.conn.commit()
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False















    #todo order panel---------------------------------------------->

    #retrieving order id----------->
    def order_id(self):
        # self.cursor.execute("""SELECT * FROM sqlite_sequence WHERE name='orders'""")
        self.cursor.execute("""SELECT MAX(order_id) FROM orders""")
        val = self.cursor.fetchone()
        order_id = 0
        if val[0] == None:
            order_id = 1
        elif val[0] == 0:
            order_id = 1
        else:
            order_id = val[0] + 1
        return order_id


    def companies_for_orders(self):
        self.cursor.execute("""SELECT DISTINCT company FROM items""")
        comp = self.cursor.fetchall()
        return comp



    def PutOrder(self,vals,weight,cost,extra):
        comp_name = vals['company']
        date = vals['date']

        try:
            self.cursor.execute("""INSERT INTO orders(order_id,company,order_weight,order_cost,extra_charges,dates,status)
                                VALUES(Null,?,?,?,?,?,'processed')""",
                                (comp_name,weight,cost,extra,date)
                                )
            self.conn.commit()
        except Exception as e:
            return e



    def PutOrderDetail(self,data_list,order_weight,order_amount,extra):
        date = data_list[0]['date']

        try:
            self.PutOrder(data_list[0],order_weight,order_amount,extra)
        except Exception as e:
            return False


        self.cursor.execute("SELECT MAX(order_id) FROM orders")
        o_id = self.cursor.fetchone()[0]

        total_items = len(data_list[1:])
        extra_charge_kg = (extra / order_weight)
        print(extra,extra_charge_kg)
        for n in data_list[1:]:
            code = n['code']
            weight = n['weight']
            cost = n['cost'] + extra_charge_kg


            try:
                average_cost = 0
                self.cursor.execute("SELECT avg_cost,current_weight FROM items WHERE item_id = ?", (code,))
                current = self.cursor.fetchone()
                current_weight = current[1]
                avg_cost = current[0]

                if current_weight <= 0:
                    average_cost = cost
                else:
                    average_cost = ((current_weight*avg_cost) + (weight*cost))/(current_weight+weight)
                    print(average_cost)

                self.cursor.execute("""INSERT INTO items_desc(item_id,cost,weight,dates,order_id,status) Values(?,?,?,?,?,?)""",
                                    (code,cost,weight,date,o_id,"processed"))

                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?),avg_cost = ?
                                    WHERE item_id = ?""",(weight,average_cost,code))
                self.conn.commit()
            except Exception as e:
                print(e)
                return False





    #getting order information
    def order_info(self,id):
        try:
            self.cursor.execute("""SELECT * FROM orders WHERE order_id = ?""",(id,))
            vals = self.cursor.fetchone()
            return vals
        except Exception as e:
            return e

    def CancelOrder(self, ord_id):
        self.cursor.execute("""SELECT extra_charges,order_weight FROM orders WHERE order_id = ?""",(ord_id,))
        org = self.cursor.fetchone()
        extra_chrg = org[0]
        weight = org[1]
        self.cursor.execute("SELECT * FROM items_desc WHERE order_id = ?",(ord_id,))
        vals = self.cursor.fetchall()
        tot_items = len(vals)
        extra_div = extra_chrg/weight

        try:
            self.cursor.execute("""UPDATE orders SET status = ? WHERE order_id = ?""",("Cancelled", ord_id))

            for val in vals:
                item_id = val[0]
                comp_cost = val[1]
                comp_weight = val[2]
                cost = comp_cost + extra_div

                self.cursor.execute("""UPDATE items SET avg_cost = (avg_cost*2 - ?), current_weight = (current_weight - ?)
                                       WHERE item_id = ?""", (cost,comp_weight,item_id,))
                self.cursor.execute("UPDATE items_desc SET status = ? WHERE item_id = ?", ("Cancelled", item_id))
                self.conn.commit()

                self.cursor.execute("SELECT current_weight FROM items WHERE item_id = ?",(item_id,))
                chk_weight = self.cursor.fetchone()[0]

                if chk_weight == 0:
                    self.cursor.execute("""UPDATE items SET avg_cost = 0 WHERE item_id = ?""",(item_id,))
                    self.conn.commit()


        except Exception as e:
            print(e)
            return False




    def OrderResults(self,year,month,comp):
        results = 0
        data = []
        if year == 'Since Start' and month == 'All' and comp == 'All':
            self.cursor.execute("SELECT * FROM orders WHERE status = 'processed'")
            data = self.cursor.fetchall()
            results = len(data)
        elif year == 'Since Start' and comp == 'All' and month != 'All':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{month[:3]}%' """)
            data = self.cursor.fetchall()
            results = len(data)

        elif year == 'Since Start' and month == 'All' and comp != 'All':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and company LIKE '%{comp}%' """)
            data = self.cursor.fetchall()
            results = len(data)

        elif year == 'Since Start' and comp != 'All' and month != 'All':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{month[:3]}%'
                                   and company LIKE '%{comp}%'
                                    """)
            data = self.cursor.fetchall()
            results = len(data)

        elif month == 'All' and comp == 'All' and year != 'Since Start':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{year}%' """)
            data = self.cursor.fetchall()
            results = len(data)

        elif month == 'All' and comp != 'All' and year != 'Since Start':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{year}%'
                                               and company LIKE '%{comp}%'
                                                """)
            data = self.cursor.fetchall()
            results = len(data)

        elif comp == 'All' and month == 'All' and year != 'Since Start':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{year}%'""")
            data = self.cursor.fetchall()
            results = len(data)

        elif comp == 'All' and year == 'Since Start' and month != 'All':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and dates LIKE '%{month[:3]}%'""")
            data = self.cursor.fetchall()
            results = len(data)

        elif comp == 'All' and year != 'Since Start' and month != 'All':
            self.cursor.execute(f"""SELECT * FROM orders WHERE status = 'processed' and (dates LIKE '%{year}%' and dates LIKE '%{month[:3]}%')""")
            data = self.cursor.fetchall()
            results = len(data)

        else:
            self.cursor.execute(
                f"""SELECT * FROM orders WHERE status = 'processed' and (dates LIKE '%{year}%' and dates LIKE '%{month[:3]}%'
                                                                    and company LIKE '%{comp}%') """)
            data = self.cursor.fetchall()
            results = len(data)


        return results,data

    def OrderItems(self,id):
        self.cursor.execute("SELECT COUNT(*) FROM items_desc WHERE order_id = ?",(id,))
        val = self.cursor.fetchone()[0]
        return val


    def OrderItemsDetail(self,id):
        self.cursor.execute("SELECT * FROM items_desc WHERE order_id = ?", (id,))
        vals = self.cursor.fetchall()
        return vals



    #todo admin profit

    def GetProfit(self,year,month):
        try:
            val = []
            if year == 'Since Start' and month == 'All':
                self.cursor.execute("SELECT bill_revenue,bill_discount FROM bills")
                val = self.cursor.fetchall()
            elif year == 'Since Start' and month != 'All':
                self.cursor.execute(f"""SELECT bill_revenue,bill_discount FROM bills WHERE bill_date LIKE '%{month[:3]}%' """)
                val = self.cursor.fetchall()
            elif month == 'All' and year != 'Since Start':
                self.cursor.execute(f"""SELECT bill_revenue,bill_discount FROM bills WHERE bill_date LIKE '%{year}%' """)
                val = self.cursor.fetchall()
            else:
                self.cursor.execute(f"""SELECT bill_revenue, bill_discount FROM bills WHERE bill_date LIKE '%{month[:3]}%'
                                        and bill_date LIKE '%{year}%' """)
                val = self.cursor.fetchall()

            total_profit = 0
            if val:
                for tup in val:
                    bill_revenue = tup[0]
                    bill_discount = tup[1]
                    bill_profit = bill_revenue - bill_discount
                    total_profit = total_profit + bill_profit

            return total_profit
        except Exception as e:
            return e







#todo Return Bill------------------------------------------------------------------------------------------------------------------------------------------>

    def retrieve_bill(self,id):
        self.cursor.execute("SELECT * FROM bills WHERE bill_id = ?",(id,))
        vals = self.cursor.fetchone()
        return vals

    def CancelBill(self,id,vals,cause,date):
        try:
            self.cursor.execute("SELECT * FROM sales WHERE bill_id = ?",(id,))
            sal = self.cursor.fetchall()
            for tup in sal:
                ids = tup[1]
                weight = tup[3]
                cost = tup[-1]
                self.cursor.execute("SELECT current_weight, avg_cost FROM items WHERE item_id = ?", (ids,))
                itm_val = self.cursor.fetchone()

                print('wieght:', weight)
                print('current weight:', itm_val)
                weighted_cost = ((cost*weight + itm_val[0]*itm_val[1])/(weight+itm_val[0]))
                print(weighted_cost)


                self.cursor.execute("""UPDATE items SET current_weight = (current_weight + ?),
                  avg_cost = ? WHERE item_id = ?""",(weight,weighted_cost,ids))


            self.vals = vals
            self.vals.append(cause)
            self.vals.append(date)
            self.cursor.execute("SELECT bill_amount FROM bills WHERE bill_id = ?", (id,))
            p_id = self.vals[-2]
            canc_amount = self.cursor.fetchone()[0]
            print(p_id, ": ", self.vals[0])
            if p_id !='' or p_id != None:
                self.cursor.execute("UPDATE partner SET current_balance = current_balance+? WHERE p_id = ?", (canc_amount, p_id))
                self.cursor.execute("DELETE FROM partner_account WHERE p_id = ? and bill_no= ?", (p_id, self.vals[0]))
            self.cursor.execute("DELETE FROM bills WHERE bill_id = ?", (id,))

            self.cursor.execute("""INSERT INTO cancelled_bills(bill_id,c_name,c_phone,address,bill_date,bill_amount,bill_due,bill_revenue,
            path_file,p_id,bill_discount,cause,canc_date)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", tuple(self.vals))

            self.conn.commit()
            return True
        except Exception as e:
            print("hi")
            print("error:- ", e)




#todo CashPending-------------------------------------------------------------------------------------------------------------------------->

    def CashPendingShow(self,tree):
        self.cursor.execute("""SELECT bill_id,c_name,c_phone,bill_amount,bill_due-bill_discount,p_id, bill_discount FROM bills WHERE bill_due>? """,(0,))
        vals_ls = self.cursor.fetchall()
        count = 1
        val = []
        for tup in vals_ls:
            if tup[-2] != None:
                continue
           
            val = list(tup)
            paid = val[3] - val[4]
            val.insert(4,paid)
            tree.insert('', 'end', text=count, values=val)
            count +=1

    def CashPendingPay(self, id, pay):
        try:
            self.cursor.execute("UPDATE bills SET bill_due = (bill_due - ?) WHERE bill_id = ?",(pay,id))
            self.conn.commit()
            self.cursor.execute("SELECT bill_due FROM bills WHERE bill_id = ?",(id,))
            return self.cursor.fetchone()[0]

        except Exception as e:
            print("something went wrong....  ", e)



    def CashPendingClearDue(self,ids):
        try:
            self.cursor.execute("UPDATE bills SET bill_due = 0 WHERE bill_id = ?",(ids,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong....")




#todo Add Discount ----------------------------------------------------------------------------------------------------------------------------------------------->

    def add_discount(self,id, disc):
        try:
            self.cursor.execute("UPDATE bills SET bill_discount = (bill_discount + ?) WHERE bill_id = ?", (disc,id))
            self.conn.commit()
        except Exception as e:
            print("something went wrong.. ", e)
            return False




    def backup(self,month,year,no):
        bck = sqlite3.connect(f"Data/database/backups/backup{year}_{month}_{no}.db")
        with bck:
            self.conn.backup(bck, pages=-1, progress=None)

        bck.close()




# todo direct sale--------------------------------------------------------------------------->

    def InsertDirectSale(self,ls, name, phone, date, bill_amount, due, p_id, addr):

        self.bill_revenue = 0

        self.InsertBills(name,phone,date,bill_amount,due,self.bill_revenue,p_id,addr)
        self.bill_val = self.cursor.execute("SELECT MAX(bill_id) FROM bills")
        self.bill_no = self.cursor.fetchone()[0]
        for args in ls:
            self.id = args[0]
            self.cost = args[1]
            self.weight = args[2]
            self.amount = args[3]

            self.original = self.cursor.execute("SELECT avg_cost,current_weight,company FROM items WHERE item_id = ?", (self.id,))
            cost_weight = self.cursor.fetchone()
            self.original_cost = args[4]
            self.sale_profit = self.amount - (self.original_cost*self.weight)
           
            if cost_weight[2].lower() == 'loading-unloading':
                self.sale_profit = self.sale_profit-self.amount
            elif cost_weight[2].lower() == 'transportation':
                self.sale_profit = self.sale_profit-self.amount

            self.cursor.execute("""INSERT INTO sales(bill_id,item_id,cost,weight,amount,sale_profit,cost_at_time)
                                  VALUES(?,?,?,?,?,?,?) """,(self.bill_no,self.id,self.cost,self.weight,self.amount,self.sale_profit,self.original_cost))

            self.bill_revenue = self.bill_revenue + self.sale_profit


        self.cursor.execute("UPDATE bills SET bill_revenue = ? WHERE bill_id = ?",(self.bill_revenue,self.bill_no))
        self.conn.commit()


        if p_id != '':
            self.debit = bill_amount

            #getting Partner Current Balance ------------------------------>
            self.blnc = self.cursor.execute("SELECT current_balance FROM partner WHERE p_id = ?",(p_id,))
            self.part_balance = self.cursor.fetchone()[0]

            if self.part_balance == None:
                self.part_balance = 0
            self.current_balance = self.part_balance
            self.balance_upd = (self.current_balance - self.debit)


            #setting up ledger due-------------------->
            self.due = 0
            if self.current_balance <= 0 or self.current_balance < self.debit:
                self.due = -(self.current_balance - self.debit)


            #setting ledger balance ------------------->
            self.ledg_balance = self.current_balance
            if self.current_balance <= 0:
                self.ledg_balance = 0


            #updating partner current balance----------->
            self.ref = f'BillNo{self.bill_no}'
            self.cursor.execute("UPDATE partner SET current_balance = ? WHERE p_id = ?",(self.balance_upd,p_id))

            self.cursor.execute("""INSERT INTO partner_account(p_id,dates,debit,credit,balance,due,rep_no) VALUES(?,?,?,NULL,?,?,?)""",
                                (p_id,date,self.debit,self.ledg_balance,self.due,self.ref))

            self.conn.commit()




#todo search bill by name or data--------------------------------------------------------------------------------------------------------------------------->

    def search(self,):
        
        try:
            self.cursor.execute(f"""SELECT bill_id, c_name, bill_date FROM bills""")
            val = self.cursor.fetchall()
            return val
        except Exception as e:
            return False

       
  