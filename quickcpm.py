#!/usr/bin/python
# -*- coding: utf-8 -*-s
import os  # directory methods
import struct
import datetime
import time
import serial
import sys
import ftplib

gmc= serial.Serial('/dev/ttyUSB0', 115200, timeout= 3) #device
peak=0 #initial peak
slp=300 #interval 5min
gaugeType="radial"
pageBanner="Home Monitor - <span style=\"font-size:x-small\">Updated:{0}</span>".format("{:%m/%d/%Y %H:%M:%S}".format(datetime.datetime.now()));
ftpLp=0
ftpLimit=10
workDir = r"/home/pi/bin/quickcpm" #set location of quickCPM.py
ftpPath = r"/"
ftpU="ftpusername" #set ftp username
ftpP="ftppassword" #set ftp password
ftpHost="ftphostname" #set ftp host
ftpOn=true #use ftp

def ftpQCPM():
    if (ftpOn):
        try:
            cwd = os.getcwd()
            ftp = ftplib.FTP(ftpHost)
            ftp.login(ftpU, ftpP)
            ftp.cwd(ftpPath)
            if(cwd != workDir):
                os.chdir(workDir)
            ftp.storlines("STOR " + "QCPMgauge.html", open("QCPMgauge.html",'rb',1024))
            ftp.storlines("STOR " + "QCPMbar.html", open("QCPMbar.html",'rb',1024))
            print("[ftp ok]")
        except:
            print("....ftp failed")
#ftp.storlines("STOR " + "gauge.min.js", open("gauge.min.js",'rb',1024))

def gaugeCPMScrpt(id,value,title,unit):
    ghpg = "\n\n<canvas id=\"gauge-ps{0}\"></canvas>\n".format(id)
    ghpg += "<script>\n"
    ghpg += "var gaugePScpm = new RadialGauge({\n"
    ghpg += "renderTo: 'gauge-ps{0}',\n".format(id)
    ghpg += "width: 200,\n"
    ghpg += "height: 200,\n"
    ghpg += "units: '{0}',\n".format(unit);
    ghpg += "minValue: 0,\n"
    ghpg += "maxValue: 1000,\n"
    ghpg += "majorTicks: [\n"
    ghpg += "'0',\n"
    ghpg += "'100',\n"
    ghpg += "'200',\n"
    ghpg += "'300',\n"
    ghpg += "'400',\n"
    ghpg += "'500',\n"
    ghpg += "'600',\n"
    ghpg += "'700',\n"
    ghpg += "'800',\n"
    ghpg += "'900',\n"
    ghpg += "'1000'\n"
    ghpg += "],\n"
    ghpg += "minorTicks: 2,\n"
    ghpg += "ticksAngle: 270,\n"
    ghpg += "startAngle: 45,\n"
    ghpg += "strokeTicks: true,\n"
    ghpg += "highlights  : [\n"
    ghpg += "{ from : 0,  to : 100, color : 'green' },\n"#rgba(78,   78, 76, 0.5)
    ghpg += "{ from : 100,  to : 200, color : 'yellow' },\n"#rgba(78,   78, 76, 0.5)
    ghpg += "{ from : 200, to : 1000, color : 'rgba(225, 7, 23, 0.75)' }\n"
    ghpg += "],\n"
    ghpg += "valueInt: 1,\n"
    ghpg += "valueDec: 0,\n"
    ghpg += "colorPlate: \"#fff\",\n"
    ghpg += "colorMajorTicks: \"#686868\",\n"
    ghpg += "colorMinorTicks: \"#686868\",\n"
    ghpg += "colorTitle: \"#000\",\n"
    ghpg += "colorUnits: \"#000\",\n"
    ghpg += "colorNumbers: \"#686868\",\n"
    ghpg += "valueBox: true,\n"
    ghpg += "colorValueText: \"#000\",\n"
    ghpg += "colorValueBoxRect: \"#fff\",\n"
    ghpg += "colorValueBoxRectEnd: \"#fff\",\n"
    ghpg += "colorValueBoxBackground: \"#fff\",\n"
    ghpg += "colorValueBoxShadow: false,\n"
    ghpg += "colorValueTextShadow: false,\n"
    ghpg += "colorNeedleShadowUp: true,\n"
    ghpg += "colorNeedleShadowDown: false,\n"
    ghpg += "colorNeedle: \"rgba(200, 50, 50, .75)\",\n"
    ghpg += "colorNeedleEnd: \"rgba(200, 50, 50, .75)\",\n"
    ghpg += "colorNeedleCircleOuter: \"rgba(200, 200, 200, 1)\",\n"
    ghpg += "colorNeedleCircleOuterEnd: \"rgba(200, 200, 200, 1)\",\n"
    ghpg += "borderShadowWidth: 0,\n"
    ghpg += "borders: true,\n"
    ghpg += "borderInnerWidth: 0,\n"
    ghpg += "borderMiddleWidth: 0,\n"
    ghpg += "borderOuterWidth: 5,\n"
    ghpg += "colorBorderOuter: \"#fafafa\",\n"
    ghpg += "colorBorderOuterEnd: \"#cdcdcd\",\n"
    ghpg += "needleType: \"arrow\",\n"
    ghpg += "needleWidth: 2,\n"
    ghpg += "needleCircleSize: 7,\n"
    ghpg += "needleCircleOuter: true,\n"
    ghpg += "needleCircleInner: false,\n"
    ghpg += "animationDuration: 1500,\n"
    ghpg += "animationRule: \"dequint\",\n"
    ghpg += "fontNumbers: \"Verdana\",\n"
    ghpg += "fontTitle: \"Verdana\",\n"
    ghpg += "fontUnits: \"Verdana\",\n"
    ghpg += "fontValue: \"Led\",\n"
    ghpg += "fontValueStyle: 'italic',\n"
    ghpg += "fontNumbersSize: 20,\n"
    ghpg += "fontNumbersStyle: 'italic',\n"
    ghpg += "fontNumbersWeight: 'bold',\n"
    ghpg += "fontTitleSize: 24,\n"
    ghpg += "fontUnitsSize: 22,\n"
    ghpg += "fontValueSize: 50,\n"
    ghpg += "animatedValue: true\n,"
    ghpg += "});\n"
    ghpg += "gaugePScpm.draw();\n"
    ghpg += "gaugePScpm.value = \"{0}\";\n".format(value)
    ghpg += "gaugePScpm.title = \"{0}\";\n".format(title)
    ghpg += "</script>\n"
    return ghpg
