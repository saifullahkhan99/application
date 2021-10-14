from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PyPDF2 import PdfFileWriter, PdfFileReader
import io,subprocess
from reportlab.lib.pagesizes import letter
import math
import time
import pywintypes
import win32api
import win32print
import os
from tkinter import messagebox
from database import Database as db

data = db('Data/database/database.db')

def close_reader():
    os.system("TASKKILL /F /IM AcroRD32.exe")

def call_printer(pdf_file):
    try:
        win32api.ShellExecute(
            0,
             "print",
            pdf_file,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0)
    except RuntimeError:
        messagebox.showerror("Printer", "Please set a default printer")
        return False
    except Exception as e:
        messagebox.showerror("Printer", "Something went wrong")
        return False

    time.sleep(5)
    close_reader()
# 

def Printer(val,current_time, var_print):
    bill_no = val[0]
    nm = val[1].title()
    bill_phone = val[2]
    bill_addr = val[3]
    bill_date = val[4]
    bill_amount = val[5]
    p_id = val[-3]
    discount = val[-1]
    bill_due = val[6]-discount
    total = bill_amount - discount

    bill_paid = float(f"%.2f"%(total-bill_due))
    if bill_due <= 0:
        bill_paid += bill_due
        bill_due = 0

    

    bill_name = bill_date.split(" ")[0]
    bill_path = f"Data\\bills\\saved\\{bill_name}{bill_no}.pdf"
    if bill_due > 0 and p_id == None:
        bill_path = f"Data\\bills\\pending\\{bill_name}{bill_no}.pdf"
    

    canv = canvas.Canvas(bill_path, pagesize = letter)
    canv.setFont("Helvetica-Bold", 22)
    canv.drawCentredString(2 * inch, 10.5 * inch, "New Ghanchi Steels")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.8 * inch, 10 * inch, "Amreli Autorized Stockist")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.46 * inch, 9.78 * inch, "Prop: Sultan Ali")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.93 * inch, 9.56 * inch, "ByPass Road Mingora Swat")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.2 * inch, 9.34 * inch, "Contact:")

    canv.setFont("Helvetica", 10)
    canv.drawCentredString(2.5 * inch, 9.34 * inch, "03461107444, 03452138865")

    canv.drawImage("Data/pics/pdf_pic.png", 6.35 * inch, 9.35 * inch, width=150, height=130)

    # Ghanchi info separation Line
    canv.line(0, 9 * inch, 10 * inch, 9 * inch)

#----------------------------------------------------------------------------------->


    # canv.setFont("Helvetica", 9)
    canv.setFont("Times-Italic", 9)
    # date
    canv.drawCentredString(5.5 * inch, 8.6 * inch, "Date:")
    canv.line(5.8 * inch, 8.6 * inch, 7.3 * inch, 8.6 * inch)
    canv.setFont("Courier-Bold",10)
    canv.drawCentredString(6.4*inch, 8.62*inch, bill_date)

    # time
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.5 * inch, 8.3 * inch, "Time:")
    canv.line(5.8 * inch, 8.3 * inch, 7.3 * inch, 8.3 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.32*inch, current_time)

    # bill No
    canv.setFont("Times-Italic", 10)
    canv.drawCentredString(5.5 * inch, 8 * inch, "Bill No:")
    canv.line(5.8 * inch, 8 * inch, 7.3 * inch, 8 * inch)
    canv.setFont("Courier-Bold", 9)
    canv.drawCentredString(6.4*inch, 8.02*inch, f"{bill_no}")

    # name
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.6 * inch, "Name:")
    canv.line(1.9 * inch, 8.58 * inch, 3.4 * inch, 8.58 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.62*inch, nm)

    # Phone
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.3 * inch, "Phone:")
    canv.line(1.9 * inch, 8.28 * inch, 3.4 * inch, 8.28 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.345*inch, bill_phone)

    # address
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.55 * inch, 8 * inch, "Address:")
    canv.line(1.9 * inch, 7.98 * inch, 3.4 * inch, 8 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.02*inch, bill_addr)

