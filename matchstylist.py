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

global stylistnames
global userdict
global stylistdict
global orders
global stylist
global user
global returns_nms
global returns_simi
global success

userdict={}
stylistdict={}
orders=[]
stylist=[]
user=[]
returns_nms=[]
returns_simi=[]
success=[]
stylistnames = []


def Removedup(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

app = bottle.app()

@app.route('/getstylistnames')
def getstylist():
    global stylistnames
    yield json.dumps(stylistnames)

@app.route('/makestylistdata')
def makestylistdata():
    global stylistnames
    stylistnames = []
    lol = []
    with open('returncountsepe.csv','r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if(i != 0):
                if row[1] not in lol:
                    lol.append(row[1])
            i = i + 1
    with open('wp_users.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in lol:
                if row[3] != '':
                    stylistnames.append((row[0],row[3]))
                else:
                    stylistnames.append((row[0],row[4]))

@app.route('/makevariablesagain')
def makevariablesagain():
    #global userdict
    global stylistdict
    global orders
    global stylist
    global user
    global returns_nms
    global returns_simi
    global success
    ifile1 = open('returncountsepe.csv', "r")
    reader1 = csv.reader(ifile1)
    rownum=0
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
    for s in stylist:
        stylistdict[s]=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0];
    ifile1.close();

@app.route('/cleanuserprofile')
def cleanuserprofile():
    global userdict
    ifile1 = open('userprofiles.csv', "r")
    reader1 = csv.reader(ifile1)
    rownum=0
    userdict={}
    l=[]
    for row in reader1:
        if (rownum==0):
            rownum+=1;
        else:
            userdict[row[1]]=[]
            userdict[row[1]].append(row[1])
            if (row[6].strip().lower()=="never"):
                userdict[row[1]].append(1)
            elif ((row[6].strip().lower()=="sometimes") or (row[6].strip().lower()=="a little bit")):
                userdict[row[1]].append(2)
            elif (row[6].strip().lower()=="all the time!"):
                userdict[row[1]].append(3)
            else:
                userdict[row[1]].append(0)
            for i in range(10,19):
                if ((row[i].strip()=="Love this collection!") or (row[i].strip()=="Love it!")):
                    userdict[row[1]].append(4);
                elif (row[i].strip()=="Quite like this range"):
                    userdict[row[1]].append(3);
                elif ((row[i].strip()=="Umm OK") or (row[i].strip()=="It's OK.")):
                    userdict[row[1]].append(2);
                elif ((row[i].strip()=="Hate this collection!")):
                    userdict[row[1]].append(1);
                else:
                    userdict[row[1]].append(0);
            if (row[19]!='NULL'):
                userdict[row[1]].append(int(row[19])+1);
            else:
                userdict[row[1]].append(0);
            if (row[20]!='NULL'):
                userdict[row[1]].append(int(row[20])+1);
            else:
                userdict[row[1]].append(0);
            if (row[36].strip().lower()=="a"):
                userdict[row[1]].append(8);
            elif (row[36].strip().lower()=="b"):
                userdict[row[1]].append(7);
            elif (row[36].strip().lower()=="c"):
                userdict[row[1]].append(6);
            elif (row[36].strip().lower()=="d"):
                userdict[row[1]].append(5);
            elif (row[36].strip().lower()=="e"):
                userdict[row[1]].append(4);
            elif (row[36].strip().lower()=="f"):
                userdict[row[1]].append(3);
            elif (row[36].strip().lower()=="g"):
                userdict[row[1]].append(2);
            elif (row[36].strip().lower()=="g"):
                userdict[row[1]].append(1);
            else:
                userdict[row[1]].append(0);
            if (('18' in row[37]) and ('24' in row[37])):
                userdict[row[1]].append(1);
            elif (('25' in row[37]) and ('29' in row[37])):
                userdict[row[1]].append(2);
            elif (('30' in row[37]) and ('34' in row[37])):
                userdict[row[1]].append(3);
            elif (('35' in row[37]) and ('40' in row[37])):
                userdict[row[1]].append(4);
            elif (('40' in row[37]) and ('35' not in row[37])):
                userdict[row[1]].append(5);
            else:
                userdict[row[1]].append(0);
            for i in range(38,45):
                if (('upto' in row[37]) and ('750' in row[37])):
                    userdict[row[1]].append(1);
                elif (('upto' in row[37]) and ('1000' in row[37])):
                    userdict[row[1]].append(2);
                elif (('upto' in row[37]) and ('1500' in row[37])):
                    userdict[row[1]].append(3);
                elif (('upto' in row[37]) and ('2000' in row[37])):
                    userdict[row[1]].append(4);
                elif (('2000' in row[37]) and ('upto' not in row[37])):
                    userdict[row[1]].append(5);
                else:
                    userdict[row[1]].append(0);
            if (row[54]!='NULL'):
                userdict[row[1]].append(float(row[54]));
            else:
                userdict[row[1]].append(0);
            rownum+=1;
    listing={}
    counter=0;
    for j in range(2,11):
        templist=[]
        for i in userdict:
            templist.append(userdict[i][j])
        listing[counter]=templist
        counter+=1;
    res= [[0 for x in range(9)] for y in range(9)]
    for i in range(9):
        for j in range(9):
            val=0
            count=0
            for k in range(0,len(userdict)):
                if listing[i][k]!=0:
                    count=count+1
                    if listing[j][k]!=0:
                        val=val+listing[j][k]
            if (count!=0):
                res[i][j]=float("%.3f" % (float(val)/float(count)));
    for j in userdict:
        existing=[]
        nonexisting=[]
        for i in range(2,11):
            if (userdict[j][i]==0):
                nonexisting.append(i)
            else:
                existing.append(i)
        for k in nonexisting:
            num=0
            if (len(existing)!=0):
                den=0
            else:
                den=1
            for l in existing:
                num+=listing[l-2][k-2]
                den+=1
            userdict[j][k]=float("%.3f" % (float(num)/float(den)));
    print( userdict)
    ifile1.close();

@app.route('/makereturncountsepe')
def makereturncountseperate():
    orderids = {}
    with open('order_final_products.csv','r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if(i != 0):
                #print(row[11].split(' ')[0])
                #print((row[11].split(' ')[0]).split('-')[0])
                if (row[11].split(' ')[0]).split('-')[0] > '2016':
                    #print(orderids.keys())
                    #print(row[2])
                    if row[2] not in orderids.keys():
                        orderids[row[2]] = 1
                    else:
                        orderids[row[2]] += 1
            i = i + 1
    data = {'u_id':[],'s_id':[],'o_id':[],'return_count':[],'return_count nms':[],'return_count similar':[],'nonreturn_count':[]}
    returnidsnms = []
    returnidsstih = []
    allreturns = []
    with open('returns.csv', 'r') as f:
        reader = csv.reader(f)
        c = 1
        for row in reader:
            if(c != 1):
                #print(row)
                #print(len(row))
                #print(row[2])
                if row[2] not in orderids.keys():
                    print('x')
                else:
                    if("not my style" in row[6]):
                        returnidsnms.append(row[2])
                    elif("similar to something I have" in row[6]):
                        returnidsstih.append(row[2])
                    if(row[2] != '1' or row[2] != '550'):
                        allreturns.append(row[2])
            c = c + 1
    returnorderids = Removedup(returnidsnms)
    returnorderids1 = Removedup(returnidsstih)
    with open('stylist.csv', 'r') as f:
        reader = csv.reader(f)
        c = 1
        for row in reader:
            if (c != 1):
                if row[1] in orderids.keys():
                    if orderids[row[1]] < 10:
                        if row[1] not in data['o_id']:
                            data['u_id'].append(row[2])
                            data['s_id'].append(row[3])
                            data['o_id'].append(row[1])
                            data['return_count'].append(0)
                            data['return_count nms'].append(0)
                            data['return_count similar'].append(0)
                            data['nonreturn_count'].append(orderids[row[1]])
            c = c + 1
    for oid in allreturns:
        if oid in data['o_id']:
            i = data['o_id'].index(oid)
            data['return_count'][i] += 1
            data['nonreturn_count'][i] -= 1
    for oid in returnidsnms:
            if(oid in data['o_id']):
                i = data['o_id'].index(oid)
                data['return_count nms'][i] += 1
    for oid in returnidsstih:
    	if oid in data['o_id']:
    		i = data['o_id'].index(oid)
    		data['return_count similar'][i] += 1
    with open('returncountsepe.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['u_id','s_id','o_id','return_count','return_count nms','return_count similar','nonreturn_count'])
        writer.writeheader()
        for i in range(len(data['u_id'])):
            writer.writerow({'u_id':data['u_id'][i],'s_id':data['s_id'][i],'o_id':data['o_id'][i],'return_count':data['return_count'][i],'return_count nms':data['return_count nms'][i],'return_count similar':data['return_count similar'][i],'nonreturn_count':data['nonreturn_count'][i]})

@app.route('/matchsylist/<num>')
def matchsylist(num):
    global userdict
    global stylistdict
    global orders
    global stylist
    global user
    global returns_nms
    global returns_simi
    global success
    rownum=0
    style=0
    for o in orders:
        style+=1
        if user[rownum] not in userdict.keys():
            style+=1
            rownum+=1
            continue;
        else:
            for i in range(0,21):
                stylistdict[stylist[rownum]][0][i]=float(stylistdict[stylist[rownum]][0][i])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(userdict[user[rownum]][i]))
            stylistdict[stylist[rownum]][1]+=1
        rownum+=1;
    calc=0
    for s in stylistdict:
        if (stylistdict[s][1]!=0):
            for i in range(0,21):
                stylistdict[s][0][i]=float(stylistdict[s][0][i])/stylistdict[s][1]
        calc+=stylistdict[s][1];
    find=num
    mval=0;
    msty='';
    matching = {}
    for s in stylistdict:
        val=0
        for i in range(0,21):
            val+=float(userdict[find][i])*float(stylistdict[s][0][i])
        if (val>mval):
            mval=val
            msty=s
        matching[s] = val
    #print(matching)
    matches = sorted(matching.items(), key=lambda item: (item[1], item[0]), reverse=True)
    #print("The best stylist is "+ str(matches[:5]))
    matches = [x[0] for x in matches]
    print(matches)
    yield json.dumps(getnames(matches[:5]))

def matchsylist2(num):
    global userdict
    global stylistdict
    global orders
    global stylist
    global user
    global returns_nms
    global returns_simi
    global success
    rownum=0
    style=0
    for o in orders:
        style+=1
        if user[rownum] not in userdict.keys():
            style+=1
            rownum+=1
            continue;
        else:
            for i in range(0,21):
                stylistdict[stylist[rownum]][0][i]=float(stylistdict[stylist[rownum]][0][i])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(userdict[user[rownum]][i]))
            stylistdict[stylist[rownum]][1]+=1
        rownum+=1;
    calc=0
    for s in stylistdict:
        if (stylistdict[s][1]!=0):
            for i in range(0,21):
                stylistdict[s][0][i]=float(stylistdict[s][0][i])/stylistdict[s][1]
        calc+=stylistdict[s][1];
    find=num
    mval=0;
    msty='';
    matching = {}
    for s in stylistdict:
        val=0
        for i in range(0,21):
            val+=float(userdict[find][i])*float(stylistdict[s][0][i])
        if (val>mval):
            mval=val
            msty=s
        matching[s] = val
    #print(matching)
    matches = sorted(matching.items(), key=lambda item: (item[1], item[0]), reverse=True)
    #print("The best stylist is "+ str(matches[:5]))
    #matches = [x[0] for x in matches]
    print(matches)
    return matches

def getnames(data):
    global stylistnames
    names = []
    for i in range(len(data)):
        for ids in stylistnames:
            if data[i] == ids[0]:
                names.append(ids)
    return names

def getnames1(data):
    global stylistnames
    names = [x for x in stylistnames if x[0] in data]
    return names

@app.route('/stylistids/<uid>/<sids>')
def ranksidforuid(uid,sids):
    global stylistnames
    #print(stylistnames)
    sids = sids.split('s')
    rankings = matchsylist2(uid)
    sid = {}
    for i in range(len(rankings)):
        if rankings[i][0] in sids:
            sid[rankings[i][0]] = rankings[i][1]
    sid = sorted(sid.items(), key=lambda item: (item[1], item[0]), reverse=True)
    data = []
    data1 = [x[0] for x in sid]
    lol = getnames1(data1)
    print(lol)
    print(sid)
    for ids in sid:
        for i in range(len(lol)):
            if lol[i][0] == ids[0]:
                data.append(lol[i])
    print(data)
    yield json.dumps(data)

makevariablesagain()
cleanuserprofile()
makestylistdata()

app.install(EnableCors())

app.run(host='0.0.0.0', port=4000, debug=True, server='gevent')
