from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
import subprocess


def CheckHex(str):
    for ch in str:
        if (('0' <= ch <= '9') or ('a' <= ch <= 'f') or ('A' <= ch <= 'F')):
            return 1
    return 0


def CheckDec(str):
    for ch in str:
        if ~('0' <= ch <= '9'):
            return 1
    return 0


def CheckBin(str):
    for ch in str:
        if ch != '1' and ch != '0':
            return 0
    return 1


root = Tk()
################################################
# Title
root.title("PCI TestBench Generator")
################################################
# root.geometry("500x500")
# root.resizable(0, 0)
################################################
# PCI_Name = StringVar()
lbl = ttk.Label(root, text='Enter PCI Module Name').grid(row=0, column=0, padx=5, pady=5)
Ent = ttk.Entry(root, width=20)
Ent.grid(row=0, column=1, padx=5, pady=5)
################################################
lblClk = ttk.Label(root, text='Enter Clk Module Name').grid(row=1, column=0, padx=5, pady=5)
EntClk = ttk.Entry(root, width=20)
EntClk.grid(row=1, column=1, padx=5, pady=5)
Clk = ttk.Entry(root, width=15)
Clk.grid(row=1, column=3, padx=5, pady=5)
Clk.insert(0, "In Nano Seconds")
Clk.configure(state=DISABLED)


def on_click(event):
    Clk.configure(state=NORMAL)
    Clk.delete(0, END)


Clk.bind('<Button-1>', on_click)
ClkBTN = ttk.Button(root, text='Enter Clk Period')
ClkBTN.grid(row=1, column=4, padx=5, pady=5)


def Enter_Clk():
    Clk_Period = Clk.get() if (Clk.get() != "In Nano Seconds" and Clk.get() != "") else 20
    Clk.configure(state=DISABLED)
    ClkBTN.state(['disabled'])
    return Clk_Period


ClkBTN.configure(command=Enter_Clk)
# Clk_Period is the variable
##################################################
lbl1 = ttk.Label(root, text='PCI Device Address')
lbl1.grid(row=2, column=1, padx=5, pady=5)
Add = ttk.Entry(root, width=40)
Add.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
Add.configure(state=DISABLED)
MenuList = ["Mode", "Binary", "Decimal", "Hexadecimal"]
varList = tk.StringVar(root)
varList.set(MenuList[0])
Mode1 = ttk.OptionMenu(root, varList, *MenuList)
Mode1.grid(row=2, column=0, padx=5, pady=5)
Mode = {'Binary': '', 'Decimal': '', 'Hexadecimal': ''}
Mod = varList.get()


def my_show(*args):
    Add.configure(state=NORMAL)
    Mod = varList.get()
    print(Mod)


varList.trace('w', my_show)
AddBTN = ttk.Button(root, text='Enter Address')
AddBTN.grid(row=2, column=4, padx=5, pady=5)


def Enter_Add():
    Mode[Mod] = Add.get()
    if varList.get() == 'Hexadecimal':
        if CheckHex(Add.get()):
            if len(Mode['Hexadecimal']) >= 8:
                Mode['Hexadecimal'] = Add.get()[0:8]
            else:
                part = "0000000" + Add.get()
                Mode['Hexadecimal'] = part[-8:]
        else:
            Mode['Hexadecimal'] = "zzzzzzzz"
    elif varList.get() == 'Decimal':
        if CheckDec(Add.get()):
            part: str = ""
            Test = str(hex(int(Mode[Mod])))
            for i in range(2, len(Test)):
                part += Test[i]
                if len(part) >= 8:
                    Mode['Hexadecimal'] = part[0:8]
                else:
                    part0 = "0000000" + part
                    Mode['Hexadecimal'] = part0[-8:]
        else:
            Mode['Hexadecimal'] = "zzzzzzzz"
    else:
        if CheckBin(Add.get()):
            Test = str(hex(int(str(int(Mode[Mod])), 2)))
            part = ""
            for i in range(2, len(Test)):
                part += Test[i]
                if len(part) >= 8:
                    Mode['Hexadecimal'] = part[0:8]
                else:
                    part0 = "0000000" + part
                    Mode['Hexadecimal'] = part0[-8:]
        else:
            Mode['Hexadecimal'] = "zzzzzzzz"
    print(Mode['Hexadecimal'])
    Add.delete(0, END)
    Add.insert(0, str(Mode['Hexadecimal']))
    varList.set(MenuList[3])
    Mode1.configure(state=DISABLED)
    Add.configure(state=DISABLED)
    AddBTN.state(['disabled'])


