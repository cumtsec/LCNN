
# coding: utf-8
# In[6]:

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

class DataCut:
    def _init_(self,linegaptemp=1):
        linegap=linegaptemp  #隔行读取
        ofl = []  # original file list


    def loadfilelist(self):
        ofilelist1 = os.listdir('./originaldata')
        self.ofl=ofilelist1.copy()
        self.ofl.sort()

    def cutfileasgroup(self):
        for cfn in dc.ofl:
            self.cutsinglefile(cfn);

    def cutsinglefile(self,curfilename):
        data_cut_name = curfilename  #r"./originaldata/哈尔乌素煤矿_1025-pd_102_17_20190430165221.log"
        data_name =curfilename.split('.')+"_line9.txt";  #"./train_set/data_line9_17_6_20190430165221.txt"
        self.label_name = curfilename.split('.')+"_line9_label.txt";   #"./train_set/data_line9_label_17_6_20190430165221.txt"
        inFile = open(data_cut_name,'r')
        y = []
        j=1
        for line in inFile:                    #循环遍历每行文本数据
            j=j+1
            if j%self.linegap==0:                         #隔行读取
                train = line.split(',')        #将用逗号隔开的数据存放到列表中
                if(train.__len__()<9):
                    continue;
                y.append(float(train[8]))      #将数据第九列加入空列表中
        lens = len(y)
        datasave=open(data_name,"w")
        #存数据,line9
        for i in range(lens):
            txt=str(y[i])
            datasave.write(txt)
            if i==lens-1:
                break
            datasave.write(",")
        datasave.close()
        self.inflexion(data_name)

    def inflexion(self,data_name):
        #读数据
        inFile = open(data_name)
        data=inFile.read()
        data=data.split(',')
        lens=len(data)
        print(lens)
        print(data)
        lens=len(data)
        y=[]
        rise=[]
        down=[]
        for i in range(lens):
            y.append(float(data[i]))
        leny=len(y)
        for i in range(leny-1):
            value=y[i+1]-y[i]
            #寻找跳变位置
            if value>=30000:
                if len(rise)==0:
                    rise.append(i)
                #判断跳点的位置间距是否太小
                elif i-rise[len(rise)-1]>=4000:
                    rise.append(i)
                else:
                    pass
            if value<=-35000:
                if len(down)==0:
                    down.append(i)
                #判断跳点的位置间距是否太小
                elif i-down[len(down)-1]>=4000:
                    down.append(i)
                #间距太小否定上一个位置
                else:
                    down.pop()
        print(rise)
        print(down)
        self.savelabel(rise,down)


    def savelabel(self,rise,down):
        label_name=self.label_name;
        a=[[0 for i in range(2)] for i in range(len(down))]
        labelFile=open(label_name,"a")
        for i in range(len(down)):  ##写label文件

            for j in range(len(rise)):
                if rise[j]>down[i]:
                    a[i][0]=down[i]
                    a[i][1]=rise[j]
                    print(down[i],rise[j],"is good",sep=",")
                    if i==0:
                        labelFile.write(str(down[i]))
                        labelFile.write(",")
                        labelFile.write(str(rise[j]))
                    else:
                        labelFile.write(",")
                        labelFile.write(str(down[i]))
                        labelFile.write(",")
                        labelFile.write(str(rise[j]))
                    break
        labelFile.close()
        print(a)


if __name__ == '__main__':
    dc=DataCut(2);





