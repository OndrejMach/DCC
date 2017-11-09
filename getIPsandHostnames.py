import os
from os import walk
import re
import subprocess
import smtplib
from email.mime.text import MIMEText


mzUser = "mzadmin"
mzPass = "dr"
dir = "d:/tmp/dcc/"
tempDir = "/tmp/DCCWFExporter/"
wflist = []

#test="CO_COM.SFTP_COLLECTION_DELETE.DE_Coll_ACC_ZACC1 (124)"

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
                if wfname not in wflist
                    wflist.append(wfname)

retval = p.wait()

p=subprocess.Popen("rm -rf "+tempDir,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

p=subprocess.Popen("mkdir "+tempDir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()




for wf in wflist:
    print mzCommandWfExport + wf +" " +tempDir+wf+".csv"
    #p = subprocess.Popen(mzCommandWfExport + wf +" " +tempDir+wf+".csv")
    #retval = p.wait()
    os.system(mzCommandWfExport + wf +" " +tempDir+wf+".csv")
files = []


for (dirpath, dirnames, filenames) in walk(tempDir):
    files.extend(filenames)
    break

result = dict()

for file in files:
    fh = open(tempDir + file, "r")
    result[file] = list();
    content = fh.readlines()
    for line in content:
        #print(line)
        mIP = re.search(r'"(\d+\.\d+\.\d+\.\d+)"',line)
        mHostname = re.search(r'"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}"',line)
        if (mIP is not None):
            #print(file + "\n")
            ip = mIP.group()[1:-1]
            if ip not in result[file]:
                result[file].append(ip)
            #print(mIP.group())
        #else:
        if (mHostname is not None):
            hn = mHostname.group()[1:-1]
            if hn not in result[file]:
                result[file].append(hn)

message = ""
for key in result:
    message = message + key + " :: ".join(result[key], ",")+"\n"
    #result[key] =

print(message)


msg = MIMEText(message)

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'environment IPs' # textfile
msg['From'] = 'ondrej.machacek@t-mobile.cz'
msg['To'] = 'ondrej.machacek@t-mobile.cz'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
