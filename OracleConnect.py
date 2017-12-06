import cx_Oracle
import re


def cutWf(wfname):
    mwf2 = re.search(r'(\w+\.\w+)\..*', wfname)
    if mwf2 is not None:
        return mwf2.group(1)
    return None

con = cx_Oracle.connect('mzrepIN5/xg4kdu61@10.99.226.14:51521/tMZTUA1')
print(con.version)

cursor = con.cursor()

cursor.execute("select DISTINCT(w.WORKFLOWNAME) from CO_INPUTTABLE i, CO_WORKFLOWTABLE w where trunc(i.COLLECTIONDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = i.COLLECTIONID and w.WORKFLOWNAME not like ('%DISK%')")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(cutWf(str(r)))

cursor.execute("select DISTINCT(w.WORKFLOWNAME) from CO_FORWARDINGTABLE f, CO_WORKFLOWTABLE w where trunc(f.FORWARDINGDATETIME) > trunc(sysdate-5) and w.WORKFLOWID = f.FORWARDINGID and w.WORKFLOWNAME not like ('%DISK%')")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(cutWf(str(r)))

cursor.close()

con.close()
