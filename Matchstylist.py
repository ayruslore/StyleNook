from gevent import monkey; monkey.patch_all()
from bottle import route, run, response
import bottle
import csv
import sys
import json

class EnableCors(object):
    name = 'enable_cors'
    api = 2
    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

ifile2 = open('userprofiles.csv', "r")
ifile1 = open('returncountsepe.csv', "r")
reader1 = csv.reader(ifile1)
reader2 = csv.reader(ifile2)
rownum=0
userdict={}
stylistdict={}
orders=[]
stylist=[]
user=[]
success=[]
returns_nms=[]
returns_simi=[]
style=0
header=[];
for row in reader1:
    if (rownum==0):
        header=row
    else:
        orders.append(row[2]);
        stylist.append(row[1]);
        user.append(row[0]);
        returns_nms.append(int(row[4]));
        returns_simi.append(int(row[5]))
        success.append(int(row[6]));
    rownum+=1

for row in reader2:
    userdict[row[1]]=[]
    for i in range(10,19):
        if ((row[i].strip()=="Love this collection!") or (row[i].strip()=="Love it!")):
            userdict[row[1]].append(2);
        elif (row[i].strip()=="Quite like this range"):
            userdict[row[1]].append(1);
        elif ((row[i].strip()=="Umm OK") or (row[i].strip()=="It's OK.")):
            userdict[row[1]].append(-1);
        elif ((row[i].strip()=="Hate this collection!")):
            userdict[row[1]].append(-2);
        else:
            userdict[row[1]].append(0);

for s in stylist:
    stylistdict[s]=[[0,0,0,0,0,0,0,0,0],0];
ifile1.close();
ifile2.close();


app = bottle.app()

@app.route('/matchsylist/<num>')
def matchsylist(num):
    rownum=0
    style=0
    for o in orders:
        style+=1
        if user[rownum] not in userdict.keys():
            style+=1
            rownum+=1
            continue;
        else:
            for i in range(0,9):
                stylistdict[stylist[rownum]][0][i]=float(stylistdict[stylist[rownum]][0][i])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(userdict[user[rownum]][i]))
            stylistdict[stylist[rownum]][1]+=1
        rownum+=1;
    calc=0
    for s in stylistdict:
        if (stylistdict[s][1]!=0):
            for i in range(0,9):
                stylistdict[s][0][i]=float(stylistdict[s][0][i])/stylistdict[s][1]
        calc+=stylistdict[s][1];
    find=num
    mval=0;
    msty='';
    for s in stylistdict:
        val=0
        for i in range(0,9):
            val+=float(userdict[find][i])*float(stylistdict[s][0][i])
        if (val>mval):
            mval=val
            msty=s
    print("The best stylist is "+ msty)
    yield json.dumps({"stylist":msty})

app.install(EnableCors())

app.run(host='0.0.0.0', port=4000, debug=True, server='gevent')
