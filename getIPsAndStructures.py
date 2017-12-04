import os
import sys
from os import walk
import re
import subprocess
#import smtplib
#from email.mime.text import MIMEText
import socket


mzUser = sys.argv[1]#"mzadmin"
mzPass = sys.argv[2] #"dr"
dir = "d:/tmp/dcc/"
tempDir = "/tmp/DataWFExporter/"
wflist = []

def resolve(fqdn):
    ip = "IP N/A for "
    try:
        ip = socket.gethostbyname(fqdn)
    except:
        ip = ip + fqdn
    return ip

def getCSVLine(struct):
    ret = ""
    for item in struct:
        ret = ret+item["filename"]+','+item["name"]+','+item["host"]+','+item["username"]+','+item["port"]+','+item["directory"]+"\n"
    return ret

def getIPs(fileContent, filename):
    ret = list()
    name = -1 #Name
    host = -1 #Host, Host Name
    username = -1 #Username
    directory = -1 #Directory
    port = -1 #Port
    line = fileContent.pop(0)
    it = 0;
    for i in line.split(","):
        if (i.find('"Name"')>-1):
            name = it
        if (i.find(']Host')>-1):
            host = it
        if (i.find(']Username')>-1):
            username = it
        if (i.find('[Collection]Remote Directory')>-1 or i.find('[Target]Directory')>-1 or i.find('[Collection]Directory')>-1):
            #print(i)
            directory = it
        if (i.find(']Port')>-1):
            port = it
        it=it+1

    #print(filename + " " +str(name)+ " "+ str(host)+" "+str(username)+" "+str(directory)+" " + str(port))
    i=0
    linePrev=""
    while i < len(fileContent):
        line = fileContent[i]
        if line.find("-----BEGIN")>-1 and line.find("PRIVATE KEY-----")>-1:
            linePrev = line[:-1]
            #print(linePrev)
        else :
            if (line.find(",")>-1):
                split = (linePrev+line).split(",") if (len(linePrev)>1) else line.split(",")
                linePrev=""
                #print("delka pole "+str(len(split)))

                item = dict()
                item["filename"] = filename
                item["name"] = split[name][1:-1] if (name > -1) else "N/A"
                item["host"] = resolve(split[host][1:-1]) if (host > -1) else "N/A"
                item["username"] = split[username][1:-1] if (username > -1) else "N/A"
                #print("###### "+str(directory)+" "+str(len(split))+" "+"".join(split))
                item["directory"] = split[directory][1:-1] if (directory > -1) else "N/A"
                item["port"] = split[port][1:-1] if (port > -1) else "N/A"
                ret.append(item)
        i = i + 1
    return ret


mzCommand = "mzsh "+mzUser+"/"+mzPass+" wflist"

mzCommandWfExport = "mzsh "+mzUser+"/"+mzPass+" wfexport "

p = subprocess.Popen(mzCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    wf = line.decode("utf-8",'backslashreplace')
    mWf = re.search(r'^(?=.*COLL.*)|(?=.*FORW.*)', wf.upper())
    if (mWf is not None):
        #print("go1")
        mwf3 = re.search(r'.*DISK.*', wf.upper())
        if mwf3 is None:
            mwf2 = re.search(r'(\S+)\.(\S+).*', wf)
            if mwf2 is not None:
                 wfname = mwf2.group(1)
                 if wfname not in wflist:
                    wflist.append(wfname)

retval = p.wait()

p=subprocess.Popen("rm -rf "+tempDir,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

p=subprocess.Popen("mkdir "+tempDir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()




for wf in wflist:
    #print mzCommandWfExport + wf +" " +tempDir+wf+".csv"
    #p = subprocess.Popen(mzCommandWfExport + wf +" " +tempDir+wf+".csv")
    #retval = p.wait()
    os.system(mzCommandWfExport + wf +" " +tempDir+wf+".csv")
files = []

for (dirpath, dirnames, filenames) in walk(tempDir):
    files.extend(filenames)
    break


result = dict()

fileOut = open("/tmp/IPs.csv", "w")
fileOut.write("wfname,name,host,username,port,directory\n")

for file in files:
    fh = open(tempDir + file, "r")
    result[file] = list;
    content = fh.readlines()
    structure = getIPs(content,file)
    fileOut.write(getCSVLine(structure))

fileOut.close()

os.system('echo "see attachement"|mailx -s "environment IPs" -a /tmp/IPs.csv ondrej.machacek@t-mobile.cz')