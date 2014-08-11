#!/usr/bin/python
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import traceback
import datetime
import ntpath


#class TimeOperations:
#class Adapter:
#class Gui:

class TimeOperations:
    def createTime(self,h,m,s):
        return datetime.datetime(100,1,1,h,m,s).time()
    def addSecs(self,tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
        return fulldate.time()
    def subSecs(self,tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate - datetime.timedelta(seconds=secs)
        return fulldate.time()

class Adapter:
    def timeToSec(self,h,m,s):
        h = int(h)
        m = int(m)
        s , mili = s.split(',')
        s = int(s)
        hSec = h*3600
        mSec= m*60
        inSec = hSec+mSec+s
        return inSec

    def adjust(self,f,deltaT,opcao):
        try:
            with open(f,'r') as data:
                list1 = data.readlines()
                mili = []
                mili2 = []
                u = 0
                timeop = TimeOperations()
                tempos1 = []
                localToGlobal = {}
                temposErrados = []
                temposErradosGlobais = []
                for i in range(len(list1)):
                    if '-->' in list1[i]:
                        (temp1, temp2) = list1[i].split('-->')
                        temp1 = temp1.strip()
                        temp2 = temp2.strip()
                        h1,m1,s1 = temp1.split(':')
                        h2,m2,s2 = temp2.split(':')
                        
                        h1 = int(h1)
                        m1 = int(m1)
                        h2 = int(h2)
                        m2 = int(m2)
                        
                        s1, ml1 = s1.split(',')
                        mili.append(ml1)
                        s1 = int(s1)
                        
                        s2, ml2 = s2.split(',')
                        mili2.append(ml2)
                        s2 = int(s2)
                        
                        if s1>59:
                            s1=59
                        if s2>59:
                            s2=59
                        
                        oldTime1 = timeop.createTime(h1,m1,s1)
                        oldTime2 = timeop.createTime(h2,m2,s2)
                        if opcao == 1:
                            newTime1 = timeop.addSecs(oldTime1, deltaT)
                            newTime2 = timeop.addSecs(oldTime2, deltaT)
                        if opcao == 2:
                            newTime1 = timeop.subSecs(oldTime1, deltaT)
                            newTime2 = timeop.subSecs(oldTime2, deltaT)
                        
                        tempo1 = str(newTime1)+','+mili[u]
                        tempos1.append(tempo1)
                        localToGlobal[len(tempos1)-1]=i

                        list1[i]= str(newTime1)+','+mili[u]+' '+'-->'+' '+str(newTime2)+','+mili2[u]+'\r\n'
                        u = u + 1
                tempFinal = tempos1[len(tempos1)-1]
                tempFinal = tempFinal.strip()
                hf , mf, sf = tempFinal.split(':')
                tempFinal = self.timeToSec(hf, mf, sf)

                for i in range(len(tempos1)):
                    temp = tempos1[i].strip()
                    h1,m1,s1 = temp.split(':')
                    temp = self.timeToSec(h1,m1,s1)
                    if temp > tempFinal:
                        temposErrados.append(i)

                for i in range(len(temposErrados)):
                    temposErradosGlobais.append(localToGlobal[i])
                
                i0 = localToGlobal[len(temposErrados)]-1
                newList1 = list1[i0:]

                w=1
                for i in range(len(newList1)):
                    if '-->' in newList1[i]:
                        newList1[i-1]=str(w)+'\r\n'
                        w = w + 1

                filename = ntpath.basename(f)
                newfilename = filename.replace('.srt', '-new.srt')
                finalfile = f.replace(filename, newfilename)
                with open(finalfile,'w') as data:
                    data.writelines(newList1)
        except IOError:
            print('The datafile is missing!')
            raise
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
    