def gaugeTempScrpt(id,value,title,unit):
    ghpg = "\n\n<canvas id=\"gauge-ps{0}\"></canvas>\n".format(id)
    ghpg += "<script>\n"
    ghpg += "var gaugePStemp = new RadialGauge({\n"
    ghpg += "renderTo: 'gauge-ps{0}',\n".format(id)
    ghpg += "width: 200,\n"
    ghpg += "height: 200,\n"
    ghpg += "units: '{0}',\n".format(unit);
    ghpg += "minValue: -10,\n"
    ghpg += "maxValue: 120,\n"
    ghpg += "majorTicks: [\n"
    ghpg += "'-10',\n"
    ghpg += "'30',\n"
    ghpg += "'50',\n"
    #ghpg += "'70',\n"
    ghpg += "'90',\n"
    ghpg += "'120'\n"
    #ghpg += "'600',\n"
    #ghpg += "'700',\n"
    #ghpg += "'800',\n"
    #ghpg += "'900',\n"
    #ghpg += "'1000'\n"
    ghpg += "],\n"
    ghpg += "minorTicks: 2,\n"
    ghpg += "ticksAngle: 270,\n"
    ghpg += "startAngle: 45,\n"
    ghpg += "strokeTicks: true,\n"
    ghpg += "highlights  : [\n"
    ghpg += "{ from : -10,  to : 30, color : 'blue' },\n"#rgba(78,   78, 76, 0.5)
    ghpg += "{ from : 30,  to : 50, color : 'ghostwhite' },\n"#rgba(78,   78, 76, 0.5)
    ghpg += "{ from : 50, to : 80, color : 'green' },\n"#rgba(225, 7, 23, 0.75)
    ghpg += "{ from : 80, to : 120, color : 'rgba(225, 7, 23, 0.75)' }\n"#rgba(225, 7, 23, 0.75)
    ghpg += "],\n"
    ghpg += "valueInt: 1,\n"
    ghpg += "valueDec: 0,\n"
    ghpg += "colorPlate: \"#fff\",\n"
    ghpg += "colorMajorTicks: \"#686868\",\n"
    ghpg += "colorMinorTicks: \"#686868\",\n"
    ghpg += "colorTitle: \"#000\",\n"
    ghpg += "colorUnits: \"#000\",\n"
    ghpg += "colorNumbers: \"#686868\",\n"
    ghpg += "valueBox: true,\n"
    ghpg += "colorValueText: \"#000\",\n"
    ghpg += "colorValueBoxRect: \"#fff\",\n"
    ghpg += "colorValueBoxRectEnd: \"#fff\",\n"
    ghpg += "colorValueBoxBackground: \"#fff\",\n"
    ghpg += "colorValueBoxShadow: false,\n"
    ghpg += "colorValueTextShadow: false,\n"
    ghpg += "colorNeedleShadowUp: true,\n"
    ghpg += "colorNeedleShadowDown: false,\n"
    ghpg += "colorNeedle: \"rgba(200, 50, 50, .75)\",\n"
    ghpg += "colorNeedleEnd: \"rgba(200, 50, 50, .75)\",\n"
    ghpg += "colorNeedleCircleOuter: \"rgba(200, 200, 200, 1)\",\n"
    ghpg += "colorNeedleCircleOuterEnd: \"rgba(200, 200, 200, 1)\",\n"
    ghpg += "borderShadowWidth: 0,\n"
    ghpg += "borders: true,\n"
    ghpg += "borderInnerWidth: 0,\n"
    ghpg += "borderMiddleWidth: 0,\n"
    ghpg += "borderOuterWidth: 5,\n"
    ghpg += "colorBorderOuter: \"#fafafa\",\n"
    ghpg += "colorBorderOuterEnd: \"#cdcdcd\",\n"
    ghpg += "needleType: \"arrow\",\n"
    ghpg += "needleWidth: 2,\n"
    ghpg += "needleCircleSize: 7,\n"
    ghpg += "needleCircleOuter: true,\n"
    ghpg += "needleCircleInner: false,\n"
    ghpg += "animationDuration: 2000,\n"
    ghpg += "animationRule: \"dequint\",\n"
    ghpg += "fontNumbers: \"Verdana\",\n"
    ghpg += "fontTitle: \"Verdana\",\n"
    ghpg += "fontUnits: \"Verdana\",\n"
    ghpg += "fontValue: \"Led\",\n"
    ghpg += "fontValueStyle: 'italic',\n"
    ghpg += "fontNumbersSize: 20,\n"
    ghpg += "fontNumbersStyle: 'italic',\n"
    ghpg += "fontNumbersWeight: 'bold',\n"
    ghpg += "fontTitleSize: 24,\n"
    ghpg += "fontUnitsSize: 22,\n"
    ghpg += "fontValueSize: 50,\n"
    ghpg += "animatedValue: true\n,"
    ghpg += "});\n"
    ghpg += "gaugePStemp.draw();\n"
    ghpg += "gaugePStemp.value = \"{0}\";\n".format(value)
    ghpg += "gaugePStemp.title = \"{0}\";\n".format(title)
    ghpg += "</script>\n"
    return ghpg
    