AddBTN.configure(command=Enter_Add)
# We stored the address
#########################################################
lbl2 = ttk.Label(root,
                 text="--------------------------------------------  PCI Master Signals  ---------------------------------------------")
lbl2.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
Counter = 1
txt = "Clk no. " + str(Counter)
lbl3 = ttk.Label(root, text=txt)
lbl3.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
################################################################################
PCI_Frame = StringVar()
PCI_Frame.set('yes')
cb1 = ttk.Checkbutton(root, text=' #Frame', variable=PCI_Frame, onvalue='yes', offvalue='no')
cb1.grid(row=5, column=0, padx=10, pady=10)

PCI_Irdy = StringVar()
PCI_Irdy.set('yes')
cb2 = ttk.Checkbutton(root, text=' #Irdy', variable=PCI_Irdy, onvalue='yes', offvalue='no')
cb2.grid(row=5, column=1, padx=10, pady=10)

PCI_Stop = StringVar()
PCI_Stop.set('yes')
cb2 = ttk.Checkbutton(root, text=' #Stop', variable=PCI_Stop, onvalue='yes', offvalue='no', state='disabled')
cb2.grid(row=5, column=4, padx=10, pady=10)

PCI_DevSel = StringVar()
PCI_DevSel.set('yes')
cb3 = ttk.Checkbutton(root, text=' #DevSel', variable=PCI_DevSel, onvalue='yes', offvalue='no', state='disabled')
cb3.grid(row=5, column=3, padx=10, pady=10)

PCI_Trdy = StringVar()
PCI_Trdy.set('yes')
cb4 = ttk.Checkbutton(root, text=' #Trdy', variable=PCI_Trdy, onvalue='yes', offvalue='no', state='disabled')
cb4.grid(row=5, column=2, padx=10, pady=10)
################################################################################
lbl4 = ttk.Label(root, text='C/BE').grid(row=6, column=0, padx=10, pady=10)
BE = ttk.Entry(root, width=10, state='disabled')
BE.grid(row=6, column=1, padx=10, pady=10)


def control():
    CBE = str(BE.get())[0:4]
    PCI_CBE = ""
    for i in CBE:
        if i != '0' and i != '1':
            PCI_CBE += '1'
        else:
            PCI_CBE += i
    BE.delete(0, END)
    BE.insert(0, PCI_CBE)
    BE.configure(state=['disabled'])
    BE1.configure(state=['disabled'])
    print(PCI_CBE)


BE1 = ttk.Button(root, text='Enter C/BE', state='disabled')
BE1.grid(row=6, column=2, padx=10, pady=10)
BE1.configure(command=control)
PCI_Control = StringVar()
# rbvalue is the variable
read = ttk.Radiobutton(root, text='Read', variable=PCI_Control, value='read')
read.grid(row=6, column=3, padx=5, pady=5)
write = ttk.Radiobutton(root, text='Write', variable=PCI_Control, value='write')
write.grid(row=6, column=4, padx=5, pady=5)
#########################################################################################
lbl5 = ttk.Label(root, text='Address/Data').grid(row=7, column=1, padx=10, pady=10)
varList2 = tk.StringVar(root)
varList2.set(MenuList[0])
Mode2 = ttk.OptionMenu(root, varList2, *MenuList)
Mode2.grid(row=7, column=0, padx=10, pady=10)
Mode3 = {'Binary': '', 'Decimal': '', 'Hexadecimal': ''}
Mod2 = varList2.get()


def show(*args):
    DataEntry.configure(state=NORMAL)


DataEntry = ttk.Entry(root, width=40, state='disabled')


