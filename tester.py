import socket
import datetime

now = datetime.datetime.now()

def padString(num):
    return str(num) if num>9 else ("0"+str(num))

def getDateStamp():
    now = datetime.datetime.now()
    return padString(now.month)+padString(now.day)+padString(now.hour)

print(getDateStamp())




# def resolve(fqdn):
#     ip = "IP N/A for "
#     try:
#         ip = socket.gethostbyname(fqdn)
#     except:
#         ip = ip + fqdn
#     return ip
#
# def getIPs(fileContent, filename):
#     ret = list()
#     name = -1 #Name
#     host = -1 #Host, Host Name
#     username = -1 #Username
#     directory = -1 #Directory
#     port = -1 #Port
#     line = fileContent.pop(0)
#     it = 0;
#     for i in line.split(","):
#         if (i.find('"Name"')>-1):
#             name = it
#         if (i.find(']Host')>-1):
#             host = it
#         if (i.find(']Username')>-1):
#             username = it
#         if (i.find('[Collection]Remote Directory')>-1 or i.find('[Target]Directory')>-1 or i.find('[Collection]Directory')>-1):
#             #print(i)
#             directory = it
#         if (i.find(']Port')>-1):
#             port = it
#         it=it+1
#
#     #print(filename + " " +str(name)+ " "+ str(host)+" "+str(username)+" "+str(directory)+" " + str(port))
#     i=0
#     linePrev=""
#     while i < len(fileContent):
#         line = fileContent[i]
#         #print(i)
#         if (line.find("-----BEGIN") > -1 and line.find("PRIVATE KEY-----") > -1):
#             linePrev = linePrev + line[:-1]
#             while not (line.find("-----END") > -1 and line.find("PRIVATE KEY-----")):
#                 i=i+1
#                 line = fileContent[i]
#         if (line.find(',')>-1):
#             split = (linePrev+line).split(",") if (len(linePrev)>1) else line.split(",")
#             linePrev=""
#             #print("delka pole "+str(len(split)))
#             #print(filename)
#             item = dict()
#             item["filename"] = filename
#             item["name"] = split[name][1:-1] if (name > -1) else "N/A"
#             item["host"] = resolve(split[host][1:-1]) if (host > -1) else "N/A"
#             item["username"] = split[username][1:-1] if (username > -1) else "N/A"
#             #print("###### " + str(directory) + " " + str(len(split)) + " " + "".join(split))
#             #print("LINE ---------" + split[directory] + "------------------------")
#             item["directory"] = split[directory][1:-1] if (directory > -1) else "N/A"
#             item["port"] = split[port] if (port > -1) else "N/A"
#             ret.append(item)
#
#         i = i + 1
#     return ret
#
#
# fh = open("/home/ondrej/Downloads/CORE.SFTP_FORWARD_KEY.csv", "r")
# #result[file] = list;
# content = fh.readlines()
# structure = getIPs(content,"test")
# print(structure)