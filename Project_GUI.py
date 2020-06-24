#import modules

import Features_Extractor
from tkinter import *
import pandas as pd
import numpy as np
import os

# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", fg="Red", font = ("Times", 14)).pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()


# Designing window for login 

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x350")
    Label(login_screen, text = "If You Have An Account ", fg = "red", font = ("algerian", 23)).pack()
    Label(login_screen, text = "").pack()
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username *", fg = "red", font = ("Times", 14)).pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password *", fg = "red", font = ("Times", 14)).pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", height = 1, width = 20, fg = "red", bg = "Green", font= ("Times", 18), command = login_verify).pack()

# Implementing event on register button

def register_user():

    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

# Implementing event on login button 

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()

# Designing popup for login success

def login_sucess():
    global login_success_screen
    global url_entry
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Login Success")
    login_success_screen.geometry("450x200")
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(login_success_screen, text="Please Enter Your URL :", fg = "red", font= ("Times", 14)).pack()
    Label(text = "").pack()

    url_verify = StringVar()
    url_entry = StringVar()
    Label(text = "").pack()
    url_entry = Entry(login_success_screen, textvariable=url_verify)
    url_entry.pack()

    Button(login_success_screen, text="Pridict", fg = "red", bg = "Green", font= ("Times"), command = Pridict).pack()    
#   Button(login_success_screen, text="OK", command=delete_login_success).pack()

# Pridiction Verification window
def Pridict():
    try:
        website = url_entry.get()
        Features_Extractor.generate_data_set(website)
    
        read = pd.read_csv(r'D:\Vnj Vibhash\Project\Detect_Phishing_Website-master\phishing.txt',header = None,sep = ',')
        read = read.iloc[:,:-1].values
        dataset = pd.read_csv(r'D:\Vnj Vibhash\Project\Detect_Phishing_Website-master\Training Dataset.csv')
        X = dataset.iloc[:,:-1].values 	
        y = dataset.iloc[:,-1].values
    
        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=8)
    
        from sklearn_extensions.extreme_learning_machines import ELMClassifier
        regressor=ELMClassifier(n_hidden=150, alpha=0.99, activation_func='tanh')
        regressor.fit(X_train,y_train)                             
    
        y_pred = regressor.predict(X_test)
    
    
        from sklearn.model_selection import cross_val_score
        accuracy = cross_val_score(estimator = regressor,X=X_train,y=y_train,cv = 5)
        accuracy.mean()
        accuracy.std()
    
        try:
            Detect_phishing_website = regressor.predict(read)
        except:
            Detect_phishing_website = -1
    
        if Detect_phishing_website == 1:
            legitimate_website()
        elif Detect_phishing_website == 0:
            suspicious_website()
        else:
            phishing_website()
    except:
        phishing_website()

# Designing popup for Pridiction

def legitimate_website():
    global legitimate_website_screen
    legitimate_website_screen = Toplevel(login_screen)
    legitimate_website_screen.title("Legitimate Website")
    legitimate_website_screen.geometry("150x100")
    Label(legitimate_website_screen, text="Legitimate Website").pack()
    Button(legitimate_website_screen, text="OK", command=delete_legitimate_website).pack()

def suspicious_website():
    global suspicious_website_screen
    suspicious_website_screen = Toplevel(login_screen)
    suspicious_website_screen.title("Suspicious Website")
    suspicious_website_screen.geometry("150x100")
    Label(suspicious_website_screen, text="Suspicious Website").pack()
    Button(suspicious_website_screen, text="OK", command=delete_suspicious_website).pack()

def phishing_website():
    global phishing_website_screen
    phishing_website_screen = Toplevel(login_screen)
    phishing_website_screen.title("Phishing Website")
    phishing_website_screen.geometry("150x100")
    Label(phishing_website_screen, text="Phishing Website").pack()
    Button(phishing_website_screen, text="OK", command=delete_phishing_website).pack()


# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups

def delete_legitimate_website():
    legitimate_website_screen.destroy()

def delete_suspicious_website():
    suspicious_website_screen.destroy()

def delete_phishing_website():
    phishing_website_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("850x500")
    main_screen.title("Phishing Website Detection Project")
    Label(text = "").pack()
    Label(text = "Welcome To My Phishing Website Detection Project", fg = "red", font = ("algerian", 23)).pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Label(text = "According to Your Requirement").pack()
    Label(text = "Please Choose Your Option", fg = "red", font = ("algerian", 23)).pack()
    Label(text = "").pack()
    Button(text="Login", height="2", width="30",fg = "red", bg = "Green", font= ("Times", 18), command = login).pack()
    Label(text = "").pack()
    Label(text = "").pack()
    Button(text="Register", height="2", width="30", fg = "red", bg = "Pink",font= ("Times", 18), command=register).pack()

    main_screen.mainloop()


main_account_screen()
