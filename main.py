import customtkinter
import sqlite3
import bcrypt
import os
import webbrowser
import send_email
from tkinter import *
from tkinter import messagebox, ttk
from pdf_format import Payslip

app = customtkinter.CTk()
app.title('Employee Payroll System')
app.geometry('650x360')
app.config(bg='#001220')

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold', 'underline')
font5 = ('Arial', 30, 'bold')
font6 = ('Arial', 20)
font7 = ('Arial', 15)

def create_tables():
    con = sqlite3.connect('data.db')
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                   username TEXT NOT NULL,
                   password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empdetails (
                   empid INT(11) PRIMARY KEY,
                   firstname TEXT NOT NULL,
                   surname TEXT NOT NULL,
                   birthdate TEXT NOT NULL,
                   gender TEXT NOT NULL,
                   department TEXT NOT NULL,
                   job TEXT NOT NULL,
                   civil TEXT NOT NULL,
                   datehired TEXT NOT NULL,
                   salary REAL,
                   email TEXT NOT NULL,
                   contact TEXT NOT NULL,
                   postal INT,
                   address TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empcontributions (
                    empid INT(11) PRIMARY KEY,
                    rate REAL,
                    paydate TEXT NOT NULL,
                    fromdate TEXT NOT NULL,
                    todate TEXT NOT NULL,
                    workingdays TEXT NOT NULL,
                    absent TEXT NOT NULL,
                    totalworkingdays TEXT NOT NULL,
                    grosspay REAL,
                    tax REAL,
                    deductions REAL,
                    totalcontributions REAL,
                    netpay REAL,
                    sss REAL,
                    pagibig REAL,
                    philhealth REAL,
                    FOREIGN KEY (empid) REFERENCES empdetails(empid)
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emppayslip (
                    empid INT(11) PRIMARY KEY,
                    payslip TEXT,
                    FOREIGN KEY (empid) REFERENCES empdetails(empid)              
    )
    ''')

    con.commit()
    con.close()

#==SIGNUP FUNCTIONS=================

def signup():
    username = username_entry.get()
    password = password_entry.get()
    confirm = confirm_entry.get()
    
    if password == confirm:
        if username != '' and password != '':
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute('SELECT username FROM users WHERE username = ?', [username])
            if cursor.fetchone() is not None:
                messagebox.showerror('Error', 'Username already exists.')
            else:
                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                print(hashed_password)
                cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hashed_password])
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Account has been created.')
        else:
            messagebox.showerror('Error', 'Enter all data.')
    else:
        messagebox.showerror('Error', 'Not the same password.')

#================

#==LOGIN FUNCTIONS===========

def login_account():
    username = username_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('SELECT password FROM users where username = ?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'Logged in successfully.')
                frame2.destroy()
                app.geometry('1200x650')
                Employee_System()
            else:
                messagebox.showerror('Error', 'Invalid password.')
        else:
            messagebox.showerror('Error', 'Invalid username.')
    else:
        messagebox.showerror('Error', 'Enter all data.')

#==============
#==LOGIN FRAME==

def login():
    frame1.destroy()
    global frame2
    frame2 = customtkinter.CTkFrame(app, bg_color = '#001220', fg_color = '#001220', width = 470, height = 360)
    frame2.place(x = 0, y = 0)

    #image1 = PhotoImage(file = "1.png")
    #image1_label = Label (frame2, image = image1 , bg = '#001220')
    #image1_label.place(x = 0, y = 0)
    #frame2.image1 = image1

    login_label = customtkinter.CTkLabel(frame2, font = font1, text = 'Log in', text_color = '#fff', bg_color = '#001220')
    login_label.place(x = 280, y = 20)
    
    global username_entry2
    global password_entry2

    username_entry2 = customtkinter.CTkEntry(frame2, font = font2, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color = '#004780', border_width = 3, placeholder_text = 'Username', placeholder_text_color = '#a3a3a3', width = 200, height = 50)
    username_entry2.place(x = 230, y = 80)

    password_entry2 = customtkinter.CTkEntry(frame2, font = font2, show = '*', text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color = '#004780', border_width = 3, placeholder_text = 'Password', placeholder_text_color = '#a3a3a3', width = 200, height = 50)
    password_entry2.place(x = 230, y = 150)

    login_button = customtkinter.CTkButton(frame2, command = login_account,font = font2, text_color = '#fff', text = 'Log in', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = 'hand2', corner_radius = 5, width = 120)
    login_button.place(x = 230, y = 220)

#==============================
#==Signup Frame==

frame1 = customtkinter.CTkFrame(app, bg_color = '#001220', fg_color = '#001220', width = 470, height = 360)
frame1.place(x = 0, y = 0)

signup_label = customtkinter.CTkLabel(frame1, font = font1, text = 'Sign Up', text_color = '#fff', bg_color = '#001220')
signup_label.place(x = 280, y = 20)

username_entry = customtkinter.CTkEntry(frame1, font = font2, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, placeholder_text = 'Username', placeholder_text_color = '#a3a3a3', width = 200, height = 50)
username_entry.place(x = 230, y = 80)

password_entry = customtkinter.CTkEntry(frame1, font = font2, show = "*", text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color = '#004780', border_width = 3, placeholder_text = 'Password', placeholder_text_color = '#a3a3a3', width = 200, height = 50)
password_entry.place(x = 230, y = 150)

confirm_entry = customtkinter.CTkEntry(frame1, font = font2, show = "*", text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color = '#004780', border_width = 3, placeholder_text = 'Confirm Password', placeholder_text_color = '#a3a3a3', width = 200, height = 50)
confirm_entry.place(x = 230, y = 220)

signup_button = customtkinter.CTkButton(frame1, command = signup,font = font2, text_color= "#fff", text = 'Sign Up', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 120)
signup_button.place(x = 230, y = 290)

login_label = customtkinter.CTkLabel(frame1, font = font3, text = 'Already have an account?', text_color = '#fff', bg_color = '#001220')
login_label.place(x = 230, y = 320)

login_button = customtkinter.CTkButton(frame1, command = login, font = font4, text_color = '#00bf77', text = 'Login', fg_color = '#001220', hover_color = '#001220', cursor = "hand2", width = 40)
login_button.place(x = 395, y = 320)

#=============================
#==Employee Detail Functions==

def emp_detail_add():
    empid = empid_entry.get()
    fn = fn_entry.get()
    sn = sn_entry.get()
    birth = birth_entry.get()
    gender = gender_entry.get()
    department = department_entry.get()
    job = job_entry.get()
    civil = civil_entry.get()
    datehired = datehired_entry.get()
    salary = salary_entry.get()
    email = email_entry.get()
    contact = contact_entry.get()
    postal = postal_entry.get()
    address = address_txt.get('1.0', END)    

    if empid == '':
        messagebox.showerror('Error', 'Enter all details required')
    else:
        try:
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM empdetails WHERE empid = ?", [empid])
            row = cursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'This Employee ID already exists within the database!')
            else:
                if int(salary) > 30000:
                    messagebox.showerror('Error', 'Salary must only be 30000 or lower')
                else:
                    cursor.execute("INSERT INTO empdetails VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           [
                               empid,
                               fn,
                               sn,
                               birth,
                               gender,
                               department,
                               job,
                               civil,
                               datehired,
                               salary,
                               email,
                               contact,
                               postal,
                               address
                            ])
                    messagebox.showinfo('Success', 'Employee Details has been added.')
                    con.commit()
                    con.close()
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')

def emp_detail_update():
    empid = empid_entry.get()
    fn = fn_entry.get()
    sn = sn_entry.get()
    birth = birth_entry.get()
    gender = gender_entry.get()
    department = department_entry.get()
    job = job_entry.get()
    civil = civil_entry.get()
    datehired = datehired_entry.get()
    salary = salary_entry.get()
    email = email_entry.get()
    contact = contact_entry.get()
    postal = postal_entry.get()
    address = address_txt.get('1.0', END)

    if empid == '' or salary == '' or fn == '' or sn == '':
        messagebox.showerror('Error', 'Employee details need to be updated')
    else:
        try:
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM empdetails WHERE empid = ?', [empid])
            row = cursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Invalid Employee ID, try another!')
            else:
                if int(salary) > 30000 or float(salary) > 30000:
                    messagebox.showerror('Error', 'Salary must only be 30000 or lower')
                else:
                    cursor.execute('''UPDATE empdetails SET firstname = ?, surname = ?, birthdate = ?, gender = ?, department = ?, job = ?, 
                               civil = ?, datehired = ?, salary = ?, email = ?, contact = ?, postal = ?, address = ? WHERE empid = ?''', 
                               (
                                   fn,
                                   sn,
                                   birth,
                                   gender,
                                   department,
                                   job,
                                   civil,
                                   datehired,
                                   float(salary), 
                                   email,
                                   contact,
                                   postal,
                                   address,
                                   empid
                               ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Employee Records Updated Successfully!")

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')

def emp_detail_delete():
    empid = empid_entry.get()
    if empid == '':
        messagebox.showerror('Error', 'Employee ID is required for deletion!')
    else:
        try:
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM empdetails WHERE empid = ?', [empid])
            cursor.execute('SELECT * FROM empcontributions WHERE empid = ?', [empid])
            row = cursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Invalid Employee ID!')
            else:
                confirm = messagebox.askyesno('Confirm', 'Do you really want to delete this employee?')
                if confirm == True:
                    cursor.execute('DELETE FROM empdetails WHERE empid = ?', [empid])
                    cursor.execute('DELETE FROM empcontributions WHERE empid = ?', [empid])
                    con.commit()
                    con.close()
                    messagebox.showinfo('Deleted', 'Employee record is deleted successfully')

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')

def clear_emp_detail():
    btn_search_emp.configure(state = NORMAL)
    btn_add_emp.configure(state = NORMAL)
    empid_entry.configure(state = NORMAL)
    empid_entry.delete(0, END)
    fn_entry.delete(0, END)
    sn_entry.delete(0, END)
    birth_entry.delete(0, END)
    gender_entry.delete(0, END)
    department_entry.delete(0, END)
    job_entry.delete(0, END)
    civil_entry.delete(0, END)
    datehired_entry.delete(0, END)
    salary_entry.delete(0, END)
    email_entry.delete(0, END)
    contact_entry.delete(0, END)
    postal_entry.delete(0, END)
    address_txt.delete(0.0, "end")

def emp_search():
    empid = empid_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM empdetails WHERE empid = ?", [empid])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Employee ID, try another!')
        else: #print the values into their entries
            btn_search_emp.configure(state = DISABLED)
            btn_add_emp.configure(state = DISABLED)
            empid_entry.configure(state = 'readonly')

            fn_entry.insert(0, row[1])
            sn_entry.insert(0, row[2])
            birth_entry.insert(0, row[3])
            gender_entry.insert(0, row[4])
            department_entry.insert(0, row[5])
            job_entry.insert(0, row[6])
            civil_entry.insert(0, row[7])
            datehired_entry.insert(0, row[8])
            salary_entry.insert(0, row[9])
            email_entry.insert(0, row[10])
            contact_entry.insert(0, row[11])
            postal_entry.insert(0, row[12])
            address_txt.insert(0.0, row[13])
           
    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

def show_employee_details():
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM empdetails")
        rows = cursor.fetchall()
        emp_tree.delete(*emp_tree.get_children())
        for row in rows:
            emp_tree.insert('', END, values = row)
        con.close()

    except Exception as ex:
        messagebox.showerror("Error", f'Error due to {str(ex)}')

#=====Employee Function=====

def Employee_System():

    #==Global Variables==
    #==Entry Variables==
    global empid_entry
    global fn_entry
    global sn_entry
    global birth_entry
    global gender_entry
    global department_entry
    global job_entry
    global civil_entry
    global datehired_entry
    global salary_entry
    global email_entry
    global contact_entry
    global postal_entry
    global address_txt

    #==Buttons==
    global btn_add_emp
    global btn_clear
    global btn_update
    global btn_delete
    global btn_next_salary
    global btn_search_emp

    empdetail_frame = customtkinter.CTkFrame(app, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    empdetail_frame.place(x = 0, y = 0)

    mainFrame1 = customtkinter.CTkFrame(empdetail_frame, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    mainFrame1.place(x = 0, y = 0)

    title = customtkinter.CTkLabel(mainFrame1, text = "Employee Details", font = font5, bg_color = '#000e1a', fg_color = '#000e1a')
    title.place(x = 100, y = 40)

    #==Frame1 Variables==
    #Not needed as customtkinter already has these values stored within the entries themselves
    '''
    var_emp_id = StringVar()
    var_firstname = StringVar()
    var_surname = StringVar()
    var_birthdate = StringVar()
    var_gender = StringVar()
    var_department = StringVar()
    var_job = StringVar()
    var_civil = StringVar()
    var_datehired = StringVar()
    var_basicsalary = StringVar()
    var_address = StringVar()
    var_email = StringVar()
    var_contact = StringVar()
    var_postalcode = StringVar()
    '''

    empid_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Employee ID:', text_color = '#fff', bg_color = '#001220')
    empid_label.place(x = 100, y = 100)

    def only_numbers(char):
        return char.isdigit()
    validation = empdetail_frame.register(only_numbers)

    empid_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200, validate = "key", validatecommand = (validation, '%S'))
    empid_entry.place(x = 250, y = 100)

    noteempid_label = customtkinter.CTkLabel(mainFrame1, font = font7, text = "'If existing employee, input only the employee ID \nto search Employee Details:'", text_color = '#fff', bg_color = '#001220')
    noteempid_label.place(x = 870, y = 25)

    fn_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'First Name:', text_color = '#fff', bg_color = '#001220')
    fn_label.place(x = 100, y = 140)

    fn_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    fn_entry.place(x = 250, y = 140)

    sn_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Surname:', text_color = '#fff', bg_color = '#001220')
    sn_label.place(x = 100, y = 180)

    sn_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    sn_entry.place(x = 250, y = 180)

    birth_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Date of Birth:', text_color = '#fff', bg_color = '#001220')
    birth_label.place(x = 100, y = 220)

    birth_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    birth_entry.place(x = 250, y = 220)

    gender_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Gender:', text_color = '#fff', bg_color = '#001220')
    gender_label.place(x = 100, y = 260)

    gender_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gender_entry.place(x = 250, y = 260)

    department_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Department:', text_color = '#fff', bg_color = '#001220')
    department_label.place(x = 600, y = 100)

    department_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    department_entry.place(x = 750, y = 100)

    job_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Job Title:', text_color = '#fff', bg_color = '#001220')
    job_label.place(x = 600, y = 140)

    job_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    job_entry.place(x = 750, y = 140)

    civil_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Civil Status:', text_color = '#fff', bg_color = '#001220')
    civil_label.place(x = 600, y = 180)

    civil_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    civil_entry.place(x = 750, y = 180)

    datehired_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Date Hired:', text_color = '#fff', bg_color = '#001220')
    datehired_label.place(x = 600, y = 220)

    datehired_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    datehired_entry.place(x = 750, y = 220)

    salary_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Basic Salary:', text_color = '#fff', bg_color = '#001220')
    salary_label.place(x = 600, y = 260)

    salary_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    salary_entry.place(x = 750, y = 260)

    email_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Email:', text_color = '#fff', bg_color = '#001220')
    email_label.place(x = 100, y = 400)

    email_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    email_entry.place(x = 250, y = 400)

    contact_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Contact:', text_color = '#fff', bg_color = '#001220')
    contact_label.place(x = 100, y = 440)

    contact_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    contact_entry.place(x = 250, y = 440)

    postal_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Postal Code:', text_color = '#fff', bg_color = '#001220')
    postal_label.place(x = 100, y = 480)

    postal_entry = customtkinter.CTkEntry(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    postal_entry.place(x = 250, y = 480)

    address_label = customtkinter.CTkLabel(mainFrame1, font = font6, text = 'Address:', text_color = '#fff', bg_color = '#001220')
    address_label.place(x = 100, y = 520)

    address_txt = customtkinter.CTkTextbox(mainFrame1, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200, height = 60)
    address_txt.place(x = 250, y = 520)

#==Buttons==
    btn_search_emp = customtkinter.CTkButton(mainFrame1, command = emp_search, font = font2, text_color= "#fff", text = 'Search Employee', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_search_emp.place(x = 700, y = 20)

    btn_show_emp = customtkinter.CTkButton(mainFrame1, command = show_emp_frame, font = font2, text_color= "#fff", text = 'Show Employees', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_show_emp.place(x = 450, y = 20)

    btn_add_emp = customtkinter.CTkButton(mainFrame1, command = emp_detail_add, font = font2, text_color= "#fff", text = 'Add Details', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_add_emp.place(x = 600, y = 400)

    btn_clear = customtkinter.CTkButton(mainFrame1, command = clear_emp_detail, font = font2, text_color= "#fff", text = 'Clear', fg_color = '#34cbcb', hover_color = '#1f7a7a', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_clear.place(x = 770, y = 400)

    btn_update = customtkinter.CTkButton(mainFrame1, command = emp_detail_update, font = font2, text_color= "#fff", text = 'Update', fg_color = '#ffbb33', hover_color = '#996600', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_update.place(x = 600, y = 470)

    btn_delete = customtkinter.CTkButton(mainFrame1, command = emp_detail_delete, font = font2, text_color= "#fff", text = 'Delete', fg_color = '#ff4d4d', hover_color = '#b30000', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_delete.place(x = 770, y = 470)

    btn_next_salary = customtkinter.CTkButton(mainFrame1, command = Salary_Frame, font = font2, text_color= "#fff", text = 'Salary Computation', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_next_salary.place(x = 680, y = 540)

#===========================
#=====Employee Database Frame=====

def show_emp_frame():
    global emp_tree

    show_emp = customtkinter.CTkToplevel() #makes this section part of the main program
    show_emp.title("EmployeePayroll System")
    show_emp.geometry("1000x500+120+60")
    show_emp.config(bg = "#001220")
    title = Label(show_emp, text="All Employee Details", font = font1, bg = "#001220", fg = "white", anchor = "w", padx = 5)
    title.pack(side = TOP, fill = X)

    scrolly = Scrollbar(show_emp, orient = VERTICAL)
    scrollx = Scrollbar(show_emp, orient = HORIZONTAL)
    scrolly.pack(side = RIGHT, fill = Y)
    scrollx.pack(side = BOTTOM, fill = X)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background = "#001220", fieldbackground = "#001220", foreground = "white", rowheight = 30)
    style.map('Treeview', background = [('selected', '#4b7c94')])
    
    emp_tree = ttk.Treeview(show_emp, xscrollcommand = scrollx.set, yscrollcommand = scrolly.set, 
                            columns = ('empid', 'firstname', 'surname', 'birthdate', 'gender', 'department', 'job', 'civil', 
                                       'datehired', 'salary', 'email', 'contact', 'postal', 'address'))
    emp_tree.heading('empid', text = 'EmpID')
    emp_tree.heading('firstname', text = 'First Name')
    emp_tree.heading('surname', text = 'Surname')
    emp_tree.heading('birthdate', text = 'Birthdate')
    emp_tree.heading('gender', text = 'Gender')
    emp_tree.heading('department', text = 'Department')
    emp_tree.heading('job', text = 'Job')
    emp_tree.heading('civil', text = 'Civil')
    emp_tree.heading('datehired', text = 'Datehired')
    emp_tree.heading('salary', text = 'Salary')
    emp_tree.heading('email', text = 'Email')
    emp_tree.heading('contact', text = 'Contact')
    emp_tree.heading('postal', text = 'Postal')
    emp_tree.heading('address', text = 'Address')
    emp_tree['show'] = 'headings'

    emp_tree.column('empid', width = 40)
    emp_tree.column('firstname', width = 80)
    emp_tree.column('surname', width = 80)
    emp_tree.column('birthdate', width = 100)
    emp_tree.column('gender', width = 50)
    emp_tree.column('department', width = 150)
    emp_tree.column('job', width = 150)
    emp_tree.column('civil', width = 50)
    emp_tree.column('datehired', width = 100)
    emp_tree.column('salary', width = 80)
    emp_tree.column('email', width = 200)
    emp_tree.column('contact', width = 80)
    emp_tree.column('postal', width = 50)
    emp_tree.column('address', width = 200)

    scrolly.config(command = emp_tree.yview)
    scrollx.config(command = emp_tree.xview)

    emp_tree.pack(fill = BOTH, expand = True)

    show_emp.after(10, show_emp.lift)

    show_employee_details()

    show_emp.mainloop()

#=================================
#=====Salary Frame Functions=====

def sal_emp_search():

    empidsal = empidsal_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute("SELECT empdetails.empid, empdetails.firstname, empdetails.surname, empdetails.salary FROM empdetails WHERE empid = ?", [empidsal])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Employee ID, try another!')

        else: #print the values into their entries
            #This ensures that the values inserted don't stack with the values inserted if they were ones inserted before
            emp_name_entry.delete(0, END)
            comp_salary_entry.delete(0, END)
            grosspay_entry.delete(0, END)

            emp_name_entry.insert(0, f"{row[1]} {row[2]}")
            comp_salary_entry.insert(0, f"{row[3]}")
            grosspay_entry.insert(0, f"{row[3]}")

    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

def salary_calculation():
    salary = comp_salary_entry.get()
    absent = absent_entry.get()
    workingdays = workingdays_entry.get()

    if absent == '' and workingdays == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
#        if workingdays == '20' or workingdays == '22':
        twd = int(workingdays) - int(absent)
        rateperday = float(salary) / float(twd)
        grosspay = float(rateperday) * float(twd)
        sss = float(salary) * 0.02
        pagibig = float(salary) * 0.02
        philhealth = float(salary) * 0.04
        total_contribution = sss + pagibig + philhealth

        if rateperday <= 685:
            netpay = float(salary) - float(total_contribution)
            deductions = float(total_contribution)
            #This ensures that the values inserted don't stack with the values inserted if they were ones inserted before
            rate_entry.delete(0, END)
            totalworkingday_entry.delete(0, END)
            grosspay_entry.delete(0, END)
            tax_entry.delete(0, END)
            deduction_entry.delete(0, END)
            ssscon_entry.delete(0, END)
            philcon_entry.delete(0, END)
            pagibigcon_entry.delete(0, END)
            contribution_entry.delete(0, END)
            netpay_entry.delete(0, END)

            rate_entry.insert(0, f"{round(rateperday, 2)}")
            totalworkingday_entry.insert(0, f"{twd}")
            grosspay_entry.insert(0, f"{round(grosspay, 2)}")
            tax_entry.insert(0, "No Tax")
            deduction_entry.insert(0, f"{round(deductions, 2)}")
            ssscon_entry.insert(0, f'{round(sss, 2)}')
            pagibigcon_entry.insert(0, f'{round(pagibig, 2)}')
            philcon_entry.insert(0, f'{round(philhealth, 2)}')
            contribution_entry.insert(0, f'{round(total_contribution, 2)}')
            netpay_entry.insert(0, f'{round(netpay, 2)}')

        elif rateperday >= 685 and float(salary) <= 30000:
            tax = float(salary) - 20833
            taxpercentage = float(tax) * 0.20
            deductions = float(total_contribution) + float(taxpercentage)
            netpay = float(salary) - float(deductions)
            rate_entry.delete(0, END)
            totalworkingday_entry.delete(0, END)
            grosspay_entry.delete(0, END)
            tax_entry.delete(0, END)
            deduction_entry.delete(0, END)
            ssscon_entry.delete(0, END)
            philcon_entry.delete(0, END)
            pagibigcon_entry.delete(0, END)
            contribution_entry.delete(0, END)
            netpay_entry.delete(0, END)

            rate_entry.insert(0, f"{round(rateperday, 2)}")
            totalworkingday_entry.insert(0, f"{twd}")
            grosspay_entry.insert(0, f"{round(grosspay, 2)}")
            tax_entry.insert(0, f'{round(taxpercentage, 2)}')
            deduction_entry.insert(0, f'{round(deductions, 2)}')
            ssscon_entry.insert(0, f'{round(sss, 2)}')
            pagibigcon_entry.insert(0, f'{round(pagibig, 2)}')
            philcon_entry.insert(0, f'{round(philhealth, 2)}')
            contribution_entry.insert(0, f'{round(total_contribution, 2)}')
            netpay_entry.insert(0, f'{round(netpay, 2)}')
        else:
            messagebox.showerror('Error', 'rate per day is illegible or\n salary exceeds max amount which is 30,000')
#       else:
#            messagebox.showerror('Error', 'Working Days can only be between 20 or 22!')

def sal_cal_add():
    empidsal = empidsal_entry.get()
    rate = rate_entry.get()
    paydate = pay_date_entry.get()
    fromdate = from_date_entry.get()
    todate = to_date_entry.get()
    workingdays = workingdays_entry.get()
    absent = absent_entry.get()
    totalworkingdays = totalworkingday_entry.get()
    grosspay = grosspay_entry.get()
    tax = tax_entry.get()
    deductions = deduction_entry.get()
    contributions = contribution_entry.get()
    netpay = netpay_entry.get()
    sss = ssscon_entry.get()
    pagibig = pagibigcon_entry.get()
    philhealth = philcon_entry.get()

    if empidsal == '':
        messagebox.showerror('Error', 'Need details and computations')
    else:
        try:
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM empcontributions WHERE empid = ?", [empidsal])
            row = cursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'The salary computations has already been encoded.')
            elif fromdate == '' or todate == '' or paydate == '' or workingdays == '' or absent == '':
                messagebox.showerror('Error', 'Please input the dates of payment')
            else:
                if rate == '' or totalworkingdays == '' or grosspay == '' or tax == '' or deductions == '' or contributions == '' or netpay == '' or sss == '' or pagibig == '' or philhealth == '':
                    messagebox.showerror('Error', 'Please calculate first')
                else: 
                    cursor.execute('''INSERT INTO empcontributions(empid, rate, paydate, fromdate, todate, workingdays, absent, 
                               totalworkingdays, grosspay, tax, deductions, totalcontributions, netpay, sss, pagibig, philhealth) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               [
                                empidsal,
                                rate,
                                paydate,
                                fromdate,
                                todate,
                                workingdays,
                                absent,
                                totalworkingdays,
                                grosspay,
                                tax,
                                deductions,
                                contributions,
                                netpay,
                                sss,
                                pagibig,
                                philhealth
                               ]) 
                    messagebox.showinfo('Success', 'Salary computation has been added.')
                    con.commit()
                    con.close()

        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')

def sal_delete():
    empidsal = empidsal_entry.get()
    payslipfilepath = 'payslips/' + f'payslip_{empidsal}.pdf'
    if empidsal == '':
        messagebox.showerror('Error', 'Employee ID is required for deletion!')
    else:
        try:
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM empcontributions WHERE empid = ?', [empidsal])
            row = cursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Invalid Employee ID!')
            
            else:
                if os.path.exists(payslipfilepath):
                    confirm = messagebox.askyesno('Confirm', "Do you really want to delete this employee's salary calculation?")
                    if confirm == True:
                        os.remove(payslipfilepath)
                        cursor.execute('DELETE FROM empcontributions WHERE empid = ?', [empidsal])
                        con.commit()
                        con.close()
                        messagebox.showinfo('Deleted', 'Salary Calculation successfully deleted!')
                else: 
                    confirm = messagebox.askyesno('Confirm', "Do you really want to delete this employee's salary calculation?")
                    if confirm == True:
                        cursor.execute('DELETE FROM empcontributions WHERE empid = ?', [empidsal])
                        con.commit()
                        con.close()
                        messagebox.showinfo('Deleted', 'Salary Calculation successfully deleted!')
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')

def show_payslip_data():
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('''SELECT empdetails.empid, empdetails.firstname, empdetails.surname, empdetails.salary, empcontributions.rate, 
                       empcontributions.paydate, empcontributions.fromdate, empcontributions.todate, empcontributions.workingdays, empcontributions.absent, 
                       empcontributions.totalworkingdays, empcontributions.grosspay, empcontributions.tax, empcontributions.deductions, 
                       empcontributions.netpay, empcontributions.sss, empcontributions.pagibig, empcontributions.philhealth FROM 
                       empdetails JOIN empcontributions ON empdetails.empid = empcontributions.empid''')
        rows = cursor.fetchall()
        salcal_tree.delete(*salcal_tree.get_children())
        for row in rows:
            salcal_tree.insert('', END, values = row)
        con.close()

    except Exception as ex:
        messagebox.showerror("Error", f'Error due to {str(ex)}')

#================================
#=====Salary Computation Frame=====

def Salary_Frame():  
    #==Global Variables==
    global empidsal_entry
    global emp_name_entry
    global comp_salary_entry
    global rate_entry
    global absent_entry
    global totalworkingday_entry
    global grosspay_entry
    global tax_entry
    global deduction_entry
    global contribution_entry
    global netpay_entry
    #==Contributions Variables==
    global ssscon_entry
    global philcon_entry
    global pagibigcon_entry
    #==Paydate Variables==
    global pay_date_entry
    global from_date_entry
    global to_date_entry
    global workingdays_entry
    #==Button Variables==
    global btn_search_sal

    salary_frame = customtkinter.CTkFrame(app, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    salary_frame.place(x = 0, y = 0)

    mainFrame2 = customtkinter.CTkFrame(salary_frame, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    mainFrame2.place(x = 0, y = 0)

    title = customtkinter.CTkLabel(mainFrame2, text = "Salary Computation", font = font5, bg_color = '#000e1a', fg_color = '#000e1a')
    title.place(x = 100, y = 40)

    empidsal_label = customtkinter.CTkLabel(mainFrame2, font = font6, text = 'Employee ID:', text_color = '#fff', bg_color = '#001220')
    empidsal_label.place(x = 400, y = 45)

    def only_numbers(char):
        return char.isdigit()
    validation = salary_frame.register(only_numbers)

    empidsal_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150, validate = "key", validatecommand = (validation, '%S'))
    empidsal_entry.place(x = 520, y = 45)

    emp_name_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Employee Name:', text_color = '#fff', bg_color = '#001220')
    emp_name_label.place(x = 100, y = 120)

    emp_name_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    emp_name_entry.place(x = 250, y = 120)

    comp_salary_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Salary:', text_color = '#fff', bg_color = '#001220')
    comp_salary_label.place(x = 100, y = 160)

    comp_salary_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    comp_salary_entry.place(x = 250, y = 160)

    tca_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = "Calculations 'Automated'", text_color = '#fff', bg_color = '#001220')
    tca_label.place(x = 100, y = 240)

    totalworkingday_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Total Working Days:', text_color = '#fff', bg_color = '#001220')
    totalworkingday_label.place(x = 100, y = 280)

    totalworkingday_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    totalworkingday_entry.place(x = 250, y = 280)

    grosspay_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Gross Pay:', text_color = '#fff', bg_color = '#001220')
    grosspay_label.place(x = 100, y = 320)

    grosspay_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    grosspay_entry.place(x = 250, y = 320)

    rate_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Rate / PerDay:', text_color = '#fff', bg_color = '#001220')
    rate_label.place(x = 100, y = 360)

    rate_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    rate_entry.place(x = 250, y = 360)

    tax_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Tax:', text_color = '#fff', bg_color = '#001220')
    tax_label.place(x = 100, y = 400)

    tax_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    tax_entry.place(x = 250, y = 400)

    deduction_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Deductions:', text_color = '#fff', bg_color = '#001220')
    deduction_label.place(x = 100, y = 440)

    deduction_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    deduction_entry.place(x = 250, y = 440)

    netpay_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Net Pay:', text_color = '#fff', bg_color = '#001220')
    netpay_label.place(x = 100, y = 480)

    netpay_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    netpay_entry.place(x = 250, y = 480)
#==Contributions==
    tc_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = "Contributions 'Automated'", text_color = '#fff', bg_color = '#001220')
    tc_label.place(x = 500, y = 240)

    ssscon_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'SSS:', text_color = '#fff', bg_color = '#001220')
    ssscon_label.place(x = 500, y = 280)

    ssscon_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    ssscon_entry.place(x = 650, y = 280)

    pagibigcon_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Pag-ibig:', text_color = '#fff', bg_color = '#001220')
    pagibigcon_label.place(x = 500, y = 320)

    pagibigcon_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    pagibigcon_entry.place(x = 650, y = 320)

    philcon_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Phil Health:', text_color = '#fff', bg_color = '#001220')
    philcon_label.place(x = 500, y = 360)

    philcon_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    philcon_entry.place(x = 650, y = 360)

    contribution_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Total Contributions:', text_color = '#fff', bg_color = '#001220')
    contribution_label.place(x = 500, y = 400)

    contribution_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    contribution_entry.place(x = 650, y = 400)

