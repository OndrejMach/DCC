from os import walk
import re
import subprocess

mzUser = "mzadmin"
mzPass = "dr"
dir = "d:/tmp/dcc/"
tempDir = "/tmp/DCCWFExporter/"
wflist = []

mzCommand = "mzsh "+mzUser+"/"+mzPass+" wflist"

mzCommandWfExport = "mzsh "+mzUser+"/"+mzPass+" wfexport "

p = subprocess.Popen(mzCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    wf = line.decode("utf-8",'backslashreplace')
    mWf = re.search(r'^(?=.*COLL)(?=.*FORW)(?!.*DISK).*',wf.upper())
    if (mWf is not None):
        wflist.append(wf)
    #print (line.decode("utf-8",'backslashreplace'))
retval = p.wait()

p=subprocess.Popen("rm -rf "+tempDir,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()

p=subprocess.Popen("mkdir "+tempDir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()


for wf in wflist:
    p = subprocess.Popen(mzCommandWfExport + wf +" " +tempDir+wf+".csv")
    retval = p.wait()
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

for key in result:
    #result[key] =
    print(result[key])


