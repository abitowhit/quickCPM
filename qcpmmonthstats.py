#!/usr/bin/python
# -*- coding: utf-8 -*-s
import os  # directory methods
import datetime
import sys
import ftplib

daycount=0
d=datetime.date.today()
y=d.strftime('%Y')
m=d.strftime('%m')
print ("{0}/{1}".format(y,m))
ftpLp=0
ftpLimit=10
workDir = r"/home/pi/bin/quickcpm/logs"
os.chdir(workDir)
ftpOn='true'

ftpPath = r"/"
ftpU="ftpuser1"
ftpP="ftppw1"
ftpHost="ftphost1"

ftpBTHost="ftphost2"
ftpBTU="ftpuser2"
ftpBTP="ftppw2"
ftpBTPath=r"/"

def ftpSite1(filename):
    if (ftpOn == 'true'):
        try:
            cwd = os.getcwd()
            ftp = ftplib.FTP(ftpHost)
            ftp.login(ftpU, ftpP)
            ftp.cwd(ftpPath)
            if(cwd != workDir):
                os.chdir(workDir)
            ftp.storlines("STOR " + filename, open(filename,'rb',1024))
            print("[Site1 ftp ok]")
            ftp.close()
        except:
            print("....Site1 ftp failed")
            
def ftpSite2(filename):
    if (ftpOn == 'true'):
        try:
            cwd = os.getcwd()
            ftp = ftplib.FTP(ftpBTHost)
            ftp.login(ftpBTU, ftpBTP)
            ftp.cwd(ftpBTPath)
            if(cwd != workDir):
                os.chdir(workDir)
            ftp.storlines("STOR " + filename, open(filename,'rb',1024))
            print("[Site2 ftp ok]")
            ftp.close()
        except:
            print("....Site2 ftp failed")            
            
def writeToFile(fileName,data, isbinary, ishtml):
        if len(data)>1:
            fn= fileName # QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.*")with open("test.txt", "a") as myfile:
            if ishtml:
                    with open(fn, "w") as file:  
                        file.write(data)
                        print("{:d} chars written to {:s}".format(len(data),fn))
            else:
                    with open(fn, "a") as file:  
                        file.write(data)
                        print("{:d} chars written to {:s}".format(len(data),fn))
                    
        else:
            print ("No data to save")
            
def getArgs():
    if (len(sys.argv) > 0):
        for argv in sys.argv:
            if (argv.split('=')[0]=='m'):
                m=argv[1]
            if (argv.split('=')[0]=='y'):
                y=argv[1]
                return
            #    d.strftime('%m') and d.strftime('%d')
getArgs()

# read the files and get avgs
directory = os.fsencode(workDir)
i=0
avg=0
rv=0
maxcpm=0
ci = 0
for file in os.listdir(directory):
    i = i+1
    filename = os.fsdecode(file)
    if filename.endswith(".csv") and "_t" not in filename and "gmc_{0}{1}".format(y,m) in filename:
       # if daycount < 2:
            daycount = daycount +1
            print(filename)
            f= open(filename,"r")
            f1 = f.readlines()
            for x in f1:
                dstamp=x.split()[0]
                cpm=x.split(',')[1].strip()
                if ":" not in cpm:
                    dcpm =int(cpm.split('.')[0])
                    print(cpm)
                    avg = avg + dcpm
                    ci = ci + 1
                    if (dcpm > maxcpm):
                        maxcpm=dcpm
cx = avg / ci
cs = "{0}".format(cx)
fname="{0}{1}_CPM.html".format(y,m)
mths=["x","Jan","Feb","Mar","Apr","May","Jun","Jly","Aug","Sep","Oct","Nov","Dec"]
rpt ="<b>{5}</b><br>Average CPM for {4} days was {2}<br>maxCPM in {4} Days was {3}<br><hr>TotlalCPM: {0}<br>stamps: {1}<br>Processed:{6}".format(avg,ci,cs.split('.')[0],maxcpm,daycount,mths[int(m)],datetime.datetime.now())

writeToFile(fname,"<html><head></head><body>{0}</body></html>".format(rpt), 'false','true')                    
print (rpt.replace("<br>","\n").replace("<b>","").replace("</b>","\n"))
ftpSite1(fname)
ftpSite2(fname)
         #print(os.path.join(directory, filename))