#==Dates==
    date_note_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = "'Manually input the date and working days'", text_color = '#fff', bg_color = '#001220')
    date_note_label.place(x = 800, y = 200)

    pay_date_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Pay Date:', text_color = '#fff', bg_color = '#001220')
    pay_date_label.place(x = 500, y = 120)

    pay_date_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    pay_date_entry.place(x = 600, y = 120)

    from_date_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'From:', text_color = '#fff', bg_color = '#001220')
    from_date_label.place(x = 850, y = 45)

    from_date_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    from_date_entry.place(x = 900, y = 45)

    to_date_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'To:', text_color = '#fff', bg_color = '#001220')
    to_date_label.place(x = 850, y = 85)

    to_date_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    to_date_entry.place(x = 900, y = 85)

    workingdays_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Working Days:', text_color = '#fff', bg_color = '#001220')
    workingdays_label.place(x = 800, y = 125)

    workingdays_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    workingdays_entry.place(x = 900, y = 125)

    absent_label = customtkinter.CTkLabel(mainFrame2, font = font7, text = 'Absents:', text_color = '#fff', bg_color = '#001220')
    absent_label.place(x = 800, y = 165)

    absent_entry = customtkinter.CTkEntry(mainFrame2, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150)
    absent_entry.place(x = 900, y = 165)
