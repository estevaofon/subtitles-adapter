#!/usr/bin/python
from Tkinter import *
import tkMessageBox
from adapter import Adapter
from tkFileDialog import askopenfilename
import ntpath
import traceback

class Gui:
    def __init__(self):
        self.adapter = Adapter()
        self.seconds = 0
        self.opcao = 0
        self.filepath = ''
    def run(self):
        app = Tk()
        app.title("Ajustador de Legendas")
        app.geometry('380x180')

        self.labelText2 = StringVar()
        self.labelText2.set("")
        label2 = Label(app, textvariable=self.labelText2, height=2, fg='blue')
        label2.pack(side='top', padx=1, pady=1)

        labelText = StringVar()
        labelText.set("Segundos")
        label1 = Label(app, textvariable=labelText, height=2)
        label1.pack()

        custName= StringVar(None)
        self.entrada = Entry(app, textvariable=custName)
        self.entrada.pack()

        self.var = IntVar()

        R1 = Radiobutton(app, text="Atrasar legenda", variable=self.var, value=1,command=self.sel)
        R1.pack()

        R2 = Radiobutton(app, text="Adiantar legenda", variable=self.var, value=2,command=self.sel)
        R2.pack()

        button1 = Button(app, text="Adaptar", width=10, command = self.changeLabel)
        button1.pack(side='bottom', padx=10, pady=10)
        
        menubar = Menu(app)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Selecionar Legenda", command=self.filechoose)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=app.quit)
        menubar.add_cascade(label="Arquivo", menu=filemenu)
        
        aboutmenu = Menu(menubar, tearoff=0)

        aboutmenu.add_command(label="O App", command=self.newWindow)
        menubar.add_cascade(label="Sobre", menu=aboutmenu)

        app.config(menu=menubar)

        app.mainloop()
    def changeLabel(self):
        try:
            stringInput = self.entrada.get()
            self.seconds = int(stringInput)
            if self.opcao == 0:
                self.notSelected()
            else:
                self.adapter.adjust(self.filepath, self.seconds,self.opcao)
                self.pronto()
        except ValueError:
            self.wrongValue()
        except IOError:
            #traceback.print_exc()
            self.missingFile()
        #except:
            #self.unknowError()
        return

    def sel(self):
        self.opcao = self.var.get()
    def pronto(self):
        tkMessageBox.showinfo("Status", "Pronto!")
    def missingFile(self):
        tkMessageBox.showinfo("Status", "Arquivo nao selecionado!")
    def wrongValue(self):
        tkMessageBox.showinfo("Status", "Por favor insira apenas numeros!")
    def notSelected(self):
        tkMessageBox.showinfo("Status", "Selecione adiantar ou atrasar a legenda.")
    def unknowError(self):
        tkMessageBox.showinfo("Status", "Erro desconhecido!")
   
    def filechoose(self):
        self.filepath = askopenfilename()
        if self.filepath != '':
            self.labelText2.set(ntpath.basename(self.filepath))
    def newWindow(self):
        top = Toplevel()
        top.title("O App")
        top.geometry('380x80')
        labelText = StringVar()
        labelText.set("Aplicativo desenvolvido em Python por Estevao Fonseca")
        label1 = Label(top, textvariable=labelText, height=2)
        label1.pack(side='top', padx=10, pady=15)

        top.mainloop()
gui = Gui()
gui.run()
    

