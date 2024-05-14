import socket
import threading
import _tkinter
import select
import os
import shlex
from shutil import copy2
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
import mysql.connector
from tkinter import filedialog
import threading
LARGE_FONT = ("verdana", 13,"bold")

### mysql
db = mysql.connector.connect(user = 'root', password = '', host = 'localhost', database = "mmt")
print(db)
cursor = db.cursor()

SIGNUP = "signup"
LOGIN = 'login'
LOGOUT = "logout"
FETCH = 'fetch'
LARGE_FONT = ("verdana", 13,"bold")




###---------------------------------------###

class serverApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)   

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage) 

    def showFrame(self, container):
        frame = self.frames[container]
        self.geometry("500x450")
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("tắt", "bạn có thật sự muốn tắt?"):
            self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.configure(bg="bisque2")
    
        controller.title("server")
        label_useron = tk.Label(self, text="người dùng đang kết nối", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_useron.grid(row=1, column=3, columnspan=3)

        label_useron = tk.Label(self, text="kết quả", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_useron.grid(row=3, column=4)
    

        self.list_user = tk.Listbox(self, width=50)
        self.list_user.grid(row=2, column=3, columnspan=3)

        label_command = tk.Label(self, text="   Nhập lệnh", font=LARGE_FONT)
        label_command.grid(row=5, column=1)
        

        self.command = tk.Entry(self)
        self.command.grid(row=6,column=1, columnspan=2)

        self.button_check=tk.Button(self, text="kiểm tra", bg="#20639b",fg='#f5ea54', command= self.check_liveacc)
        self.button_check.grid(row=2,column=1)    

        self.button_command=tk.Button(self, text="chạy", bg="#20639b",fg='#f5ea54', command= self.add_button_)
        self.button_command.grid(row=6,column=2)

        self.list_comment = tk.Listbox(self, width=50)
        self.list_comment.grid(row=4, column=3, columnspan=3, rowspan=6)

  
   
        
    def print_c(self, x):
        max_length = 50
        while len(x) > max_length:
            part, x = x[:max_length], x[max_length:]
            if x and x[0] == ",":
                part += x[0]  # Thêm dấu ',' vào cuối phần trước
                x = x[1:]  # Bỏ dấu ',' khỏi đầu chuỗi x
            self.list_comment.insert(tk.END, part)
        self.list_comment.insert(tk.END, x)
    def print_d(self,x):
            self.list_user.insert(tk.END,x)

    def check_liveacc(self):
        self.list_user.delete(0, tk.END)
        for row in Live_Account: 
            self.print_d(row)
    
    def add_button_(self):
        self.list_comment.delete(0,tk.END)
        value = self.command.get()
        thamso = space_empty(value)
        if (value.startswith('ping ') or value=='ping'):
            if (thamso==1):
                host_name = value[5:]
                check = Check_LiveAccount(host_name)
                if check == False:
                        self.print_c((host_name+' connect')) 
                else:
                        self.print_c(host_name +' not connect')
            else: self.print_c("hàm này cần tham số user")
            

        elif(value.startswith('discover ') or value == 'discover'):
            if (thamso==1):
                host_name = value[9:]
                self.discover_c(host_name)
            else: self.print_c("hàm này cần tham số user")
        elif(value.startswith=='listUserO'):
            self.listUserO_c()
        elif(value.startswith('listUserA')):
            self.listUserA_c()
            
        elif(value=='listUser'):
            self.listUser_c()
        # elif(value.startswith('getUserInform ')):
        #     username = value[13:]
        #     self.getUserInform_c(username)
        elif(value.startswith('getOwner ') or value == 'getOwner'):
            if (thamso==1):
                filename = value[9:]
                self.getOwner_c(filename)
            else: self.print_c("xin thêm tên file đi")
 
        else:
            self.print_c('bạn có thể nhập các hàm: ping, discover, liseUserO, listUserA, listUser,  getOwner bằng cách gọi tên kèm theo tham số truyền vào nếu có.')

    ###--------------hàm xử lí nhỏ-----------------####

    
        
    def discover_c(self, user):
        cursor.execute("select file_name from ds_user  where username = %s",(user,))
        result = cursor.fetchall()
        if len(result) == 0:
            self.print_c('không tìm thấy gì hết!')
        else:
            self.print_c((user, ":", result))
    def listUser_c(self):
        cursor.execute("select username from taikhoan")
        result = cursor.fetchall()
        if len(result) == 0:
            self.print_c('không tìm thấy gì hết!')
        else:
            for row in result:
                self.print_c(row[0])  
    def listUserO_c (self):
        if len(Live_Account) == 0:
            self.print_c('không tìm thấy ai!')
            return 0
        for row in Live_Account:
            ip, id= row.split("-")
            self.printc(id)
    def listUserA_c (self):
        if len(Live_Account) == 0:
            self.print_c('không thấy ai cả!')
        for row in Live_Account:
            parse= row.find("-")
            parse_check= row[(parse+1):]
            self.print_c(parse_check)
            self.discover_c(parse_check)   
    def getOwner_c (self,filename):
        cursor.execute("select username from ds_user  where file_name = %s",  (filename,))
        result=cursor.fetchall()
        if not result:
            self.print_c("bạn sẽ không tìm thấy nó lúc này")
        else:
            result_str = ''
            for row in result:
                if not Check_LiveAccount(row[0]):
                    result_str += row[0] + '\n' 
            self.print_c(result_str) 
          
def space_empty(s):
   
    parts = s.split(" ")
   
    if len(parts) > 1:
        
        if parts[1]:
            return True  # Có khoảng trắng và sau khoảng trắng không rỗng
    return False  # Không có khoảng trắng hoặc sau khoảng trắng rỗng

##
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP




#host = "192.168.137.1" #loopback

host = "192.168.0.203"
port = 10001
format = "utf8"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
###---------------------Login/SignUp----------------###

## dang ki tai khoan
def Insert_New_Account(user,password):
    sql = "INSERT INTO TaiKhoan(username, password, addr_IP, path) VALUES (%s, %s, %s, %s)"
    val = (user, password, "", "")
    cursor.execute(sql, val)
    db.commit() 

#### kiem tra ten dang ki co bi trung
def check_clientSignUp(username):
    if username == "admin":
        return 0
    cursor.execute("select username from TaiKhoan")
    for row in cursor:
        parse=str(row)
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        if parse_check == username:
            return 0
    return 1

#### Lưu đường dẫn tới thư mục local repo vào database
def Update_repoPath(username, password, addr, path):
    sql = "UPDATE TaiKhoan SET path = %s, addr_IP = %s WHERE username = %s AND password = %s"
    val = (path, addr, username, password)
    cursor.execute(sql, val)
    db.commit()

#### Copy file từ client sang local repository
def publishFile(destFileName, userName):
    cursor.execute("SELECT file_name FROM ds_user WHERE username = %s", (userName,))
    result = cursor.fetchone()
    file_exists = False  # Biến boolean để kiểm tra xem tên file đã tồn tại hay chưa
    if result is not None:
        for row in cursor:
            parse=str(row)
            parse_check =parse[2:]
            parse= parse_check.find("'")
            parse_check= parse_check[:parse]
            if parse_check == destFileName:
                file_exists = True
                break

    if file_exists:
        conn.sendall('trung_ten'.encode(format))
    else:
        cursor.execute("SELECT path FROM TaiKhoan WHERE username = %s", (userName,))
        result = cursor.fetchone()
        if result is not None:
            path_value = result[0]
            destPath = os.path.join(path_value, destFileName)
            conn.sendall(destPath.encode(format))

            sql = "INSERT INTO ds_user(username, file_name) VALUES (%s, %s)"
            val = (userName, destFileName)
            cursor.execute(sql, val)
            db.commit()
            print(f'{userName} đã thêm file {destFileName} vào local repository')
        else:
            print("Invalid message format")

Live_Account=[]
ID=[]
Ad=[]

## kiem tra ten dang nhap 
def Check_LiveAccount(username):
    for row in Live_Account:
        parse= row.find("-")
        parse_check= row[(parse+1):]
        if parse_check== username:
            return False
    return True
### log out
def Remove_LiveAccount(conn,addr):
    for row in Live_Account:
        parse= row.find("-")
        parse_check=row[:parse]
        if parse_check== str(addr):
            parse= row.find("-")
            Ad.remove(parse_check)
            username= row[(parse+1):]
            ID.remove(username)
            Live_Account.remove(row)

## check login
def check_clientLogIn(username, password):
    if not Check_LiveAccount(username):
        return 0
    if username == "admin" and password == "database":
        return 1

    cursor.execute("SELECT username FROM TaiKhoan")
    result = cursor.fetchall()

    for row in result:
        parse=str(row)
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        if parse_check == username:
            cursor.execute("select password from TaiKhoan  where username = %s",(username,))
            parse= str(cursor.fetchone())
            parse_check =parse[2:]
            parse= parse_check.find("'")
            parse_check= parse_check[:parse]
            if password== parse_check:
                return 1
    return 2
## signUp
def clientSignUp(conn, addr):

    user = conn.recv(1024).decode(format)
    print("username: --" + user + "--")

    conn.sendall(user.encode(format))
    pswd = conn.recv(1024).decode(format)
    print("password: --" + pswd + "--")

    accepted = check_clientSignUp(user)
    print("accept:", accepted)
    conn.sendall(str(accepted).encode(format))
    if accepted == 1:
        # add client sign up address to live account
        Insert_New_Account(user, pswd)
        Ad.append(str(addr))
        ID.append(user)
        account = str(Ad[Ad.__len__() - 1]) + "-" + str(ID[ID.__len__() - 1])
        Live_Account.append(account)

        path_to_repository = conn.recv(1024).decode(format)
        conn.sendall(path_to_repository.encode(format))
        parse_check = str(addr)
        parse_check = parse_check[2:]
        parse = parse_check.find("'")
        parse_check = parse_check[:parse]
        print(parse_check)
        Update_repoPath(str(user), str(pswd), str(parse_check), str(path_to_repository))

    print("end-SignUp()")
    return accepted

##login
def clientLogIn(conn):

    user = conn.recv(1024).decode(format)
    print("username:--" + user +"--")
    conn.sendall(user.encode(format))
    pswd = conn.recv(1024).decode(format)
    print("password:--" + pswd +"--")
    accepted = check_clientLogIn(user, pswd)
    if accepted == 1:
        ID.append(user)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)
    print("accept:", accepted)
    print("end-logIn()")
    return accepted

########   discover ####
def discover(user):
    cursor.execute("select file_name from ds_user  where username = %s",(user,))
    result = cursor.fetchall()
    if len(result) == 0:
        print('Khong tim thay Hostnames!')
    else:
        print(user, ":", result)

def sendOwnerInform(conn,addr):
    username = conn.recv(1024).decode(format)

    conn.sendall(username.encode(format)) ### user nguoi giu file
    check_live = Check_LiveAccount(username)
    if check_live == False:
        cursor.execute("select addr_IP from TaiKhoan  where username = %s",(username,))
        parse= str(cursor.fetchone())
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        conn.sendall(parse_check.encode(format))
        conn.recv(1024)

        cursor.execute("select path from TaiKhoan  where username = %s",(username,))
        parse= str(cursor.fetchone())
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        conn.sendall(parse_check.encode(format)) ## gui path  nguoi giu file
    
        user = conn.recv(1024).decode(format)
        cursor.execute("select path from TaiKhoan  where username = %s",(user,))
        parse= str(cursor.fetchone())
        parse_check =parse[2:]
        parse= parse_check.find("'")
        parse_check= parse_check[:parse]
        conn.sendall(parse_check.encode(format))
        conn.recv(1024)

        file_name_ = conn.recv(1024).decode(format)
        conn.sendall('thanhcong'.encode(format))
        user_ = conn.recv(1024).decode(format)
        conn.sendall('thanhcong'.encode(format))
        sql = "INSERT INTO ds_user(username, file_name) VALUES (%s, %s)"
        val = (user_, file_name_)
        cursor.execute(sql, val)
        db.commit()
        
    else:
        conn.sendall('-1'.encode(format))
        conn.recv(1024)

###---------------list------------------###

def listUser():
    cursor.execute("select username from taikhoan")
    result = cursor.fetchall()
    if len(result) == 0:
        print('Khong tim thay hostname!')
    else:
        for row in result:
            print(row[0])  

def listUserO ():
    for row in Live_Account:
        ip, id= row.split("-")
        print(id)


def listUserA_2 (conn, addr):
    conn.sendall('thanh cong'.encode(format))
    user = conn.recv(1024).decode(format)
    
    for row in Live_Account:
        parse= row.find("-")
        parse_check= row[(parse+1):]
        if parse_check == user:
            continue
        cursor.execute("select file_name from ds_user  where username = %s",(parse_check,))
        result = cursor.fetchall()
        if len(result) == 0:
            continue
        else:
            result_str = ''
            for row in result:
                    result_str += row[0] + ' ' 
            conn.sendall(result_str.encode(format))
            conn.recv(1024)
            conn.sendall(parse_check.encode(format))
    conn.sendall('kethuc'.encode(format))
    conn.recv(1024)
    conn.sendall('ketthuc'.encode(format))
        

###-------------get-----------_###
def getUserInform (user):
    check = Check_LiveAccount(user)
    if check == False:
        for row in Live_Account:
            ip, id= row.split("-")
            if id== user: 
                print(ip)
    else:
        print(user ,' not connect')

def getOwner (conn, filename):
    conn.sendall('thanh cong'.encode(format))
    user_ = conn.recv(1024).decode(format)
    cursor.execute("select username from ds_user  where file_name = %s",  (filename,))
    result=cursor.fetchall()
    if not result:
        conn.sendall("Not user".encode(format))
        conn.recv(1024)
    else:
        check = 0
        result_str = ''
        for row in result:
            if not Check_LiveAccount(row[0]):
                if row[0] !=  user_:
                    result_str += row[0] + ' ' 
                    check = check + 1
        if check == 0:
            conn.sendall("Not user".encode(format))
            conn.recv(1024)
        else:
            conn.sendall(result_str.encode(format))
            conn.recv(1024)

#########online########

# ######## check conn############
# def check_connections(user):
#     if(not Live_Account):
#         print(user ,' not connect')
#     else:     
#         for row in Live_Account:
#             parse= row.find("-")
#             parse_check=row[(parse+1):]
#             if parse_check== user:
#                 print(user, ' connect') 
#             else:
#                 print(user ,' not connect')
def get_path(conn,addr, user):
    cursor.execute("select path from taikhoan  where username = %s",  (user,))
    parse= str(cursor.fetchone())
    parse_check =parse[2:]
    parse= parse_check.find("'")
    parse_check= parse_check[:parse]
    conn.sendall(parse_check.encode(format))
    conn.recv(1024)

####--------------xu li-------####
def handleClient(conn, addr):
    print("connection:",str(addr))
    ################ login /signUp #############
    while True:
        try:
            option = conn.recv(1024).decode(format)
            parts = option.split(" ")
            path = option.split(" ")
            if option == LOGIN:
                Ad.append(str(addr))
                check = clientLogIn(conn)
                if(check == 1):
                    conn.sendall(str(check).encode(format))
                    print('Dang nhap thanh cong!')
                    print("")
                   
                else:
                    conn.sendall(str(check).encode(format))
                    print('Dang nhap that bai!')
                    print("")
            elif option == SIGNUP:
                check = clientSignUp(conn, addr)
                if(check == 1):
                    print('Dang ki thanh cong!')
                    print("")
                    
                else:
                    print('Dang ki that bai!')
                    print("")
            elif option == 'list_all':
                listUserA_2 (conn, addr)
            elif(option == "logout"):
                Remove_LiveAccount(conn,addr)
                conn.sendall("True".encode(format))

            elif(option == FETCH):
                sendOwnerInform(conn,addr)
            elif option.startswith("findOwner"):
                filename = option[10:]
                getOwner(conn, filename)
            elif len(parts) == 3 and parts[0] == "publish":
                dest_filename = parts[1]
                username = parts[2]
                publishFile(dest_filename, username)
            elif path[0] == 'path_repo':
                get_path(conn,addr, path[1])
            elif(option == 'quit'):
                print(str(addr), "not connection")
                print("end-thread:", str(addr))
                Remove_LiveAccount(conn,addr)
                conn.close()
                return
        except:
            print(str(addr), "not connection")
            print("end-thread:", str(addr))
            Remove_LiveAccount(conn,addr)
            conn.close()
            return
            
   


s.bind((host, port))
s.listen()
print("SERVER SIDE")
print("server:", host, port)
print("Waiting for Client")



def server_conn_thread():
    app = serverApp()
    try:
        app.mainloop()
    except:
        print("Error: server is not responding")
    finally:

        print('end')
        


thread_server_connect = threading.Thread(target=server_conn_thread)
thread_server_connect.daemon = False
thread_server_connect.start()


while True:
    try:
        conn, addr = s.accept()
        thread_client = threading.Thread(target=handleClient, args=(conn,addr))
        thread_client.daemon = False
        thread_client.start()
    except:
        print("Error")
s.close()



