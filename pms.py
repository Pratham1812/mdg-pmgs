from art import *
import maskpass
from cryptography.fernet import Fernet
import hashlib
import sqlite3
import random
import time
import base64
# connect to the database, creating it if it doesn't exist
conn = sqlite3.connect('db.sqlite')

# create a cursor object
cursor = conn.cursor()

# create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS pms (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,description TEXT, password TEXT,key TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, pass_user TEXT)''')

# commit the changes
conn.commit()
tprint("PMGS")



print("#"*39)
print("#"+" "*15+"Welcome"+" "*15+"#")
print("#"*39)
print("Press")
print("1. To generate a new password")
print("2. To save and maintain all your password at one place")

print("3. To view saved passwords \n\n")
print("MADE WITH LOVE BY PRATHAM AGARWAL")

key = int(input())

if(key==1):
    print("Enter length of password required ")
    length = int(input())
    print("Please choose the prefference for your password ")
    print("Press")
    print("1. Include UPPERCASE letters")
    print("2. Include LOWERCASE letters")
    print("3. Include Numbers")
    print("4. Include alpha numeric characters")
    print("5. Include special characters")
    print("Enter the number of your prefference, Please follow the following format while typing --> num1 num2 num3 ")
    ls1 = list(map(int,input().split()))
    ls = [i-1 for i in ls1]
    super_list = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz","1234567890"]
    super_list.append(super_list[0]+super_list[1]+super_list[2])
    super_list.append("""!@#$%^&*()_+-=<>;'"][}{?/|""")
    gen_pass = ""
    for j in range(length):
        random.seed(j*time.time())
        if(len(ls)>1):
            sel =  super_list[ls[random.randint(0,len(ls)-1)]]
                    
            gen_pass += sel[random.randint(0,len(sel)-1)]
            

        elif(len(ls)==1):
            sel =  super_list[ls[0]]
            
            gen_pass += sel[random.randint(0,len(sel)-1)]
        
            

    print("The generated password is "+ gen_pass)
    print("Press 1 if you want to store this password in our highly protected db")


elif(key==2):
    print("Create a new user or login to existing user with your password")
    print("Press 1 to create new user")
    print("Press 2 to login as a existing user")
    key3 = int(input())
    if(key3==2):
    
        username = input("Enter your username : ")
    

        userpass = maskpass.askpass(mask="*")
        res = cursor.execute("""SELECT * FROM users WHERE username='{}' AND pass_user='{}'""".format(username,userpass))
        if(res.fetchone() is None):
            print("incorrect credentials")
        else:
            
        
            desc = input("Enter some information related to your password ")
            
        
            pass_user = maskpass.askpass(mask="*")
            key = Fernet.generate_key()
            
            fernet = Fernet(key)
            
            # then use the Fernet class instance
            # to encrypt the string string must
            # be encoded to byte string before encryption
            encoded_pass = fernet.encrypt(pass_user.encode())
            cursor.execute("""INSERT INTO pms (username,description,password,key) VALUES ('{}','{}','{}','{}')""".format(username,desc,encoded_pass.decode("utf-8"),key.decode("utf-8")))
            print("successfully inserted")
    elif(key3==1):
    
        username = input("Enter your username : ")
        

        userpass = maskpass.askpass(mask="*")
        cursor.execute("""INSERT INTO users (username,pass_user) VALUES ('{}','{}')""".format(username,userpass))
        
        

        desc = input("Enter some information related to your password ")
        
        
        pass_user = maskpass.askpass(mask="*")
        key = Fernet.generate_key()
        
        fernet = Fernet(key)
        
        # then use the Fernet class instance
        # to encrypt the string string must
        # be encoded to byte string before encryption
        encoded_pass = fernet.encrypt(pass_user.encode())
        cursor.execute("""INSERT INTO pms (username,description,password,key) VALUES ('{}','{}','{}','{}')""".format(username,desc,encoded_pass.decode("utf-8"),key.decode("utf-8")))
        
        print("successfully inserted")

elif(key==3):
    username = input("Enter your username ")
    userpass = maskpass.askpass(mask="*")
    res = cursor.execute("""SELECT * FROM users WHERE username='{}' AND pass_user='{}'""".format(username,userpass))
    if(res.fetchone() is None):
        print("incorrect credentials")
    else:
        res = cursor.execute("""SELECT * FROM pms WHERE username='{}' """.format(username))
        god_lst = res.fetchall()
        print("Hello ! ",god_lst[0][1])
        for j in god_lst:
    
            print(j[2])
            
            fernet = Fernet((j[4].encode()))
            decMessage = fernet.decrypt((j[3].encode())).decode("utf-8")
            print("The stored password related to "+j[2]+" is "+decMessage)


cursor.close()
conn.commit()
conn.close()