def Enter_Data():
    Mode3[Mod2] = DataEntry.get()
    if varList2.get() == 'Hexadecimal':
        if CheckHex(DataEntry.get()):
            if len(Mode3['Hexadecimal']) >= 8:
                Mode3['Hexadecimal'] = DataEntry.get()[0:8]
            else:
                part = "0000000" + DataEntry.get()
                Mode3['Hexadecimal'] = part[-8:]
        else:
            Mode3['Hexadecimal'] = "zzzzzzzz"
    elif varList2.get() == 'Decimal':
        if CheckDec(DataEntry.get()):
            part: str = ""
            Test = str(hex(int(Mode3[Mod2])))
            for i in range(2, len(Test)):
                part += Test[i]
                if len(part) >= 8:
                    Mode3['Hexadecimal'] = part[0:8]
                else:
                    part0 = "0000000" + part
                    Mode3['Hexadecimal'] = part0[-8:]
        else:
            Mode3['Hexadecimal'] = "zzzzzzzz"
    else:
        if CheckBin(DataEntry.get()):
            Test = str(hex(int(str(int(Mode3[Mod2])), 2)))
            part = ""
            for i in range(2, len(Test)):
                part += Test[i]
                if len(part) >= 8:
                    Mode3['Hexadecimal'] = part[0:8]
                else:
                    part0 = "0000000" + part
                    Mode3['Hexadecimal'] = part0[-8:]
        else:
            Mode3['Hexadecimal'] = "zzzzzzzz"
    DataEntry.delete(0, END)
    DataEntry.insert(0, str(Mode3['Hexadecimal']))
    varList2.set(MenuList[3])
    Mode2.configure(state=DISABLED)
    DataEntry.configure(state=DISABLED)
    DataBTN.state(['disabled'])
    return (Mode3['Hexadecimal'])


varList2.trace('w', show)
DataEntry.grid(row=7, column=2, columnspan=2, padx=10, pady=10)
DataBTN = ttk.Button(root, text='Enter Address/Data')
DataBTN.grid(row=7, column=4, padx=10, pady=10)
DataBTN.configure(command=Enter_Data)
#####################################################################
NextClk = ttk.Button(root, text='Next Clk')
NextClk.grid(row=8, column=3, padx=10, pady=10)
Control = ""
count = 0
Address = ""