#gaugeType="linear"
def cpmGauge(curCPM, peak):
    ghpg = "\n<canvas data-type=\"{0}-gauge\"\n".format(gaugeType)
    ghpg += "data-width=\"200\"\n"
    ghpg += "data-height=\"200\"\n"
    ghpg += "data-units=\"CPM\"\n"
    ghpg += "data-title=\"Peak {0}\"\n".format(peak)
    ghpg += "data-value=\"{0}\"\n".format(curCPM)
    ghpg += "data-min-value=\"0\"\n"
    ghpg += "data-max-value=\"220\"\n"
    ghpg += "data-major-ticks=\"0,50,100,1000,2000\"\n"
 #   ghpg += "data-major-ticks=\"0,20,40,60,80,100,120,140,160,180,200,220\"\n"
    ghpg += "data-minor-ticks=\"2\"\n"
    ghpg += "ata-stroke-ticks=\"false\"\n"
    ghpg += "data-highlights='[\n"
    ghpg += "{ \"from\": 0, \"to\": 50, \"color\": \"green\" },\n"
    ghpg += "{ \"from\": 50, \"to\": 100, \"color\": \"yellow\" },\n"
    ghpg += "{ \"from\": 100, \"to\": 150, \"color\": \"red\" }\n"
    #ghpg += "{ \"from\": 1000, \"to\": 2000, \"color\": \"maroon\" }\n"
    #ghpg += "{ \"from\": 100, \"to\": 120, \"color\": \"maroon\" }\n"
    ghpg +="]'\n"
    ghpg += "data-color-plate=\"#222\"\n"
    ghpg += "data-color-major-ticks=\"#f5f5f5\"\n"
    ghpg += "data-color-minor-ticks=\"#ddd\"\n"
    ghpg += "data-color-title=\"#fff\"\n"
    ghpg += "data-color-units=\"#ccc\"\n"
    ghpg += "data-color-numbers=\"#eee\"\n"
    ghpg += "data-color-needle-start=\"rgba(240, 128, 128, 1)\"\n"
    ghpg += "data-color-needle-end=\"rgba(255, 160, 122, .9)\"\n"
    ghpg += "data-value-box=\"true\"\n"
    ghpg += "data-animation-rule=\"bounce\"\n"
    ghpg += "data-animation-duration=\"500\"\n"
    ghpg += "data-font-value=\"Led\"\n"
    ghpg += "data-animated-value=\"true\"\n"
    ghpg += "></canvas>"
    return ghpg