#==Buttons==
    btn_search_sal = customtkinter.CTkButton(mainFrame2, command = sal_emp_search, font = font7, text_color= "#fff", text = 'Search Employee', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 30)
    btn_search_sal.place(x = 680, y = 45)

    btn_calculate_salary = customtkinter.CTkButton(mainFrame2, command = salary_calculation,font = font7, text_color= "#fff", text = 'Calculate', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 50)
    btn_calculate_salary.place(x = 500, y = 460)

    btn_add_payslip = customtkinter.CTkButton(mainFrame2, command = sal_cal_add, font = font7, text_color= "#fff", text = 'Add to Payslip', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 50)
    btn_add_payslip.place(x = 650, y = 460)

    btn_view_payslip = customtkinter.CTkButton(mainFrame2, command = show_payslip, font = font7, text_color= "#fff", text = 'View Payslip', fg_color = '#ffbb33', hover_color = '#996600', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 50)
    btn_view_payslip.place(x = 800, y = 460)

    btn_delete_calculation = customtkinter.CTkButton(mainFrame2, command = sal_delete, font = font7, text_color= "#fff", text = 'Delete Payslip', fg_color = '#ff4d4d', hover_color = '#b30000', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 50)
    btn_delete_calculation.place(x = 950, y = 460)

    btn_emp_details = customtkinter.CTkButton(mainFrame2, command = Employee_System, font = font2, text_color= "#fff", text = 'Back to \nEmployee Details', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_emp_details.place(x = 565, y = 550)
    
    btn_generate_payslip = customtkinter.CTkButton(mainFrame2, command = Generate_Payslip_Frame, font = font2, text_color= "#fff", text = 'Generate Payslip', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_generate_payslip.place(x = 865, y = 550)

#================================
#=====Salary Database TopLevel=====

def show_payslip():
    global salcal_tree

    show_sal = customtkinter.CTkToplevel() #makes this section part of the main program
    show_sal.title("Payslip Data")
    show_sal.geometry("1000x500+120+60")
    show_sal.config(bg = "#001220")
    title = Label(show_sal, text="Employee Payslip Information", font = font1, bg = "#001220", fg = "white", anchor = "w", padx = 5)
    title.pack(side = TOP, fill = X)

    scrolly = Scrollbar(show_sal, orient = VERTICAL)
    scrollx = Scrollbar(show_sal, orient = HORIZONTAL)
    scrolly.pack(side = RIGHT, fill = Y)
    scrollx.pack(side = BOTTOM, fill = X)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background = "#001220", fieldbackground = "#001220", foreground = "white", rowheight = 30)
    style.map('Treeview', background = [('selected', '#4b7c94')])
    
    salcal_tree = ttk.Treeview(show_sal, xscrollcommand = scrollx.set, yscrollcommand = scrolly.set, 
                            columns = ('empdetails.empid', 'empdetails.firstname', 'empdetails.surname', 'empdetails.salary', 'empcontributions.rate', 
                                       'empcontributions.paydate', 'empcontributions.fromdate', 'empcontributions.todate', 'empcontributions.workingdays', 
                                       'empcontributions.absent', 'empcontributions.totalworkingdays', 'empcontributions.grosspay', 'empcontributions.tax', 
                                       'empcontributions.deductions', 'empcontributions.netpay', 'empcontributions.sss', 'empcontributions.pagibig', 'empcontributions.philhealth'))
    salcal_tree.heading('empdetails.empid', text = 'EmpID')
    salcal_tree.heading('empdetails.firstname', text = 'First Name')
    salcal_tree.heading('empdetails.surname', text = 'Surname')
    salcal_tree.heading('empdetails.salary', text = 'Salary')
    salcal_tree.heading('empcontributions.rate', text = 'Rate/PerDay')
    salcal_tree.heading('empcontributions.paydate', text = 'Pay Date')
    salcal_tree.heading('empcontributions.fromdate', text = 'From Date')
    salcal_tree.heading('empcontributions.todate', text = 'To Date')
    salcal_tree.heading('empcontributions.workingdays', text = 'Work Days')
    salcal_tree.heading('empcontributions.absent', text = 'Absents')
    salcal_tree.heading('empcontributions.totalworkingdays', text = 'Total Working Days')
    salcal_tree.heading('empcontributions.grosspay', text = 'Gross Pay')
    salcal_tree.heading('empcontributions.tax', text = 'Tax')
    salcal_tree.heading('empcontributions.deductions', text = 'Deductions')
    salcal_tree.heading('empcontributions.netpay', text = 'Net Pay')
    salcal_tree.heading('empcontributions.sss', text = 'SSS')
    salcal_tree.heading('empcontributions.pagibig', text = 'Pag Ibig')
    salcal_tree.heading('empcontributions.philhealth', text = 'Phil Health')
    salcal_tree['show'] = 'headings'

    salcal_tree.column('empdetails.empid', width = 40)
    salcal_tree.column('empdetails.firstname', width = 80)
    salcal_tree.column('empdetails.surname', width = 80)
    salcal_tree.column('empdetails.salary', width = 100)
    salcal_tree.column('empcontributions.rate', width = 100)
    salcal_tree.column('empcontributions.paydate', width = 100)
    salcal_tree.column('empcontributions.fromdate', width = 100)
    salcal_tree.column('empcontributions.todate', width = 100)
    salcal_tree.column('empcontributions.workingdays', width = 80)
    salcal_tree.column('empcontributions.absent', width = 80)
    salcal_tree.column('empcontributions.totalworkingdays', width = 150)
    salcal_tree.column('empcontributions.grosspay', width = 80)
    salcal_tree.column('empcontributions.tax', width = 50)
    salcal_tree.column('empcontributions.deductions', width = 80)
    salcal_tree.column('empcontributions.netpay', width = 80)
    salcal_tree.column('empcontributions.sss', width = 80)
    salcal_tree.column('empcontributions.pagibig', width = 80)
    salcal_tree.column('empcontributions.philhealth', width = 80)

    scrolly.config(command = salcal_tree.yview)
    scrollx.config(command = salcal_tree.xview)

    salcal_tree.pack(fill = BOTH, expand = True)

    show_sal.after(10, show_sal.lift)

    show_payslip_data()

    show_sal.mainloop()

#==================================
#=====Generate Payslip Frame Functions=====

def gen_pay_emp_search():
    empidgen = empidgen_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('''SELECT empdetails.empid, empdetails.firstname, empdetails.surname, empdetails.birthdate, empdetails.gender, 
                       empcontributions.paydate, empdetails.department, empdetails.job, empdetails.datehired, empdetails.email, empcontributions.fromdate, 
                       empcontributions.todate, empcontributions.grosspay, empcontributions.tax, empcontributions.deductions, 
                       empcontributions.totalcontributions, empcontributions.netpay FROM empdetails JOIN empcontributions ON 
                       empdetails.empid = empcontributions.empid WHERE empdetails.empid = ?''', [empidgen])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Employee ID, try another!')

        else: #print the values into their entries
            #This ensures that the values inserted don't stack with the values inserted if they were ones inserted before
            btn_generate_payslip.configure(state = NORMAL)

            gp_fn_entry.delete(0, END)
            gp_sn_entry.delete(0, END)
            gp_birth_entry.delete(0, END)
            gp_gender_entry.delete(0, END)
            gp_pay_date_entry.delete(0, END)
            gp_department_entry.delete(0, END)
            gp_job_entry.delete(0, END)
            gp_datehired_entry.delete(0, END)
            gp_email_entry.delete(0, END)
            gp_from_date_entry.delete(0, END)
            gp_to_date_entry.delete(0, END)
            gp_grosspay_entry.delete(0, END)
            gp_tax_entry.delete(0, END)
            gp_deduction_entry.delete(0, END)
            gp_contribution_entry.delete(0, END)
            gp_netpay_entry.delete(0, END)      

            gp_fn_entry.insert(0, f"{row[1]}")
            gp_sn_entry.insert(0, f"{row[2]}")
            gp_birth_entry.insert(0, f"{row[3]}")
            gp_gender_entry.insert(0, f"{row[4]}")
            gp_pay_date_entry.insert(0, f"{row[5]}")
            gp_department_entry.insert(0, f"{row[6]}")
            gp_job_entry.insert(0, f"{row[7]}")
            gp_datehired_entry.insert(0, f"{row[8]}")
            gp_email_entry.insert(0, f"{row[9]}")
            gp_from_date_entry.insert(0, f"{row[10]}")
            gp_to_date_entry.insert(0, f"{row[11]}")
            gp_grosspay_entry.insert(0, f"{row[12]}")
            gp_tax_entry.insert(0, f"{row[13]}")
            gp_deduction_entry.insert(0, f"{row[14]}")
            gp_contribution_entry.insert(0, f"{row[15]}")
            gp_netpay_entry.insert(0, f"{row[16]}")     
           
    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

def generate_pdf():
    empidgen = empidgen_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('''SELECT empdetails.empid, empdetails.firstname, empdetails.surname, empdetails.birthdate, empdetails.gender, 
                        empdetails.email, empdetails.datehired, empcontributions.fromdate, empcontributions.todate, empdetails.department, 
                        empdetails.job, empdetails.salary, empcontributions.tax, empcontributions.deductions, empcontributions.sss, 
                        empcontributions.pagibig, empcontributions.philhealth, empcontributions.paydate, empcontributions.netpay 
                        FROM empdetails JOIN empcontributions ON empdetails.empid = empcontributions.empid WHERE empdetails.empid = ?''', [empidgen])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', "Invalid Employee ID, can't generate payslip with this one, try another!")
        else:
            pdf = Payslip()
            pdf.add_page()
            pdf.employee_info(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            pdf.salary_comp(row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18])

            output_folder = 'payslips'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            else:
                pdf_file = os.path.join(output_folder, f'payslip_{row[0]}.pdf')
                pdf.output(pdf_file)
                messagebox.showinfo('Payslip Created', f'Payslip for Employee ID: {row[0]}\nhas been created.')
                btn_generate_payslip.configure(state = DISABLED)
                btn_print_payslip.configure(state = NORMAL)
                btn_email_payslip.configure(state = NORMAL)

    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

def print_pdf():
    empidgen = empidgen_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute("SELECT empid FROM empdetails WHERE empid = ?", [empidgen])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Employee ID\ntry another to print!')
        else:
            output_folder = 'payslips'
            pdf_file = os.path.join(output_folder, f'payslip_{empidgen}.pdf')
            webbrowser.open_new('file://' + os.path.realpath(pdf_file))

    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

def send_payslip_email():
    empidgen = empidgen_entry.get()
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute("SELECT empid, firstname, surname, email FROM empdetails WHERE empid = ?", [empidgen])
        row = cursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Employee ID\nPlease select valid ID to send Email!')
        else:
            output_folder = 'payslips'
            pdf_file = os.path.join(output_folder, f'payslip_{row[0]}.pdf')

            #Email Initialization
            sender_email = "Group5PythonICCT@gmail.com"
            sender_password = "uzfa cimb ewcd dkql"
            receiver_email = row[3]
            subject = f"Payslip Distribution for ID: {empidgen}"
            body = f"Employee ID: {row[0]}\nEmployee Name: {row[1]} {row[2]}\nThis is your payslip for this month"
            file_path = os.path.realpath(pdf_file)
            file_name = f'payslip_{row[0]}.pdf'

            send_email.send_message(sender_email, sender_password, receiver_email, subject, body, file_path, file_name)

            messagebox.showinfo('Success', 'Email Sent!')

    except Exception as ex:
        messagebox.showerror('Error', f'Error due to {str(ex)}')

#================================
#=====Generate Payslip Frame=====

def Generate_Payslip_Frame():
    #==Global Variables==
    global empidgen_entry
    global gp_fn_entry
    global gp_sn_entry
    global gp_birth_entry
    global gp_gender_entry
    global gp_department_entry
    global gp_job_entry
    global gp_datehired_entry
    global gp_email_entry
    #==Salary Computation Variables
    global gp_grosspay_entry
    global gp_tax_entry
    global gp_deduction_entry
    global gp_contribution_entry
    global gp_netpay_entry
    #==Date Variables==
    global gp_pay_date_entry
    global gp_from_date_entry
    global gp_to_date_entry

    #==Button Variables
    global btn_generate_payslip
    global btn_print_payslip
    global btn_email_payslip

    payslip_frame = customtkinter.CTkFrame(app, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    payslip_frame.place(x = 0, y = 0)

    mainFrame3 = customtkinter.CTkFrame(payslip_frame, bg_color = '#001220', fg_color = '#001220', width = 1350, height = 700)
    mainFrame3.place(x = 0, y = 0)

    title = customtkinter.CTkLabel(mainFrame3, text = "Generate Payslip", font = font5, bg_color = '#000e1a', fg_color = '#000e1a')
    title.place(x = 100, y = 40)

    empidgen_label = customtkinter.CTkLabel(mainFrame3, font = font6, text = 'Employee ID:', text_color = '#fff', bg_color = '#001220')
    empidgen_label.place(x = 380, y = 45)

    def only_numbers(char):
        return char.isdigit()
    validation = payslip_frame.register(only_numbers)

    empidgen_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 150, validate = "key", validatecommand = (validation, '%S'))
    empidgen_entry.place(x = 500, y = 45)

    #==Employee Details Section==

    gp_fn_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'First Name:', text_color = '#fff', bg_color = '#001220')
    gp_fn_label.place(x = 150, y = 150)

    gp_fn_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_fn_entry.place(x = 300, y = 150)

    gp_sn_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Surname:', text_color = '#fff', bg_color = '#001220')
    gp_sn_label.place(x = 150, y = 190)

    gp_sn_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_sn_entry.place(x = 300, y = 190)

    gp_birth_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Date of Birth:', text_color = '#fff', bg_color = '#001220')
    gp_birth_label.place(x = 150, y = 230)

    gp_birth_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_birth_entry.place(x = 300, y = 230)

    gp_gender_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Gender:', text_color = '#fff', bg_color = '#001220')
    gp_gender_label.place(x = 150, y = 270)

    gp_gender_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_gender_entry.place(x = 300, y = 270)

    gp_pay_date_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Pay Date:', text_color = '#fff', bg_color = '#001220')
    gp_pay_date_label.place(x = 600, y = 150)

    gp_pay_date_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_pay_date_entry.place(x = 750, y = 150)

    gp_department_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Department:', text_color = '#fff', bg_color = '#001220')
    gp_department_label.place(x = 600, y = 190)

    gp_department_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_department_entry.place(x = 750, y = 190)

    gp_job_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Job Title:', text_color = '#fff', bg_color = '#001220')
    gp_job_label.place(x = 600, y = 230)

    gp_job_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_job_entry.place(x = 750, y = 230)

    gp_datehired_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Date Hired:', text_color = '#fff', bg_color = '#001220')
    gp_datehired_label.place(x = 600, y = 270)

    gp_datehired_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_datehired_entry.place(x = 750, y = 270)

    gp_email_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Email:', text_color = '#fff', bg_color = '#001220')
    gp_email_label.place(x = 600, y = 310)

    gp_email_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 200)
    gp_email_entry.place(x = 750, y = 310)

    #=======================
    #==Salary Calculations Section==

    gp_grosspay_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Gross Pay:', text_color = '#fff', bg_color = '#001220')
    gp_grosspay_label.place(x = 150, y = 400)

    gp_grosspay_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_grosspay_entry.place(x = 300, y = 400)

    gp_tax_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Tax:', text_color = '#fff', bg_color = '#001220')
    gp_tax_label.place(x = 150, y = 440)

    gp_tax_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_tax_entry.place(x = 300, y = 440)

    gp_deduction_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Deductions:', text_color = '#fff', bg_color = '#001220')
    gp_deduction_label.place(x = 150, y = 480)

    gp_deduction_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_deduction_entry.place(x = 300, y = 480)

    gp_contribution_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Total Contributions:', text_color = '#fff', bg_color = '#001220')
    gp_contribution_label.place(x = 150, y = 520)

    gp_contribution_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_contribution_entry.place(x = 300, y = 520)

    gp_netpay_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'Net Pay:', text_color = '#fff', bg_color = '#001220')
    gp_netpay_label.place(x = 150, y = 560)

    gp_netpay_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_netpay_entry.place(x = 300, y = 560)

    #==Dates==
    gp_from_date_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'From:', text_color = '#fff', bg_color = '#001220')
    gp_from_date_label.place(x = 950, y = 45)

    gp_from_date_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_from_date_entry.place(x = 1000, y = 45)

    gp_to_date_label = customtkinter.CTkLabel(mainFrame3, font = font7, text = 'To:', text_color = '#fff', bg_color = '#001220')
    gp_to_date_label.place(x = 950, y = 85)

    gp_to_date_entry = customtkinter.CTkEntry(mainFrame3, font = font7, text_color = '#fff', fg_color = '#001a2e', bg_color = '#121111', border_color= '#004780', border_width = 3, width = 125)
    gp_to_date_entry.place(x = 1000, y = 85)
    #=========
    #===============================

    #==Buttons==

    btn_search_gen = customtkinter.CTkButton(mainFrame3, command = gen_pay_emp_search, font = font7, text_color= "#fff", text = 'Search Employee', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 30)
    btn_search_gen.place(x = 660, y = 45)

    btn_generate_payslip = customtkinter.CTkButton(mainFrame3, state = DISABLED, command = generate_pdf, font = font7, text_color= "#fff", text = 'Generate Payslip', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 125, height = 30)
    btn_generate_payslip.place(x = 800, y = 45)

    btn_print_payslip = customtkinter.CTkButton(mainFrame3, state = DISABLED, command = print_pdf, font = font7, text_color= "#fff", text = 'Print Payslip', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 200, height = 80)
    btn_print_payslip.place(x = 600, y = 400)
    
    btn_email_payslip = customtkinter.CTkButton(mainFrame3, state = DISABLED, command = send_payslip_email, font = font7, text_color= "#fff", text = 'E-mail Payslip', fg_color = '#00956d', hover_color = '#006e44', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 200, height = 80)
    btn_email_payslip.place(x = 850, y = 400)

    btn_back_salary = customtkinter.CTkButton(mainFrame3, command = Salary_Frame, font = font7, text_color= "#fff", text = 'Back to\nSalary Computation', fg_color = '#0099e6', hover_color = '#005580', bg_color = '#121111', cursor = "hand2", corner_radius = 5, width = 150, height = 50)
    btn_back_salary.place(x = 750, y = 525)

    #==========
    
#================================
#=====Mainloop and Table Creation=====

create_tables()
app.mainloop()

#=====================================