def Next():
    global count, Counter, Control, Address
    if Counter == 1:
        if os.path.isfile('Testbench.v'):
            os.remove("Testbench.v")
        fh = open("Testbench.v", 'w')
        fh.write("module testbench(Trdy, Devsel, Stop, Address);\nreg[31:0] W2, Mem[0:7];\n")
        PCI_Clk_Name = EntClk.get()
        if PCI_Clk_Name != "":
            fh.write(PCI_Clk_Name)
        else:
            fh.write("clk")
        fh.write(" c1(Clk);\ninout [31:0]Address;\ninput Stop, Devsel, Trdy;\n")
        fh.write("reg [3:0] Cbe;\nreg flg, count, Rst, Frame, Irdy;\nwire[31:0] W1;\n")
        PCI_Name = Ent.get()
        if PCI_Name != "":
            fh.write(PCI_Name)
        else:
            fh.write("PCI")
        fh.write(" p1(Clk, Rst, Frame, Irdy, Trdy, Address, Cbe, Devsel, Stop);\n")
        fh.write("assign Address = flg? W2 : 32'hzzzzzzzz;\nassign W1 = Address;\n")
        fh.write("//Beginig Testbench\ninitial begin\n\t$dumpfile(\"test.vcd\");\n\t$dumpvars(0,testbench);\nend\n")
        fh.write("initial begin\n\tcount <= 1'b0;\n\tW2 <= 32'hzzzzzzzz;\n\tflg <= 1'b1;\n")
        fh.write("\tRst <= 1'b1;\n\tFrame <= 1'b1;\n\tIrdy <= 1'b1;\n")
        ##############################################################################
        fh.write("\twhile(Trdy == 1'b1 && count == 1'b1) begin\n\t\t#" + str(Enter_Clk()) + " ;//Do Nothing\n\tend\n")
        fh.write("\t#" + str(Enter_Clk()) + "\n\t\tRst <= 1'b0;\n")
        if PCI_Frame.get() == "yes":
            fh.write("\t\tFrame <= 1'b1;\n\t\tcount <= 1'b1;\n")
            read.configure(state=['normal'])
            write.configure(state=['normal'])
            fh.write("\t\tW2 <= 32'hzzzzzzzz;\n\t\tCbe <= 4'bzzzz;\n\t\tIrdy <= 1'b1;\n")
            fh.write("")
        elif PCI_Frame.get() == "no":
            fh.write("\t\tFrame <= 1'b0;\n")
            read.configure(state=['disabled'])
            write.configure(state=['disabled'])
            count += 1
            if count == 1:
                if Mode3['Hexadecimal'] != '':
                    fh.write("\t\tW2 <= 32'h" + str(Mode3['Hexadecimal']) + ";\n")
                else:
                    fh.write("\t\tW2 <= 32'hzzzzzzzz;\n")
                if PCI_Irdy.get() == "yes":
                    fh.write("\t\tIrdy <= 1'b1;\n")
                elif PCI_Irdy.get() == "no":
                    fh.write("\t\tIrdy <= 1'b0;\n")
                Control += PCI_Control.get()
                PCI_Irdy.set("no")
                if Control == "write":
                    fh.write("\t\tCbe <= 4'b0011;   //Write operation\n")
                    BE.configure(state=['normal'])
                    BE1.configure(state=['normal'])
                    PCI_Trdy.set("no")
                    Ad = Mode['Hexadecimal'] if Mode['Hexadecimal'] != "" else "00001f40"
                    if DataEntry.get() == Ad:
                        PCI_DevSel.set("no")
                else:
                    fh.write("\t\tCbe <= 4'b0010;   //Read operation\n")
                    PCI_Control.set("read")
                    BE.configure(state=['normal'])
                    BE1.configure(state=['normal'])
                    # fh.write("\t\tMem[count] <= W1;\n\t\tcount = count + 1;\n")
                Address += DataEntry.get()
        Counter = Counter + 1
        newtxt = "Clk no. " + str(Counter)
        lbl3.config(text=newtxt)
        Mode2.configure(state=['normal'])
        DataEntry.configure(state=['normal'])
        DataEntry.delete(0, END)
        varList2.set(MenuList[0])
        DataEntry.configure(state=['disabled'])
        DataBTN.configure(state=['normal'])
    else:
        fh = open("Testbench.v", 'a')
        fh.write("\twhile(Trdy == 1'b1 && count == 1'b1) begin\n\t\t#" + str(Enter_Clk()) + " ;//Do Nothing\n\tend\n")
        fh.write("\t#" + str(Enter_Clk()) + "\n")
        if PCI_Frame.get() == "yes":
            fh.write("\t\tFrame <= 1'b1;\n\t\tcount <= 1'b1;\n")
            read.configure(state=['normal'])
            write.configure(state=['normal'])
        elif PCI_Frame.get() == "no":
            fh.write("\t\tFrame <= 1'b0;\n")
            read.configure(state=['disabled'])
            write.configure(state=['disabled'])
            count += 1
            if count == 1:
                PCI_Irdy.set("no")
                if Mode3['Hexadecimal'] != '':
                    fh.write("\t\tW2 <= 32'h" + str(Mode3['Hexadecimal']) + ";\n")
                else:
                    fh.write("\t\tW2 <= 32'hzzzzzzzz;\n")
                if PCI_Irdy.get() == "yes":
                    fh.write("\t\tIrdy <= 1'b1;\n")
                elif PCI_Irdy.get() == "no":
                    fh.write("\t\tIrdy <= 1'b0;\n")
                Control += PCI_Control.get()
                if Control == "write":
                    fh.write("\t\tCbe <= 4'b0011;   //Write operation\n")
                    BE.configure(state=['normal'])
                    BE1.configure(state=['normal'])
                    PCI_Trdy.set("no")
                    Ad = Mode['Hexadecimal'] if Mode['Hexadecimal'] != "" else "00001f40"
                    if DataEntry.get() == Ad:
                        PCI_DevSel.set("no")
                else:
                    fh.write("\t\tCbe <= 4'b0010;   //Read operation\n")
                    PCI_Control.set("read")
                    BE.configure(state=['normal'])
                    BE1.configure(state=['normal'])
                    # fh.write("\t\tMem[count] <= W1;\n\t\tcount = count + 1;\n")
                Address += DataEntry.get()
            if (Control == "read" and count == 2):
                PCI_Trdy.set("no")
                Ad = Mode['Hexadecimal'] if Mode['Hexadecimal'] != "" else "00001f40"
                if Address == Ad:
                    PCI_DevSel.set("no")
                fh.write("\t\tW2 <= 32'hzzzzzzzz;\n")
        if Control == "write" and count != 0:
            if Mode3['Hexadecimal'] != '':
                fh.write("\t\tW2 <= 32'h" + str(Mode3['Hexadecimal']) + ";\n")
            else:
                fh.write("\t\tW2 <= 32'hzzzzzzzz;\n")
            BE.configure(state=['normal'])
            BE.delete(0, END)
            BE1.configure(state=['normal'])
        if Control == "read" and count > 1:
            fh.write("\t\tMem[count] <= W1;\n\t\tcount = count + 1;\n")
            BE.configure(state=['normal'])
            BE.delete(0, END)
            BE1.configure(state=['normal'])
        if PCI_Irdy.get() == "yes":
            fh.write("\t\tIrdy <= 1'b1;\n")
        elif PCI_Irdy.get() == "no":
            fh.write("\t\tIrdy <= 1'b0;\n")
        if BE.get() == '':
            fh.write("\t\tCbe <= 4'bzzzz;\n")
        else:
            fh.write("\t\tCbe <= 4'b" + str(BE.get()) + ";\n")
        Counter = Counter + 1
        newtxt = "Clk no. " + str(Counter)
        lbl3.config(text=newtxt)
        Mode2.configure(state=['normal'])
        DataEntry.configure(state=['normal'])
        DataEntry.delete(0, END)
        varList2.set(MenuList[0])
        DataEntry.configure(state=['disabled'])
        DataBTN.configure(state=['normal'])
    print("clicked")