def tempGauge(curTemp, title):
    ghpg = "\n<canvas data-type=\"{0}-gauge\"\n".format(gaugeType)
    ghpg += "data-width=\"200\"\n"
    ghpg += "data-height=\"200\"\n"
    ghpg += "data-units=\"Temp\"\n"
    ghpg += "data-title=\"{0}f\"\n".format(curTemp)
    ghpg += "data-value=\"{0}\"\n".format(curTemp)
    ghpg += "data-min-value=\"-10\"\n"
    ghpg += "data-max-value=\"120\"\n"
    ghpg += "data-major-ticks=\"-10,0,50,75,100,120\"\n"
    ghpg += "data-minor-ticks=\"2\"\n"
    ghpg += "ata-stroke-ticks=\"false\"\n"
    ghpg += "data-highlights='[\n"
    ghpg += "{ \"from\": -10, \"to\": 0, \"color\": \"white\" },\n"
    ghpg += "{ \"from\": 0, \"to\": 30, \"color\": \"lightgray\" },\n"
    ghpg += "{ \"from\": 30, \"to\": 65, \"color\": \"slateblue\" },\n"
    ghpg += "{ \"from\": 65, \"to\": 85, \"color\": \"blue\" },\n"
    ghpg += "{ \"from\": 85, \"to\": 120, \"color\": \"red\" }\n"
    ghpg +="]'\n"
    ghpg += "data-color-plate=\"#222\"\n"
    ghpg += "data-color-major-ticks=\"#f5f5f5\"\n"
    ghpg += "data-color-minor-ticks=\"#ddd\"\n"
    ghpg += "data-color-title=\"#fff\"\n"
    ghpg += "data-color-units=\"#ccc\"\n"
    ghpg += "data-color-numbers=\"#eee\"\n"
    ghpg += "data-color-needle-start=\"rgba(240, 128, 128, 1)\"\n"
    ghpg += "data-color-needle-end=\"rgba(255, 160, 122, .9)\"\n"
    ghpg += "data-value-box=\"true\"\n"
    ghpg += "data-animation-rule=\"bounce\"\n"
    ghpg += "data-animation-duration=\"500\"\n"
    ghpg += "data-font-value=\"Led\"\n"
    ghpg += "data-animated-value=\"true\"\n"
    ghpg += "></canvas>"
    return ghpg