#------------------------------------------------------------------------------------->





    # billing detail-------------------------------------------------------------------------
    canv.setFillGray(0.98)
    canv.roundRect(1.05*inch,2*inch, 455,390,2,fill = 1)
    canv.setFillGray(0)

    canv.setFont("Helvetica", 9)
    # start Line
    canv.line(1.05*inch,7*inch,7.37*inch,7*inch)
    # SNO
    canv.drawCentredString(1.2*inch,7.05*inch,"S.No")

    # code
    canv.drawCentredString(1.75*inch,7.05*inch, "Code")

    # desc
    canv.drawCentredString(3.1*inch, 7.05*inch, "Description")

    # weight kg
    canv.drawCentredString(4.57*inch, 7.05*inch, "Kilo")

    # weight grams
    canv.drawCentredString(5.37*inch, 7.05*inch, "Gram")

    # cost
    canv.drawCentredString(6.17*inch, 7.05*inch, "Cost")

    # amount
    canv.drawCentredString(6.88*inch, 7.05*inch, "Amount")
    dt = data.bill_detail_for_admin(bill_no)
    sno = 1
    init_height = 6.7*inch
    total_weight = 0
    for tup in dt:
        code = tup[1]
        cost = tup[2]
        weight = tup[3]
        grame, kilo = math.modf(weight)
        x, grams = math.modf(grame * 1000)
        amount = float(f"%.2f" % tup[4])
        man = weight / 50
        item = data.retriev_items_for_admin_bill(code)
        name = item[0].replace(" ", "")
        desc = item[1] + " Steel G60 " + name
        if item[1].lower() == 'commercial':
            desc = item[1] + " Steels " + name
        elif item[1].lower() == 'binding wire':
            desc = item[1]
        elif item[1].lower() == 'loading-unloading':
            desc = item[1]
        elif item[1].lower() == 'transportation':
            desc = item[1]


        canv.drawCentredString(1.2 * inch, init_height, f'{sno}')
        # code
        canv.drawCentredString(1.75 * inch, init_height, f'{code}')
        # desc
        canv.drawCentredString(3.1 * inch, init_height, desc)
        # kg
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(4.57 * inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(4.57*inch, init_height, "-")
        else:
            canv.drawCentredString(4.57 * inch, init_height, f"{kilo}")
            canv.setFont("Helvetica", 5)
            canv.drawCentredString(4.57 * inch, init_height - 0.15 * inch, f"(%.2f man)" % man)
        # gram
        canv.setFont("Helvetica", 9)
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(5.37 * inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(5.37*inch, init_height, "-")
        else:
            canv.drawCentredString(5.37 * inch, init_height, f"{grams}")
        # cost
        canv.drawCentredString(6.17 * inch, init_height, f"{cost}")
        # amount
        canv.drawCentredString(6.88 * inch, init_height, f'{amount:,}')

        total_weight = total_weight + weight
        sno += 1
        init_height -= 0.4 * inch

    tons = total_weight/1000
    canv.rect(1.05 * inch, 1.63 * inch, width=120, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.37 * inch, 1.72 * inch, "weight: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(2.07*inch,1.72*inch, f"%.2f tons" %tons)



    # end line
    # canv.line(1.3*inch,3*inch,7.5*inch,3*inch)

    if p_id == '' or p_id == None:
        # total amount
        canv.rect(5.44 * inch, 1.63 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.7 * inch, "Sub total: ")
        canv.setFont("Courier-Bold", 11)
        bill_tot = float(f"%.2f"%bill_amount)
        canv.drawCentredString(6.73*inch, 1.7*inch, f'{bill_tot:,}')


        # Discount
        canv.rect(5.44 * inch, 1.32 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.4 * inch, "Discount: ")
        canv.setFont("Courier-Bold", 11)
        canv.drawCentredString(6.72 * inch, 1.41 * inch, f'{discount:,}')

        # Total
        canv.rect(5.44 * inch, 1.02 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.1 * inch, "Total: ")
        canv.setFont("Courier-Bold", 11)
        bill_due = float(f"%.2f" % bill_due)
        canv.drawCentredString(6.72*inch, 1.11*inch, f'{total:,}')

        #paid
        canv.rect(5.44 * inch, 0.71 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 0.8 * inch, "Paid: ")
        canv.setFont("Courier-Bold", 11)

        canv.drawCentredString(6.72*inch, 0.81*inch, f'{bill_paid:,}')


        #due
        canv.rect(5.44 * inch, 0.41 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 0.5 * inch, "Due: ")
        canv.setFont("Courier-Bold", 11)
        bill_due = float(f"%.2f" % bill_due)
        canv.drawCentredString(6.72*inch, 0.51*inch, f'{bill_due:,}')
    else:

        canv.rect(5.44 * inch, 1.63 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.7 * inch, "Debited: ")
        canv.setFont("Courier-Bold", 11)
        bill_tot = float(f"%.2f"%bill_amount)
        canv.drawCentredString(6.73*inch, 1.7*inch, f'{bill_tot:,}')




    # finish line
    canv.line(0, 12, 10 * inch, 12)
    # email
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.2 * inch, 2, "Email: amrelisteelswat@gmail.com")
    canv.drawCentredString(7 * inch, 2, "Facebook: facebook.com/amrelisteelswat")

    #sign
    canv.drawCentredString(1.05 * inch, .32*inch, "Sign")
    canv.line(1.2 * inch, .27*inch, 2.5*inch, .27*inch)
    canv.showPage()
    canv.save()

    
    data.bill_path(bill_no,bill_path)

    if var_print == True:
        call_printer(bill_path)


def edit_pdf(id,date,file):
    file_name = file.split('\\')[-1]
    path = f"Data\\bills\\saved\\{file_name}"

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Italic", 9)
    can.drawCentredString(6.44*inch,0.85*inch,f"(Dues Cleared @ {date})")
    can.line(6.15*inch,1.15*inch, 7.27*inch,1.15*inch)
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    x = open(f"{file}","rb")
    existing_pdf = PdfFileReader(x)
    # existing_pdf = PdfFileReader(open(f"{file}", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file

    packet.close()
    outputStream = open(path, "wb")
    output.write(outputStream)
    outputStream.close()
    x.close()
    can.showPage()

    data.bill_path(id, path)

    x = file
    os.remove(x)



def orders(data_list):
    pass
def Orders(data_list):
    file_chk = os.path.isfile('./Data/bills/temp/orders.pdf')
    if file_chk == True:
        os.remove('./Data/bills/temp/orders.pdf')

    canv = canvas.Canvas('Data/bills/temp/orders.pdf', pagesize=letter)
    canv.setFont("Helvetica-Bold", 22)
    canv.drawCentredString(2 * inch, 10.5 * inch, "New Ghanchi Steels")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.8 * inch, 10 * inch, "Amreli Autorized Stockist")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.46 * inch, 9.78 * inch, "Prop: Sultan Ali")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.93 * inch, 9.56 * inch, "ByPass Road Mingora Swat")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.2 * inch, 9.34 * inch, "Contact:")

    canv.setFont("Helvetica", 10)
    canv.drawCentredString(2.5 * inch, 9.34 * inch, "03461107444, 03452138865")

    canv.drawImage("Data/pics/pdf_pic.png", 6.35 * inch, 9.35 * inch, width=150, height=130)

    # Ghanchi info separation Line
    canv.line(0, 9 * inch, 10 * inch, 9 * inch)

    # ----------------------------------------------------------------------------------------------------->

    canv.setFillGray(0.98)
    canv.roundRect(30, 50, 550, 550, 2, fill=1)
    canv.setFillGray(0)

    canv.drawCentredString(0.7 * inch, 8.1 * inch, "Sno")
    canv.drawCentredString(1.4 * inch, 8.1 * inch, "Order No")
    canv.drawCentredString(2.65 * inch, 8.1 * inch, "Date")
    canv.drawCentredString(4.1 * inch, 8.1 * inch, "Company")
    canv.drawCentredString(5.4 * inch, 8.1 * inch, "Items")
    canv.drawCentredString(6.4 * inch, 8.1 * inch, "Weight (tons)")
    canv.drawCentredString(7.5 * inch, 8.1 * inch, "Amount")

    canv.line(30, 7.95 * inch, 580, 7.95 * inch)



    start_height = 7.75 * inch
    page_break_list = [24]
    for j in range(1, 1001):
        val = 24 + (33 * j)
        page_break_list.append(val)


    x  = 1
    total_weight = 0
    total_amount = 0

    for tup in data_list:
        order_no = tup[0]
        company_name = tup[1]
        ord_weight = tup[2]/1000
        ord_amount = float(f"%.2f"%tup[3])
        ord_date = tup[5]
        order_items = data.OrderItems(order_no)

        canv.drawCentredString(0.7 * inch, start_height, f"{x}")
        canv.drawCentredString(1.4 * inch, start_height, f"{order_no}")
        canv.drawCentredString(2.65 * inch, start_height, f"{ord_date}")
        canv.drawCentredString(4 * inch, start_height, f"{company_name}")
        canv.drawCentredString(5.4 * inch, start_height, f"{order_items}")
        canv.drawCentredString(6.4 * inch, start_height, f"{ord_weight}")
        canv.drawCentredString(7.5 * inch, start_height, f'{ord_amount:,}')

        if x in page_break_list:
            canv.showPage()
            canv.setFillGray(0.98)
            canv.roundRect(30, 50, 550, 550, 2, fill=1)
            canv.setFillGray(0)
            start_height = 10.8 * inch

        #incrementing variables----------------->
        start_height = start_height - 0.3 * inch
        total_weight = total_weight + ord_weight
        total_amount = total_amount + ord_amount
        x += 1




    # total weight
    canv.rect(1 * inch, 20, width=200, height=20)
    canv.setFont("Times-Italic", 11)
    canv.drawCentredString(1.5 * inch, 25, "Total Weight: ")
    canv.setFont("Courier-Bold", 12)
    canv.drawCentredString(2.6 * inch, 25, f"{float(f'%.2f'%total_weight)}")

    # total amount
    canv.rect(4 * inch, 20, width=200, height=20)
    canv.setFont("Times-Italic", 11)
    canv.drawCentredString(4.5 * inch, 25, "Total Amount: ")
    canv.setFont("Courier-Bold", 12)
    ord_tot_amount = float(f"%.2f"%total_amount)
    canv.drawCentredString(5.7 * inch, 25, f'{float("%.3f"%ord_tot_amount):,}')

    canv.showPage()
    canv.save()

    call_printer(r'.\Data\bills\temp\orders.pdf')