NextClk.configure(command=Next)


def Fnsh():
    PCI_Trdy.set("yes")
    PCI_Irdy.set("yes")
    PCI_DevSel.set("yes")
    fh = open("Testbench.v", 'a')
    fh.write("\t#" + str(Enter_Clk()) + "\n")
    fh.write("\t\tFrame <= 1'b1;\n")
    fh.write("\t\tIrdy <= 1'b1;\n")
    fh.write("\t\tCbe <= 4'bzzzz;\n")
    fh.write("\t\tW2 <= 32'hzzzzzzzz;\n")
    fh.write("\tend\nendmodule")
    fh.close()


Finish = ttk.Button(root, text='End Module')
Finish.grid(row=8, column=4, padx=10, pady=10)
Finish.configure(command=Fnsh)


def opening():
    os.system("notepad testbench.v")


opn = ttk.Button(root, text='Open Testbench file')
opn.grid(row=8, column=0, padx=10, pady=10)
opn.configure(command=opening)
#########################################################################################################
# Simulation Part
lbl2 = ttk.Label(root,
                 text="--------------------------------------------  Simulation Part  ---------------------------------------------")
lbl2.grid(row=9, column=0, columnspan=5, padx=5, pady=5)
filelbl = ttk.Label(root, text='Enter PCI & Testbench file Name').grid(row=10, column=0, padx=5, pady=5)
fileEnt = ttk.Entry(root, width=20)
fileEnt.grid(row=10, column=1, padx=5, pady=5)
TestEnt = ttk.Entry(root, width=20)
TestEnt.grid(row=10, column=2, padx=5, pady=5)
FileName = ""
TestName = ""
Sim = ttk.Button(root, width=20, text="Simulate")
Sim.grid(row=10, column=3, padx=10, pady=10)
kill = ttk.Button(root, width=20, text="Plot")
kill.grid(row=10, column=4, padx=10, pady=10)


def Simulate():
    global FileName, TestName
    if fileEnt.get() == "":
        FileName += "PCI.v"
    elif fileEnt.get()[-1] == "v" and fileEnt.get()[-2] == ".":
        FileName += fileEnt.get()
    else:
        FileName += (fileEnt.get() + ".v")
    if TestEnt.get() == "":
        TestName += "Testbench.v"
    elif TestEnt.get()[-1] == "v" and TestEnt.get()[-2] == ".":
        TestName += TestEnt.get()
    else:
        TestName += (TestEnt.get() + ".v")
    print(FileName, TestName)
    fileEnt.configure(state=['disabled'])
    TestEnt.configure(state=['disabled'])
    os.system("copy " + TestName + " c:\iverilog\\bin\\")
    os.system("copy " + FileName + " c:\iverilog\\bin\\")
    os.system("dir")
    os.chdir("c:\iverilog\\bin\\")
    os.system("iverilog -o dsn Testbench.v " + FileName)
    os.system("vvp dsn -s")
    # os.system("taskkill /f /im vvp.exe")
    os.chdir("..\gtkwave\\bin\\")
    os.chdir("..\..\\bin\\")
    os.system("move test.vcd c:\iverilog\\gtkwave\\bin\\")
    os.chdir("..\gtkwave\\bin\\")
    os.system("gtkwave test.vcd")


def killed():
    os.system("taskkill /f /im vvp.exe")


kill.configure(command=killed)
Sim.configure(command=Simulate)
root.mainloop()