def getWebPage(tval,cval,curCPM,peak):
    hpg = "<html><head><meta http-equiv=\"refresh\" content=\"30\"><meta http-equiv=\"Cache-Control\" content=\"no-store\" />"
    hpg += "<meta charset=\"UTF-8\"/><title>{0}</title>".format(pageBanner)
    hpg += "<style>._PR {font-size:large;box-shadow: 3px 4px 5px #888888;color:#333;border-top-left-radius: 8px;border-top-right-radius: 8px;border-bottom-right-radius: 8px;border-bottom-left-radius: 8px;border-width:1px;border-style: solid;border-color:silver;text-align: left;margin:4px 4px 4px 4px;padding:4px 4px 4px 4px;}</style>"
    hpg += "<script src=\"gauge.min.js\"></script>"
    hpg += "</head><body style=\"background-color:silver;align-content:center\">{0}".format(pageBanner)
    hpg += "<div style=\"width:96%;float:left;background-color:gray;align-content:center\" class=\"_PR\">"
    hpg += "<div class=\"_PR\" style=\"width:45%;float:left;background-color:#000000;color:#37bc2d\">Temp:<br><TMP></div>"
    hpg += "<div class=\"_PR\" style=\"width:45%;float:left;background-color:#000000;color:#37bc2d\"><CPM></div>"
    #hpg += cpmGauge(curCPM,peak)
    hpg += "<div style=\"width:100%;float:left\"><a href=QCPMgauge.html class=\"_PR\" style=\"text-decoration:none;text-align:center;width:96%;background-color:silver;color:#333;float:left;border-radius:20;padding:4px\"\">Gauge</a></div>"
    hpg += "</div>"
    hpg += "</div></body></html>"
    #hpg += "</div></div></body></html>"
    return parsepage(tval,cval,hpg)
def getGaugePage(tval,cval,curCPM,peak,curF,curC):
    hpg = "<html><head><meta http-equiv=\"refresh\" content=\"30\"><meta http-equiv=\"Cache-Control\" content=\"no-store\" />"
    hpg += "<meta charset=\"UTF-8\"/><title>QuickCPM</title>"
    hpg += "<style>._PR {font-size:large;box-shadow: 3px 4px 5px #888888;color:#333;border-top-left-radius: 8px;border-top-right-radius: 8px;border-bottom-right-radius: 8px;border-bottom-left-radius: 8px;border-width:1px;border-style: solid;border-color:silver;text-align: left;margin:4px 4px 4px 4px;padding:4px 4px 4px 4px;}</style>"
    hpg += "<script src=\"gauge.min.js\"></script>"
    hpg += "</head><body style=\"background-color:silver;align-content:center\">"
    hpg += "<div style\"width:100%;font-family:Verdana\">{0}</div>".format(pageBanner)
    hpg += "<div style=\"float:left;background-color:gray;align-content:center;padding:10px\" class=\"_PR\">"
    
    #static html page
    #hpg += cpmGauge(curCPM,peak) 
    #hpg += tempGauge(curTemp,"Temp");
    
    #scripted html page
    hpg += gaugeCPMScrpt("cpm",curCPM,"CPM","Peak CPM {0}".format(peak)) #id,value,title,unit
    hpg += gaugeTempScrpt("tmp",curF,"Temp","{0}c".format(curC)) #id,value,title,unit
    hpg += "<div style=\"width:100%;float:left\"><a href=QCPMbar.html class=\"_PR\" style=\"text-decoration:none;text-align:center;width:96%;background-color:silver;color:#333;float:left;border-radius:20;padding:4px\">Bar</a></div>"
    hpg += "</div>"
    hpg += "<div></body></html>"
    return parsepage(tval,cval,hpg)
def parsepage(tval,cval,pval) :
    return (pval.replace("<TMP>",tval).replace("<CPM>",cval))

def getCPM(gmc): 
    gmc.write(b'<GETCPM>>')
    dat = gmc.read(2)
    try:
        gv= ord(dat[0])<< 8 | ord(dat[1])
    except IndexError:
        gv= ord("\x00")
    return gv

def writeToFile(fileName,data, isbinary, ishtml):
        if len(data)>1:
            fn= fileName # QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.*")with open("test.txt", "a") as myfile:
            if isbinary:
                print "Writing binary"
                with open(fn, "wb") as file:  
                    file.write(data)  
                print "{:d} bytes saved to {:s}".format(len(data), fn)
            else:
                if ishtml:
                    with open(fn, "w") as file:  
                        file.write(data)
                        print "{:d} chars written to {:s}".format(len(data),fn)
                else:
                    with open(fn, "a") as file:  
                        file.write(data)
                        print "{:d} chars written to {:s}".format(len(data),fn)
                    
        else:
            print "No data to save"

        