def AdminBill(datas,current_time,ask_print):
    # file_chk = os.path.isfile('./Data/bills/temp/adminbill.pdf')
    # if file_chk == True:
    #     os.remove('./Data/bills/temp/adminbill.pdf')
    try:
        bill_no = datas[0]
        bill_name = datas[1].title()
        bill_phone = datas[2]
        bill_addr = datas[3]
        bill_date = datas[4]
        p_id = datas[-3]
        bill_amount = float(f"%.2f"%datas[5])
        bill_due = float(f"%.2f"%datas[6])
        bill_revenue = float(f"%.2f"%datas[7])
        bill_discount = float(f"%.2f"%datas[-1])
    except TypeError:
        messagebox.showerror("Bill","The bill does not exist")
        return False


    canv = canvas.Canvas('./Data/bills/temp/adminbill.pdf', pagesize=letter)

    canv.setFont("Helvetica-Bold", 22)
    canv.drawCentredString(2 * inch, 10.5 * inch, "New Ghanchi Steels")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.8 * inch, 10 * inch, "Amreli Autorized Stockist")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.46 * inch, 9.78 * inch, "Prop: Sultan Ali")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.93 * inch, 9.56 * inch, "ByPass Road Mingora Swat")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.2 * inch, 9.34 * inch, "Contact:")

    canv.setFont("Helvetica", 10)
    canv.drawCentredString(2.5 * inch, 9.34 * inch, "03461107444, 03452138865")

    canv.drawImage("Data/pics/pdf_pic.png", 6.35 * inch, 9.35 * inch, width=150, height=130)

    # Ghanchi info separation Line
    canv.line(0, 9 * inch, 10 * inch, 9 * inch)

    # ----------------------------------------------------------------------------------->

    # canv.setFont("Helvetica", 9)
    canv.setFont("Times-Italic", 9)
    # date
    canv.drawCentredString(5.5 * inch, 8.6 * inch, "Date:")
    canv.line(5.8 * inch, 8.6 * inch, 7.3 * inch, 8.6 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.62*inch, bill_date)

    # time
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.5 * inch, 8.3 * inch, "Time:")
    canv.line(5.8 * inch, 8.3 * inch, 7.3 * inch, 8.3 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.32*inch, current_time)

    # bill No
    canv.setFont("Times-Italic", 10)
    canv.drawCentredString(5.5 * inch, 8 * inch, "Bill No:")
    canv.line(5.8 * inch, 8 * inch, 7.3 * inch, 8 * inch)
    canv.setFont("Courier-Bold", 9)
    canv.drawCentredString(6.4*inch, 8.02*inch, f"{bill_no}")

    # name
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.6 * inch, "Name:")
    canv.line(1.9 * inch, 8.58 * inch, 3.4 * inch, 8.58 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.62*inch, bill_name)

    # Phone
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.3 * inch, "Phone:")
    canv.line(1.9 * inch, 8.28 * inch, 3.4 * inch, 8.28 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.345*inch, bill_phone)

    # address
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.55 * inch, 8 * inch, "Address:")
    canv.line(1.9 * inch, 7.98 * inch, 3.4 * inch, 8 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.02*inch, bill_addr)

    # ------------------------------------------------------------------------------------->

    # billing detail-------------------------------------------------------------------------
    canv.setFillGray(0.98)
    canv.roundRect(1.05 * inch, 2 * inch, 455, 390, 2, fill=1)
    canv.setFillGray(0)

    canv.setFont("Helvetica", 9)
    # start Line
    canv.line(1.05 * inch, 7 * inch, 7.37 * inch, 7 * inch)
    # SNO
    canv.drawCentredString(1.2 * inch, 7.05 * inch, "S.No")

    # code
    canv.drawCentredString(1.75 * inch, 7.05 * inch, "Code")

    # desc
    canv.drawCentredString(3.1 * inch, 7.05 * inch, "Description")

    # weight kg
    canv.drawCentredString(4.57 * inch, 7.05 * inch, "Kilo")

    # weight grams
    canv.drawCentredString(5.37 * inch, 7.05 * inch, "Gram")

    # cost
    canv.drawCentredString(6.17 * inch, 7.05 * inch, "Cost")

    # amount
    canv.drawCentredString(6.88 * inch, 7.05 * inch, "Amount")
    dt = data.bill_detail_for_admin(bill_no)
    sno = 1
    init_height = 6.7*inch
    total_weight = 0
    for tup in dt:
        code = tup[1]
        cost = tup[2]
        weight = tup[3]
        grame,kilo = math.modf(weight)
        x,grams = math.modf(grame*1000)
        amount = float(f"%.2f"%tup[4])
        man = weight/50
        item = data.retriev_items_for_admin_bill(code)
        name = item[0].replace(" ","")
        desc = item[1] + " Steel G60 " + name
        if item[1].lower() == 'commercial':
            desc = item[1] + " Steels " + name
        elif item[1].lower() == 'binding wire':
            desc = item[1]
        elif item[1].lower() == 'loading-unloading':
            desc = item[1]
        elif item[1].lower() == 'transportation':
            desc = item[1]
        total_weight = total_weight + weight

        #sno
        canv.drawCentredString(1.2*inch, init_height,f'{sno}')
        #code
        canv.drawCentredString(1.75*inch, init_height, f'{code}')
        #desc
        canv.drawCentredString(3.1*inch, init_height, desc)
        #kg
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(4.57*inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(4.57*inch, init_height, "-")
        else:
            canv.drawCentredString(4.57*inch, init_height, f"{kilo}")

            canv.setFont("Helvetica", 5)
            canv.drawCentredString(4.57*inch,init_height-0.15*inch, f"(%.2f man)" %man)
        #gram
        canv.setFont("Helvetica", 9)
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(5.37*inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(5.37*inch, init_height, "-")
        else:
            canv.drawCentredString(5.37 * inch, init_height, f"{grams}")

        #cost
        canv.drawCentredString(6.17*inch, init_height, f"{cost}")
        #amount
        canv.drawCentredString(6.88*inch, init_height, f'{amount:,}')

        sno +=1
        init_height -= 0.4*inch

    tons = total_weight/1000
    canv.rect(1.05 * inch, 1.63 * inch, width=120, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.37 * inch, 1.72 * inch, "weight: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(2.07*inch,1.72*inch, f"%.2f tons" %tons)

    # discount
    canv.rect(1.05 * inch, 1.32 * inch, width=120, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.4 * inch, 1.4 * inch, "Discount: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(2.2 * inch, 1.4 * inch, f'{bill_discount:,}')

    # profit
    canv.rect(1.05 * inch, 1.02 * inch, width=120, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.37 * inch, 1.1 * inch, "Profit: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(2.2 * inch, 1.11 * inch, f"{float('%.2f'%(bill_revenue)):,}")

    if p_id == '' or p_id == None:
        # total amount
        canv.rect(5.44 * inch, 1.63 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.7 * inch, "Total Amount: ")
        canv.setFont("Courier-Bold", 11)
        canv.drawCentredString(6.73*inch, 1.7*inch, f'{bill_amount:,}')

        # paid
        canv.rect(5.44 * inch, 1.32 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.4 * inch, "Paid: ")
        canv.setFont("Courier-Bold", 11)
        canv.drawCentredString(6.72 * inch, 1.41 * inch,f"{bill_amount-bill_due}")

        # Due
        canv.rect(5.44 * inch, 1.02 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.1 * inch, "Due: ")
        canv.setFont("Courier-Bold", 11)
        canv.drawCentredString(6.72*inch, 1.11*inch, f'{bill_due:,}')
    else:
        canv.rect(5.44 * inch, 1.63 * inch, width=140, height=20)
        canv.setFont("Times-Italic", 9)
        canv.drawCentredString(5.82 * inch, 1.7 * inch, "Debited: ")
        canv.setFont("Courier-Bold", 11)
        canv.drawCentredString(6.73*inch, 1.7*inch, f'{bill_amount:,}')


    # finish line
    canv.line(0, 12, 10 * inch, 12)
    # email
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.2 * inch, 2, "Email: amrelisteelswat@gmail.com")
    canv.drawCentredString(7 * inch, 2, "Facebook: facebook.com/amrelisteelswat")

    # sign
    canv.drawCentredString(5.52 * inch, .32 * inch, "Sign")
    canv.line(5.67 * inch, .27 * inch, 7.37 * inch, .27 * inch)

    canv.showPage()
    canv.save()

    if ask_print == True:
        call_printer(r'.\Data\bills\\temp\\adminbill.pdf')
    else:
        subprocess.Popen([r".\Data\bills\\temp\\adminbill.pdf"], shell=True)






def OrderDetail(datas,current_time):
    file_chk = os.path.isfile(r'.\Data\bills\\temp\DetailOrder.pdf')
    if file_chk == True:
        os.remove(r'.\Data\bills\\temp\DetailOrder.pdf')



    order_no = datas[0]
    company_name = datas[1]
    order_weight = datas[2]
    order_amount = float(f"%.2f"%datas[3])
    order_extra = datas[4]
    order_date = datas[5]

    canv = canvas.Canvas(r'.\Data\bills\temp\DetailOrder.pdf', pagesize=letter)

    canv.setFont("Helvetica-Bold", 22)
    canv.drawCentredString(2 * inch, 10.5 * inch, "New Ghanchi Steels")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.8 * inch, 10 * inch, "Amreli Autorized Stockist")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.46 * inch, 9.78 * inch, "Prop: Sultan Ali")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.93 * inch, 9.56 * inch, "ByPass Road Mingora Swat")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.2 * inch, 9.34 * inch, "Contact:")

    canv.setFont("Helvetica", 10)
    canv.drawCentredString(2.5 * inch, 9.34 * inch, "03461107444, 03452138865")

    canv.drawImage("Data/pics/pdf_pic.png", 6.35 * inch, 9.35 * inch, width=150, height=130)

    # Ghanchi info separation Line
    canv.line(0, 9 * inch, 10 * inch, 9 * inch)

    # ----------------------------------------------------------------------------------->

    # canv.setFont("Helvetica", 9)
    canv.setFont("Times-Italic", 9)
    # date
    canv.drawCentredString(5.5 * inch, 8.6 * inch, "Date:")
    canv.line(5.8 * inch, 8.6 * inch, 7.3 * inch, 8.6 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.62*inch, order_date)

    # time
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.5 * inch, 8.3 * inch, "Time:")
    canv.line(5.8 * inch, 8.3 * inch, 7.3 * inch, 8.3 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.32*inch, current_time)

    # company name
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.6 * inch, "Company: ")
    canv.line(1.9 * inch, 8.58 * inch, 3.4 * inch, 8.58 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.62*inch, company_name)

    # Bill no
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.3 * inch, "Order No: ")
    canv.line(1.9 * inch, 8.28 * inch, 3.4 * inch, 8.28 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.345*inch, f"{order_no}")

    # ------------------------------------------------------------------------------------->

    # billing detail-------------------------------------------------------------------------
    canv.setFillGray(0.98)
    canv.roundRect(1.05 * inch, 2 * inch, 455, 430, 2, fill=1)
    canv.setFillGray(0)

    canv.setFont("Helvetica", 9)
    # start Line
    canv.line(1.05 * inch, 7.68 * inch, 7.37 * inch, 7.68 * inch)
    # SNO
    canv.drawCentredString(1.2 * inch, 7.75 * inch, "S.No")

    # code
    canv.drawCentredString(1.75 * inch, 7.75 * inch, "Code")

    # desc
    canv.drawCentredString(3.1 * inch, 7.75 * inch, "Description")

    # weight kg
    canv.drawCentredString(4.57 * inch, 7.75 * inch, "Kilo")

    # weight grams
    canv.drawCentredString(5.37 * inch, 7.75 * inch, "Gram")

    # cost
    canv.drawCentredString(6.17 * inch, 7.75 * inch, "Cost")

    # amount
    canv.drawCentredString(6.88 * inch, 7.75 * inch, "Amount")


    vals = data.OrderItemsDetail(order_no)
    sno = 1
    init_height = 7.4*inch
    total_weight = 0
    for tup in vals:
        code = tup[0]
        cost = float(f"%.2f"%tup[1])
        weight = tup[2]
        grame,kilo = math.modf(weight)
        x,grams = math.modf(grame*1000)
        amount = float(f"%.2f"%(cost*weight))
        man = weight/50
        item = data.retriev_items_for_admin_bill(code)
        name = item[0].replace(" ","")
        desc = item[1] + " Steel G60 " + name
        if item[1].lower() == 'commercial':
            desc = item[1] + " Steels " + name
        elif item[1].lower() == 'binding wire':
            desc = item[1]
        elif item[1].lower() == 'loading-unloading':
            desc = item[1]
        elif item[1].lower() == 'transportation':
            desc = item[1]
        total_weight = total_weight + weight

        #sno
        canv.drawCentredString(1.2*inch, init_height,f'{sno}')
        #code
        canv.drawCentredString(1.75*inch, init_height, f'{code}')
        #desc
        canv.drawCentredString(3.1*inch, init_height, desc)
        #kg
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(4.57*inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(4.57*inch, init_height, "-")
        else:
            canv.drawCentredString(4.57 * inch, init_height, f"{kilo}")

            canv.setFont("Helvetica", 5)
            canv.drawCentredString(4.57*inch,init_height-0.15*inch, f"(%.2f man)" %man)
        #gram
        canv.setFont("Helvetica", 9)
        if item[1].lower() == 'loading-unloading':
            canv.drawCentredString(5.37*inch, init_height, "-")
        elif item[1].lower() == 'transportation':
            canv.drawCentredString(5.37*inch, init_height, "-")
        else:
            canv.drawCentredString(5.37 * inch, init_height, f"{grams}")

        #cost
        canv.drawCentredString(6.17*inch, init_height, f"{cost}")
        #amount
        canv.drawCentredString(6.88*inch, init_height, f'{amount:,}')

        sno +=1
        init_height -= 0.4*inch

    canv.rect(1.05 * inch, 1.63 * inch, width=120, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.37 * inch, 1.72 * inch, "weight: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(2.07*inch,1.72*inch, f"%.2f tons"%(order_weight/1000))


    # total amount
    canv.rect(5.44 * inch, 1.63 * inch, width=140, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.82 * inch, 1.7 * inch, "Total Amount: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(6.73*inch, 1.7*inch, f'{order_amount:,}')

    # extra charges
    canv.rect(5.44 * inch, 1.32 * inch, width=140, height=20)
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.82 * inch, 1.4 * inch, "Extra: ")
    canv.setFont("Courier-Bold", 11)
    canv.drawCentredString(6.72 * inch, 1.41 * inch, f"%.2f" % order_extra)


    # finish line
    canv.line(0, 12, 10 * inch, 12)
    # email
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.2 * inch, 2, "Email: amrelisteelswat@gmail.com")
    canv.drawCentredString(7 * inch, 2, "Facebook: facebook.com/amrelisteelswat")

    # sign
    canv.drawCentredString(5.52 * inch, .32 * inch, "Sign")
    canv.line(5.67 * inch, .27 * inch, 7.37 * inch, .27 * inch)

    canv.showPage()
    canv.save()

    call_printer(r'.\Data\bills\temp\DetailOrder.pdf')









def ledger(frame,data_list,date):

    ask = messagebox.askyesno("print", "are you sure want to print?", parent = frame)
    if ask == False:
        return False


    partner_id = data_list[0]
    partner_name = data_list[1].title()

    
    current_date = date
    phone = "0"+str(data_list[2])
    address = data_list[3]
    print(phone)


    canv = canvas.Canvas(r'.\Data\bills\\temp\\ledger.pdf', pagesize=letter)

    canv.setFont("Helvetica-Bold", 22)
    canv.drawCentredString(2 * inch, 10.5 * inch, "New Ghanchi Steels")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.8 * inch, 10 * inch, "Amreli Autorized Stockist")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.46 * inch, 9.78 * inch, "Prop: Sultan Ali")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.93 * inch, 9.56 * inch, "ByPass Road Mingora Swat")

    canv.setFont("Helvetica", 12)
    canv.drawCentredString(1.2 * inch, 9.34 * inch, "Contact:")

    canv.setFont("Helvetica", 10)
    canv.drawCentredString(2.5 * inch, 9.34 * inch, "03461107444, 03452138865")

    canv.drawImage("Data/pics/pdf_pic.png", 6.35 * inch, 9.35 * inch, width=150, height=130)

    # Ghanchi info separation Line
    canv.line(0, 9 * inch, 10 * inch, 9 * inch)

    # ----------------------------------------------------------------------------------->

    # canv.setFont("Helvetica", 9)
    canv.setFont("Times-Italic", 9)
    # date
    canv.drawCentredString(5.5 * inch, 8.6 * inch, "Date:")
    canv.line(5.8 * inch, 8.6 * inch, 7.3 * inch, 8.6 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.62*inch, current_date)

    # adddress
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(5.5 * inch, 8.3 * inch, "Address:")
    canv.line(5.8 * inch, 8.3 * inch, 7.3 * inch, 8.3 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(6.4*inch, 8.32*inch, address)

    # Partner name
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.6 * inch, "Name: ")
    canv.line(1.9 * inch, 8.58 * inch, 3.4 * inch, 8.58 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.62*inch, partner_name)

    # contact
    canv.setFont("Times-Italic", 9)
    canv.drawCentredString(1.5 * inch, 8.3 * inch, "Contact No: ")
    canv.line(1.9 * inch, 8.28 * inch, 3.4 * inch, 8.28 * inch)
    canv.setFont("Courier-Bold", 10)
    canv.drawCentredString(2.5*inch, 8.345*inch, f"{phone}")


