from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess
root=Tk()
root.title("Shareit")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)


def select_file():
      global filename
      filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                         title='Select Image File',
                                         filetype=(('file_type','*.txt'),('all files','*.*')))



def sender():
      s=socket.socket()
      host=socket.gethostname()
      port=8080
      s.bind((host,port))
      s.listen(1)
      print(host)
      print('waiting for any incoming connections...')
      conn,addr=s.accept()
      file=open(filename,'rb')
      file_data=file.read(1024)
      conn.send(file_data)
      print("Data has been transmitted successfully...")


def Send():

      print(image_dir)

      window=Toplevel(root)
      window.title("Send")
      window.geometry('450x560+500+200')
      window.configure(bg="#f4fdfe")
      window.resizable(False,False)

      #icon
      image_icon1=PhotoImage(file=os.path.join(image_dir, "send.png"))
      window.iconphoto(False,image_icon1)
      print(image_dir)
      Sbackground=PhotoImage(file=os.path.join(image_dir, "background.png"))
      Label(window,image=Sbackground).place(x=-2,y=0)
      print(image_dir)
      Mbackground=PhotoImage(file=os.path.join(image_dir, "background2.png"))
      Label(window,image=Mbackground,bg='#f4fdfe').place(x=100,y=260)

      with open('user.txt', 'r') as file:
            USER = file.read()

      host=socket.gethostname()
      Label(window,text=f'ID: {USER}',bg='white',fg='black').place(x=140,y=290)

      Button(window,text="+ select file", width=10,height=1,font='arial 14 bold',bg="#fff",fg="#000",command=select_file).place(x=160,y=150)
      Button(window,text="SEND",width=8,height=1,font='arial 14 bold',bg='#000',fg="#fff",command=sender).place(x=300,y=150)

      with open('user.txt', 'w') as file:
            file.write('')

      window.mainloop()

def Receive():



      main=Toplevel(root)
      main.title("Receive")
      main.geometry('450x560+500+200')
      main.configure(bg="#f4fdfe")
      main.resizable(False,False)

      def receiver():
            ID=SenderID.get()
            filename1=incoming_file.get()

            s=socket.socket()
            port=8080
            s.connect((ID,port))
            file=open(filename1,'wb')
            file_data=s.recv(1024)
            file.write(file_data)
            file.close()
            print("File has been received successfully")

      #icon
      image_icon1=PhotoImage(file=os.path.join(image_dir, "send.png"))
      main.iconphoto(False,image_icon1)

      Hbackground=PhotoImage(file=os.path.join(image_dir, "bg3.png"))
      Label(main,image=Hbackground).place(x=-2,y=0)

      logo=PhotoImage(file=os.path.join(image_dir, "bg5.png"))
      Label(main,image=logo,bg="#f4fdfe").place(x=10,y=250)

      Label(main,text="Receive",font=('arial',20),bg="#f4fdfe").place(x=100,y=280)

      Label(main,text="Input sender id",font=('arial',10,'bold'),bg="#f4fdfe").place(x=20,y=340)
      SenderID = Entry(main,width=25,fg="black",border=2,bg='white',font=('arial',15))
      SenderID.place(x=20,y=370)
      SenderID.focus()

      Label(main,text="Filename for the incoming file: ",font=('arial',10,'bold'),bg="#f4fdfe").place(x=20,y=420)
      incoming_file = Entry(main,width=25,fg="black",border=2,bg='white',font=('arial',15))
      incoming_file.place(x=20,y=450)

      # imageicon=PhotoImage(file="Image/arrow.png")
      rr= Button(main,text="Receive",compound=LEFT,width=30,bg="#39c790",font=('arial',14,'bold'),command=receiver)
      rr.place(x=20,y=500)

      main.mainloop()



      # Lấy đường dẫn của thư mục cơ sở
base_dir = os.path.dirname(os.path.abspath(__file__))

      # Thêm đường dẫn tương đối tới thư mục chứa file .png
image_dir = os.path.join(base_dir, "Image")
print(image_dir)

#icon
image_icon=PhotoImage(file=os.path.join(image_dir, "icon.png"))
root.iconphoto(False,image_icon)

Label(root,text="File Transfer",font=('Acumin Variable Concept',20,'bold'),
      bg="#f4fdfe").place(x=20,y=30)
Frame(root,width=400,height=2,bg="#f3f5f6").place(x=25,y=80)

send_image=PhotoImage(file=os.path.join(image_dir, "send.png"))
send=Button(root,image=send_image,bg="#f4fdfe",bd=0, width=100,height=100, command=Send)
send.place(x=50,y=100)

receive_image=PhotoImage(file=os.path.join(image_dir, "send.png"))
receive=Button(root,image=receive_image,bg="#f4fdfe",bd=0,width=100,height=100,command= Receive)
receive.place(x=300,y=100)

#label

Label(root,text="Send",font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65,y=200)
Label(root,text="Receive",font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300,y=200)










root.mainloop()