def gmcCommand(gmc, cmd, returnlength, byteformat = True):
    try: #send command
        gmc.write(cmd)
    except:        
        print ("\nSend Error")#, sys.exc_info()
        gmc.close()
        sys.exit(1)
    try: #read data
        rtn = gmc.read(returnlength)
    except:
        print ("\nReceive ERROR")#, sys.exc_info()
        gmc.close()
        sys.exit(1)
    if byteformat: rtn = map(ord,rtn) # convert string to list of int
    return rtn

def getClock():
    clockval="<SETDATETIME[YYMMDDHHMMSS]>>"#set gmc clock cmd
    datenow = "{:%m/%d/%Y %H:%M:%S}".format(datetime.datetime.now())
    return datenow
def getFName(tagStr):
    fName = "logs/{:s}{:%Y%m%d}_{:s}.csv".format("gmc_",datetime.datetime.now(),tagStr)
    return fName
def tFile():
    fName = "logs/{:s}{:%Y%m%d}_temp.csv".format("gmc_",datetime.datetime.now())
    return fName
def getTEMP(gmc): 
    gmc.write(b'<GETTEMP>>')
    dat = gmc.read(4)
    try:
        i = ord(dat[0])# ord(dat[0])<< 8 | ord(dat[1])
        d = ord(dat[1])
        tCelcius = "{0}.{1}".format(i,d)
        tFarenheit=float(tCelcius)*1.4+32
        gv="{0},{1}".format(tCelcius,tFarenheit)
    except IndexError:
        gv  =ord("0")
    return gv

cl = getClock()
if len(sys.argv) > 1:
        print "Interval:{0} sec".format(sys.argv[1])# sys.argv[1:] = ["-h"]
        try:
            slp=float(sys.argv[1])
        except:
            print "Usage: python gmccpm.py 10 (for 10 sec interval)\nTimer argument [1] must be an integer"
            sys.exit(1)
try:
    while True:
        cl = getClock()
        currentCPM=getCPM(gmc)
        cpm = "{0},{1}\n".format(cl,currentCPM)
        if currentCPM > peak:
            peak=currentCPM
        print "{0} {1} (Peak:{2})".format(cl,currentCPM,peak)
        tmp = "{0}".format(getTEMP(gmc))
        tCel =tmp.split(',')[0]
        tF = tmp.split(',')[1]
        tCSV="{0},{1},{2}\n".format(cl,tF,tCel)
        tempDsply ="{0}c - {1}f".format(tCel,tF)
        tempH = "{:s}<table style=\"width:98%;bgcolor:white;height:14px;box-shadow:none;\">".format(tempDsply)
        tempH += "<td style=\"background-color:maroon;width:{0}%;border-top-left-radius: 8px;border-bottom-left-radius: 8px;padding:1px;margin-left:-8px;font-size:large;color:white;text-align:center\"><b>{0}f </b></td>".format(tmp.split(',')[1])
        tempH += "<td style=\"background-color:#eaeaea;padding:1px;border-top-right-radius: 8px;border-bottom-right-radius: 8px\"></td></table><br>"
        pkH = "<table style=\"width:98%;bgcolor:white;height:14px;box-shadow:none;\">"
        pkH += "<td style=\"background-color:darkblue;width:{0}%;border-top-left-radius: 8px;border-bottom-left-radius: 8px;padding:1px;margin-left:-8px;font-size:small;color:white;text-align:center\"><b>{0} CPM </b></td>".format(peak)
        pkH += "<td style=\"background-color:#eaeaea;padding:1px;border-top-right-radius: 8px;border-bottom-right-radius: 8px\"></td></table>"
        print tempDsply
        cpmH = "{0}<br>Peak: {1}".format(cpm.replace(' ','-').replace(',',"<br>CPM: "),peak)
        cpmH += pkH
        writeToFile(getFName("cpm"),cpm,0,0)
        writeToFile(getFName("temp"),tCSV,0,0)
        writeToFile("QCPMbar.html",getWebPage(tempH,cpmH,currentCPM,peak),0,1)
        writeToFile("QCPMgauge.html",getGaugePage(tempH,cpmH,currentCPM,peak,tF,tCel),0,1)
        if (ftpLp == 0):
            ftpQCPM()
        if (ftpLp >= ftpLimit):
            ftpLp=1
            ftpQCPM()
        ftpLp += 1
        time.sleep(slp) 
except KeyboardInterrupt:
    pass