#rectagle


    
    canv.setFillGray(0.98)
    canv.roundRect(18, 40, 565, 540, 2, fill=1)
    canv.setFillGray(0)

    # canv.drawCentredString(0.7 * inch, 7.7 * inch, "Sno")
    canv.drawCentredString(0.8 * inch, 7.7 * inch, "Date")
    canv.drawCentredString(1.8 * inch, 7.7 * inch, "Reference")
    canv.drawCentredString(1.8 * inch, 7.55 * inch, "(Doc)")
    canv.drawCentredString(2.7 * inch, 7.7 * inch, "Sales")
    canv.drawCentredString(2.7 * inch, 7.55 * inch, "(tons)")
    canv.drawCentredString(3.6 * inch, 7.7 * inch, "Debit")
    canv.drawCentredString(4.8 * inch, 7.7 * inch, "Credit")
    canv.drawCentredString(6 * inch, 7.7 * inch, "Balance")
    canv.drawCentredString(7.3 * inch, 7.7 * inch, "Due")

    canv.line(25, 7.5 * inch, 575, 7.5 * inch)



    start_height = 7.3 * inch
    page_break_list = [23]
    for j in range(1, 1001):
        val = 24 + (31 * j)
        page_break_list.append(val)

    vals = data.ledger(partner_id)
    x  = 1
    total_weight = 0
    total_debit = 0
    total_credit = 0

    for tups in vals:
        
        account_date = tups[1]
        debit = tups[2]
        sale = 0
        credit = tups[3]
        balance = tups[4]
        due = tups[5]
        ref_no = tups[6]
        bill = tups[7]

        if credit == None:
            credit = 0
        if debit == None:
            debit = 0
        if due == None:
            due = 0
        if bill != None:
            if debit >=0:
                sale_detail = data.bill_detail_for_admin(bill)
                for tup in sale_detail:
                    sale = (sale+tup[3]/1000)
        total_weight = (total_weight + sale)




        canv.setFont("Courier", 9)

        canv.drawCentredString(0.8 * inch, start_height, f"{account_date}")
        canv.drawCentredString(1.8 * inch, start_height, f"{ref_no}")
        canv.drawCentredString(2.7 * inch, start_height, f"%.3f"%sale)
        canv.drawCentredString(3.6 * inch, start_height, f"%.2f"%debit)
        canv.drawCentredString(4.8 * inch, start_height, f"%.2f"%float(credit))
        canv.drawCentredString(6 * inch, start_height, f"%.2f"%balance)
        canv.drawCentredString(7.3 * inch, start_height, f"%.2f"%due)

        if x in page_break_list:
            canv.showPage()
            canv.setFillGray(0.98)
            canv.roundRect(18, 50, 560, 700, 2, fill=1)
            canv.setFillGray(0)
            start_height = 10.5 * inch

        canv.setFont("Courier-Bold", 10)

    #     #incrementing variables----------------->
        start_height = start_height - 0.3 * inch
        total_debit = total_debit + debit
        total_credit = total_credit + credit
        x += 1



    partner_get_balance = data.partner_balance(partner_id)[0]
    partner_balance = 0
    partner_due = 0

    if partner_get_balance < 0:
        partner_due = -(partner_get_balance)
    else:
        partner_balance = partner_get_balance



    # for x <=23
    if x<=24:
        canv.setFillGray(0.9)
        canv.roundRect(120, 15, 462, 23, 2, fill=1)
        canv.setFillGray(0)
        
        # total weight  
       

        canv.setFont("Times-Italic", 11)
        canv.drawCentredString(1.95 * inch, 20, "Total : ")
        
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(2.7 * inch, 20, f"{float('%.2f'%total_weight)}")

        # # total debit
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(3.6 * inch, 20, f'{float("%.3f"%total_debit):,}')

        # total credit
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(4.8 * inch, 20, f'{float("%.3f"%total_credit):,}')

        # total balance
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(6 * inch, 20, f'{float("%.3f"%partner_balance):,}')

        # total due
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(7.3 * inch, 20, f'{float("%.3f"%partner_due):,}')



    
    else:
        canv.setFillGray(0.9)
        canv.roundRect(120, 20, 462, 25, 2, fill=1)
        canv.setFillGray(0)


        canv.setFont("Times-Italic", 11)
        canv.drawCentredString(1.95 * inch, 25, "Total : ")
        
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(2.7 * inch, 25, f"{float('%.2f'%total_weight)}")

        # # total debit
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(3.6 * inch, 25, f'{float("%.3f"%total_debit):,}')

        # total credit
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(4.8 * inch, 25, f'{float("%.3f"%total_credit):,}')

        # total balance
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(6 * inch, 25, f'{float("%.3f"%partner_balance):,}')

        # total due
        canv.setFont("Courier-Bold", 9)
        canv.drawCentredString(7.3 * inch, 25, f'{float("%.3f"%partner_due):,}')

    canv.showPage()
    canv.save()

    call_printer(r'.\Data\bills\\temp\\ledger.pdf')



 