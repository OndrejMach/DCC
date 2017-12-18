import os
import sys
from os import walk
import re
import subprocess
#import smtplib
#from email.mime.text import MIMEText
import socket
#import cx_Oracle

#mzrepIN5/xg4kdu61@10.99.226.14:51521/tMZTUA1
dbuser = "mzrepIN5"
dbpass = "xg4kdu61"
dbIP = "10.99.226.14"
dbPort = "51521"
dbSID = "tMZTUA1"
dbRepUser = "mzrepIN5"

if len(sys.argv) < 6:
    #print("help: python getIPsAndStructures.py <mzadmin> <mzadmin_pass> <db_user> <db_pass> <db_IP> <db_port> <db_SID> <db_mzrep_user>")
    print("help: python getIPsAndStructures.py <mzadmin> <mzadmin_pass> <db_user> <db_pass> <SID> <db_mzrep_user>")
    exit(1)


mzUser = sys.argv[1].strip()#"mzadmin"
mzPass = sys.argv[2].strip() #"dr"
dbuser = sys.argv[3].strip()#"mzrepIN5"
dbpass = sys.argv[4].strip()#"xg4kdu61"
#dbIP = sys.argv[5].strip()#"10.99.226.14"
#dbPort = int(sys.argv[6].strip())#"51521"
dbSID = sys.argv[5].strip()#"tMZTUA1"
dbRepUser = sys.argv[6].strip()#"mzrepIN5"


dir = "d:/tmp/dcc/"
tempDir = "/tmp/DataWFExporter"+dbuser+"/"
#wflist = []

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
        #print(i)
        if (line.find("-----BEGIN") > -1 and line.find("PRIVATE KEY-----") > -1):
            linePrev = linePrev + line[:-1]
            while not (line.find("-----END") > -1 and line.find("PRIVATE KEY-----")):
                i=i+1
                line = fileContent[i]
        if (line.find(',')>-1):
            split = (linePrev+line).split(",") if (len(linePrev)>1) else line.split(",")
            linePrev=""
            #print("delka pole "+str(len(split)))
            #print(filename)
            item = dict()
            item["filename"] = filename
            item["name"] = split[name][1:-1] if (name > -1) else "N/A"
            item["host"] = resolve(split[host][1:-1]) if (host > -1) else "N/A"
            item["username"] = split[username][1:-1] if (username > -1) else "N/A"
            #print("###### " + str(directory) + " " + str(len(split)) + " " + "".join(split))
            #print("LINE ---------" + split[directory] + "------------------------")
            item["directory"] = split[directory][1:-1] if (directory > -1) else "N/A"
            item["port"] = split[port] if (port > -1) else "N/A"
            ret.append(item)

        i = i + 1
    return ret

def cutWf(wfname):
    mwf2 = re.search(r'(\w+\.\w+)\..*', wfname)
    if mwf2 is not None:
        return mwf2.group(1)
    return None

    #mzrepIN5/xg4kdu61@10.99.226.14:51521/tMZTUA1
    #CORE.SFTP_FORWARD_KEY.DE_Forw_CMD_RAW_10_102_133_7_MSS12
def processQueryRes(result):
    ret = []
    for r in result:
        res = cutWf(str(r))
        if res not in ret:
            ret.append(res)
    return ret

