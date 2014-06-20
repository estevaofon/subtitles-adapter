#!/usr/bin/python
from timeFunctions import TimeOperations
import ntpath

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

