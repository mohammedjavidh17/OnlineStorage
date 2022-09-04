from tkinter import *
from tkinter import messagebox
from Client import *
from tkinter import ttk
from tkinter.ttk import Radiobutton

rt = Tk()
rt.title("Zettabyte")
rt.geometry("1500x800")
fnt = ("Consolas", 15)
fnt1= ("Consolas", 20)
def ClearAll():
    for x in rt.winfo_children():
        x.destroy()

def DisWind(Con : pd.DataFrame):
    def Preview():
        PrevFrm = Frame(rt)
        PrevFrm.place(relx=0.2, rely=0.02,anchor=NW, relwidth=0.8, relheight=0.8)
        prev = Text(PrevFrm)
        prev.place(relx=0.01, rely=0.01, relheight=0.99, relwidth=0.99)
        indx = "READ "+str(Sel.get()+1)+" "+Ext[int(Sel.get())]
        dta = GetFile(indx).decode('utf-8')
        prev.insert(END, str(dta))
    s = ttk.Style()
    s.configure('my.TButton', font=('Consolas', 12))
    ClearAll()
    print(Con)
    FileNames = list(Con.iloc[:, 1])
    Ext = list(Con.iloc[:, 2])
    DisFiles = Frame(rt)
    DisFiles.place(relx=0.02, rely=0.02, anchor=NW)
    Sel = IntVar()
    Sel.set(None)
    Label(DisFiles, text="YourFiles", font=fnt).pack()
    for i,x in enumerate(FileNames):
        Radiobutton(DisFiles, text=str(x)+'.'+Ext[i], value=i, variable=Sel, style='my.TButton', command=Preview).pack(padx=10, pady=10, fill='x')

def AuthWindow():
    def SignWindow():
        def PreSign():
            NewId = str(Id.get())
            NPas = str(pas.get())
            Cmd = 'NEW '+NewId+" "+NPas
            rep =NewUser(Cmd.encode('utf-8'))
            if  rep == 'EXIST':
                messagebox.showerror("Error", "User Id already exist")
            elif rep == 'False':
                messagebox.showerror("Error", "Something went wrong")
            elif rep == 'DONE':
                messagebox.showinfo("Sucess", "Successfully ID created")
        FrmSign = Frame(rt)
        FrmSign.place(relx=0.5, rely=0.5, anchor=CENTER, relheight=0.98, relwidth=0.98)
        FrmSign.tkraise()
        Label(FrmSign, text="Create ID", font=fnt).pack(pady=5)
        Id = Entry(FrmSign, width=20, font=fnt)
        Id.pack(pady=5)
        Label(FrmSign, text="Create Password", font=fnt).pack(pady=5)
        pas = Entry(FrmSign, width=20, font=fnt)
        pas.pack(pady=5)
        Button(FrmSign, text="Create Account", font=fnt, command=PreSign).pack(pady=10)
    def preAuth():
        cmd = "AUTH "+str(ID.get())+" "+str(pas.get())
        rep = ReqAccess(cmd)
        if rep == "Invalid":
            messagebox.showerror('wrong cred', "try again")
            return None
        Config = csvOrga(rep)
        DisWind(Config)
    
    frm = Frame(rt)
    frm.place(relx=0.5, rely=0.5, anchor=CENTER)
    Label(frm, text="UserID ", padx=10, font=fnt).pack(padx=5, pady=20)
    ID = Entry(frm, width=20, font=fnt)
    ID.pack(padx=20, pady=5)
    Label(frm, text="Password ", padx=10, font=fnt).pack(padx=5, pady=20)
    pas = Entry(frm, width=20, font=fnt)
    pas.pack(padx=20, pady=5)
    Button(frm, text="Log In",font=fnt, command=preAuth).pack(pady=5)
    Button(frm, text="Sign Up", font=fnt, command= SignWindow).pack(pady=5)

def mainWindow():
    AuthWindow()
if(s.recv(1024) == b'READY'):
    mainWindow()
else:
    messagebox.showerror('Error', 'Server Not responding')
rt.mainloop()