#def getWfsfromDB(userdb,passworddb, sid, ip, port, mzrepuser):
#     retlist = []
#     connString = userdb+'/'+passworddb+'@'+str(ip)+':'+str(port)+'/'+sid
#
#     #dsn_tns = cx_Oracle.makedsn('10.99.226.14', 51521, 'tMZTUA1')
#     #con = cx_Oracle.connect(user='mzrepIN5', password='xg4kdu61', dsn=dsn_tns)
#
#     dsn_tns = cx_Oracle.makedsn(ip, port, sid)
#     con = cx_Oracle.connect(user=userdb, password=passworddb, dsn=dsn_tns)
#
#     print("trying to connec to Oracle "+connString)
#     #con = cx_Oracle.connect(connString)
#     cursor = con.cursor()
#     cursor.execute(
#         "select DISTINCT(w.WORKFLOWNAME) from "+mzrepuser+".CO_INPUTTABLE i, "+mzrepuser+".CO_WORKFLOWTABLE w where trunc(i.COLLECTIONDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = i.COLLECTIONID and w.WORKFLOWNAME not like ('%DISK%')")
#     print("fetchall:")
#     retlist.extend(processQueryRes(cursor.fetchall()))
#     cursor.execute(
#         "select DISTINCT(w.WORKFLOWNAME) from "+mzrepuser+".CO_FORWARDINGTABLE f, "+mzrepuser+".CO_WORKFLOWTABLE w where trunc(f.FORWARDINGDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = f.FORWARDINGID and w.WORKFLOWNAME not like ('%DISK%')")
#     retlist.extend(processQueryRes(cursor.fetchall()))
#
#     cursor.close()
#
#     con.close()
#     print(retlist)
#     return retlist


def getWfsfromSQLPLus(userdb,passworddb,mzrepuser,sid):
    ret= []
    sqlstmt = r'"SET HEADING OFF\n'
    sqlstmt = sqlstmt +"select DISTINCT(w.WORKFLOWNAME) from " + mzrepuser + ".CO_INPUTTABLE i, " + mzrepuser + ".CO_WORKFLOWTABLE w where trunc(i.COLLECTIONDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = i.COLLECTIONID and w.WORKFLOWNAME not like ('%DISK%');"
    sqlstmt = sqlstmt+ r"\n"
    sqlstmt = sqlstmt+ "select DISTINCT(w.WORKFLOWNAME) from "+mzrepuser+".CO_FORWARDINGTABLE f, "+mzrepuser+".CO_WORKFLOWTABLE w where trunc(f.FORWARDINGDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = f.FORWARDINGID and w.WORKFLOWNAME not like ('%DISK%');"
    sqlstmt = sqlstmt+'"'
    sqlpluscommand = "echo -e "+sqlstmt +"|sqlplus -s "+userdb+"/"+passworddb+"@"+sid
    #print(sqlpluscommand)
    p = subprocess.Popen(sqlpluscommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        wf = line.decode("utf-8",'backslashreplace')
        if len(wf) >0:
            wfname = cutWf(wf)
            if wfname is not None and wfname not in ret:
                ret.append(wfname)
    return ret


#mzCommand = "mzsh "+mzUser+"/"+mzPass+" wflist"

mzCommandWfExport = "mzsh "+mzUser+"/"+mzPass+" wfexport "

#p = subprocess.Popen(mzCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    wf = line.decode("utf-8",'backslashreplace')
#    mWf = re.search(r'^(?=.*COLL.*)|(?=.*FORW.*)', wf.upper())
#    if (mWf is not None):
#        #print("go1")
#        mwf3 = re.search(r'.*DISK.*', wf.upper())
#        if mwf3 is None:
#            mwf2 = re.search(r'(\S+)\.(\S+).*', wf)
#            if mwf2 is not None:
#                 wfname = mwf2.group(1)
#                 if wfname not in wflist:
#                    wflist.append(wfname)

#retval = p.wait()


#wflist = getWfsfromDB(dbuser,dbpass, dbSID,dbIP,dbPort,dbRepUser)
wflist = getWfsfromSQLPLus(dbuser,dbpass,dbRepUser, dbSID)

#print(wflist)

p=subprocess.Popen("rm -rf "+tempDir,shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
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

fileOut = open("/tmp/"+dbuser+"IPs.csv", "w")
fileOut.write("wfname,name,host,username,port,directory\n")

for file in files:
    fh = open(tempDir + file, "r")
    result[file] = list;
    content = fh.readlines()
    structure = getIPs(content,file)
    fileOut.write(getCSVLine(structure))

fileOut.close()

os.system('echo "see attachement"|mailx -s "environment IPs" -a /tmp/'+dbuser+'IPs.csv ondrej.machacek@t-mobile.cz')