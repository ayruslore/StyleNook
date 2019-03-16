import pymysql
from gevent import monkey; monkey.patch_all()
from bottle import route, run, response
import bottle
import csv
import sys
import json
import statistics
from collections import OrderedDict
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler  # For scaling dataset
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation #For clustering
from sklearn.mixture import GaussianMixture #For GMM clustering

class EnableCors(object):
    name = 'enable_cors'
    api = 2
    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            if bottle.request.method != 'OPTIONS':
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
global mediandata
global userclusterdata
global sizeclusters
global stylistreturnpercent
global stylistreturnpercentdistinct
global clustcenters
global stylegenre_clustcenters
global stylegenreclusterlabels
global stylistdistinctuser
global orderuser
global stylistidnames
global budgetcluster_centers
global user_dist_dict
global return_shape
global return_budget
global budgetclusterlabels

def Removedup(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def doKmeans(X, nclust = 5):
    model = KMeans(nclust)
    model.fit(X)
    clust_labels = model.predict(X)
    cent = model.cluster_centers_
    return (clust_labels, cent)

def globaldataloader():
    global stylistnames
    stylistnames = []
    global stylistdict
    stylistdict={}
    global orders
    orders=[]
    global user
    user=[]
    global returns_simi
    returns_simi=[]
    global stylistreturnpercent
    stylistreturnpercent = {}
    global stylistreturnpercentdistinct
    stylistreturnpercentdistinct = {}
    global stylegenre_clustcenters
    stylegenre_clustcenters = []
    global stylistdistinctuser
    stylistdistinctuser = {}
    global orderuser
    orderuser = {}
    global budgetcluster_centers
    budgetcluster_centers = []
    global user_dist_dict
    user_dist_dict = {}
    global return_shape
    return_shape = []
    global return_budget
    return_budget = []
    global userdict
    userdict={}
    global stylist
    stylist=[]
    global returns_nms
    returns_nms=[]
    global success
    success=[]
    global mediandata
    mediandata = []
    global stylistidnames
    stylistidnames = {}
    global stylegenreclusterlabels
    stylegenreclusterlabels = {}
    global clustcenters
    clustcenters = []
    global sizeclusters
    sizeclusters = {"1":[],"2":[],"3":[],"4":[],"0":[]}
    global userclusterdata
    userclusterdata = {}
    global budgetclusterlabels
    budgetclusterlabels = {}
    with open('wp_users.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[3] != '':
                stylistidnames[row[0]] = row[3]
            else:
                stylistidnames[row[0]] = row[4]
    with open('orders.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            orderuser[ row[0] ] = row[1]
    with open('distinctuser.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                if row[0] not in stylistdistinctuser:
                    stylistdistinctuser[ row[0] ] = 1
                else:
                    stylistdistinctuser[ row[0] ] += 1
            c += 1
    with open('budgetcluster.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                budgetclusterlabels[row[0]] = row[1]
            c += 1
    with open('stylegenrecluster.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                stylegenreclusterlabels[row[0]] = row[1]
            c += 1
    with open('shapeclustercenter.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                clustcenters.append([round(float(row[1]), 2), round(float(row[2]), 2)])
            c += 1
    with open('stylegenreclustercenter.csv', 'r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0 :
                stylegenre_clustcenters.append([round(float(row[1]), 2), round(float(row[2]), 2), round(float(row[3]), 2), round(float(row[4]), 2), round(float(row[5]), 2), round(float(row[6]), 2), round(float(row[7]), 2), round(float(row[8]), 2), round(float(row[9]), 2), round(float(row[10]), 2)])
            c += 1
    with open('budgetclustercenter.csv', 'r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                budgetcluster_centers.append([round(float(row[1]), 2), round(float(row[2]), 2), round(float(row[3]), 2), round(float(row[4]), 2), round(float(row[5]), 2), round(float(row[6]), 2), round(float(row[7]), 2), round(float(row[8]), 2)])
            c += 1
    with open('bodyshapecluster.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                userclusterdata[row[0]] = row[1]
                if row[0] not in sizeclusters[row[1]]:
                    sizeclusters[row[1]].append(row[0])
            c += 1
    with open('returncountsepe.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                if row[1] not in stylistreturnpercent.keys():
                    stylistreturnpercent[row[1]] = {'return':int(row[3]) , 'non-return':int(row[6]), 'percent':0}
                else:
                    stylistreturnpercent[row[1]]['return'] += int(row[3])
                    stylistreturnpercent[row[1]]['non-return'] += int(row[6])
            c += 1
    for key in stylistreturnpercent.keys():
        stylistreturnpercent[key]['percent'] = (100.0 * stylistreturnpercent[key]['return'])/(stylistreturnpercent[key]['non-return'] + stylistreturnpercent[key]['return'])
    with open('distinctfirstuser.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c != 0:
                if row[1] not in stylistreturnpercentdistinct.keys():
                    stylistreturnpercentdistinct[row[1]] = {'return':int(row[3]) , 'non-return':int(row[6]), 'percent':0}
                else:
                    stylistreturnpercentdistinct[row[1]]['return'] += int(row[3])
                    stylistreturnpercentdistinct[row[1]]['non-return'] += int(row[6])
            c += 1
    for key in stylistreturnpercentdistinct.keys():
        stylistreturnpercentdistinct[key]['percent'] = (100.0 * stylistreturnpercentdistinct[key]['return'])/(stylistreturnpercentdistinct[key]['non-return'] + stylistreturnpercentdistinct[key]['return'])
    '''
    with open('stylist-vikram.csv','w') as f:
        writer = csv.DictWriter(f,fieldnames=['s_id','total-items-shipped','items-returned'])
        writer.writeheader()
        for key in stylistreturnpercent:
            writer.writerow({'s_id':key, 'total-items-shipped':stylistreturnpercent[key]['non-return']+stylistreturnpercent[key]['return'], 'items-returned':stylistreturnpercent[key]['return']})
    '''

def datadownloader():
    conn = pymysql.connect(host='stylenook.cckva6br9zc4.ap-south-1.rds.amazonaws.com',user='vikram',password='f46ZKohK1K2HHXOH',db='stylenoo_ecom')
    a=conn.cursor()
    sql = 'SELECT * FROM `orders`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('orders.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))
    sql = 'SELECT * FROM `order_final_products`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('order_final_products.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))
    sql = 'SELECT * FROM `returns`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('returns.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))
    sql = 'SELECT * FROM `stylist_assignment`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('stylist_assignment.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))
    sql = 'SELECT * FROM `typeform_data`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('userprofiles.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))
    sql = 'SELECT * FROM `wp_users`;'
    countrow = a.execute(sql)
    data = a.fetchall()
    with open('wp_users.csv','w') as f:
        c = csv.writer(f)
        for row in data:
            c.writerow(list(row))

def makestylistdata():
    global stylistnames
    stylistnames = []
    lol = []
    with open('returncountsepe.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] not in lol:
                lol.append(row[1])
    with open('wp_users.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in lol:
                if row[3] != '':
                    stylistnames.append((row[0],row[3]))
                else:
                    stylistnames.append((row[0],row[4]))

def makevariablesagain():
    global userdict
    global stylistdict
    global orders
    global stylist
    global user
    global returns_nms
    global returns_simi
    global return_shape
    global return_budget
    global success
    global mediandata
    ifile1 = open('returncountsepe.csv', "r")
    reader1 = csv.reader(ifile1)
    rownum=0
    header=[];
    for row in reader1:
        if rownum==0:
            header = row
        else:
               orders.append(row[2]);
               stylist.append(row[1]);
               user.append(row[0]);
               returns_nms.append(int(row[4]));
               returns_simi.append(int(row[5]));
               success.append(int(row[6]));
               return_shape.append(int(row[7]));
               return_budget.append(int(row[8]));
        rownum += 1
    for s in stylist:
        stylistdict[s]=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],0];
    rownum=0
    style=0
    for o in orders:
        style+=1
        if user[rownum] not in userdict.keys() or user[rownum] not in user_dist_dict.keys():
            style+=1
            rownum+=1
            continue;
        else:
            stylistdict[stylist[rownum]][0][0]=float(stylistdict[stylist[rownum]][0][0])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(user_dist_dict[user[rownum]]['STYLE_1']));
            stylistdict[stylist[rownum]][0][1]=float(stylistdict[stylist[rownum]][0][1])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(user_dist_dict[user[rownum]]['STYLE_2']));
            stylistdict[stylist[rownum]][0][2]=float(stylistdict[stylist[rownum]][0][2])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(user_dist_dict[user[rownum]]['STYLE_3']));
            stylistdict[stylist[rownum]][0][3]=float(stylistdict[stylist[rownum]][0][3])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(user_dist_dict[user[rownum]]['STYLE_4']));
            stylistdict[stylist[rownum]][0][4]=float(stylistdict[stylist[rownum]][0][4])+(((float(success[rownum])-float(returns_nms[rownum])+float(returns_simi[rownum]))/5)*float(user_dist_dict[user[rownum]]['STYLE_5']));
            stylistdict[stylist[rownum]][0][5]=float(stylistdict[stylist[rownum]][0][5])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BUDGET_1']));
            stylistdict[stylist[rownum]][0][6]=float(stylistdict[stylist[rownum]][0][6])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BUDGET_2']));
            stylistdict[stylist[rownum]][0][7]=float(stylistdict[stylist[rownum]][0][7])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BUDGET_3']));
            stylistdict[stylist[rownum]][0][8]=float(stylistdict[stylist[rownum]][0][8])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BUDGET_4']));
            stylistdict[stylist[rownum]][0][9]=float(stylistdict[stylist[rownum]][0][9])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BUDGET_5']));
            stylistdict[stylist[rownum]][0][10]=float(stylistdict[stylist[rownum]][0][10])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BODY_1']));
            stylistdict[stylist[rownum]][0][11]=float(stylistdict[stylist[rownum]][0][11])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BODY_2']));
            stylistdict[stylist[rownum]][0][12]=float(stylistdict[stylist[rownum]][0][12])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BODY_3']));
            stylistdict[stylist[rownum]][0][13]=float(stylistdict[stylist[rownum]][0][13])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BODY_4']));
            stylistdict[stylist[rownum]][0][14]=float(stylistdict[stylist[rownum]][0][14])+(((float(success[rownum])-float(return_shape[rownum]))/5)*float(user_dist_dict[user[rownum]]['BODY_5']));
            stylistdict[stylist[rownum]][1]+=1
        rownum+=1;
    calc=0
    for s in stylistdict:
        if (stylistdict[s][1]!=0):
            for i in range(0,15):
                stylistdict[s][0][i]=float(stylistdict[s][0][i])/stylistdict[s][1]
        calc+=stylistdict[s][1];
    ifile1.close();
    mediandata = []
    rsid = list(stylistdict.keys())
    for i in range(len(stylistdict[rsid[0]][0])):
        data = []
        for styid in stylistdict.keys():
            data.append(stylistdict[styid][0][i])
        mediandata.append(statistics.mean(data))

def matchstylist2(num):
    global userdict
    global user_dist_dict
    global stylistdict
    global orders
    global stylist
    global user
    global returns_nms
    global returns_simi
    global success
    global budgetclusterlabels, stylegenreclusterlabels, userclusterdata
    find=num
    mval=0;
    msty='';
    matching = {}
    labels = [budgetclusterlabels[num], stylegenreclusterlabels[num], userclusterdata[num]]
    for s in stylistdict:
        val=0
        val += stylistdict[s][0][int(labels[1])] + stylistdict[s][0][int(labels[0])+5] + stylistdict[s][0][int(labels[2])+10]
        if (val>mval):
            mval=val
            msty=s
        matching[s] = val
    matches = sorted(matching.items(), key=lambda item: (item[1], item[0]), reverse=True)
    return matches

def getnames1(data):
    global stylistnames
    names = [x for x in stylistnames if x[0] in data]
    return names

def cleanuserprofile():
    global userdict
    ifile1 = open('userprofiles.csv', "r")
    reader1 = csv.reader(ifile1)
    rownum=0
    userdict={}
    l=[]
    for row in reader1:
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
            if (row[23]=="Mostly Indian ethnic clothes"):
                userdict[row[1]].append(5);
            elif (row[23]=="A good mix of Western and Indian clothes"):
                userdict[row[1]].append(25);
            elif (row[23]=="Mostly Western clothes"):
                userdict[row[1]].append(45);
            else:
                userdict[row[1]].append(0);
            if ("professional" in row[25]):
                userdict[row[1]].append(3);
            elif ("bit" in row[25]):
                userdict[row[1]].append(6);
            elif ("experiment" in row[25]):
                userdict[row[1]].append(9);
            elif ("individualistic" in row[25]):
                userdict[row[1]].append(12);
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
                if (('upto' in row[i]) and ('750' in row[i])):
                    userdict[row[1]].append(1);
                elif (('upto' in row[i]) and ('1000' in row[i])):
                    userdict[row[1]].append(2);
                elif (('upto' in row[i]) and ('1500' in row[i])):
                    userdict[row[1]].append(3);
                elif (('upto' in row[i]) and ('2000' in row[i])):
                    userdict[row[1]].append(4);
                elif (('2000' in row[i]) and ('upto' not in row[i])):
                    userdict[row[1]].append(5);
                else:
                    userdict[row[1]].append(0);
            if (row[56]!=''):
                userdict[row[1]].append(float(row[56]))
            else:
                userdict[row[1]].append(0);
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
    ifile1.close();

def makeuserdistdict():
    global user_dist_dict, userdict, budgetcluster_centers, stylegenre_clustcenters, clustcenters
    data = {'uid':[],'height':[],'weight':[]}
    with open('userprofiles.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if (row[27] != '') and (row[28] != '') and (row[28] != 'Barcelona'):
                data['uid'].append(row[1])
                b = row[27].split()
                if len(b) == 4:
                    a = float(b[0])*12 + float(b[2])
                else:
                    a = float(b[0])*12
                data['height'].append(a)
                data['weight'].append(float(row[28]))
    data_df = pd.DataFrame({'uid':data['uid'], 'height':data['height'], 'weight':data['weight']})
    user_dist_dict = {}
    data = pd.DataFrame.from_dict(userdict, orient='index')
    data.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w']
    result = {}
    for i in range(0, len(list(data['a']))):
        if list(data['a'])[i] in list(data_df['uid']):
            result[list(data['a'])[i]] = {}
            result[list(data['a'])[i]]['BUDGET_1'] = ((list(data['p']))[i]**2 - budgetcluster_centers[0][0]**2) + ((list(data['q']))[i]**2 - budgetcluster_centers[0][1]**2) +((list(data['r']))[i]**2 - budgetcluster_centers[0][2]**2) + ((list(data['s']))[i]**2 - budgetcluster_centers[0][3]**2) + ((list(data['t']))[i]**2 - budgetcluster_centers[0][4]**2) + ((list(data['u']))[i]**2 - budgetcluster_centers[0][5]**2) + ((list(data['v']))[i]**2 - budgetcluster_centers[0][6]**2)
            result[list(data['a'])[i]]['BUDGET_2'] = ((list(data['p']))[i]**2 - budgetcluster_centers[1][0]**2) + ((list(data['q']))[i]**2 - budgetcluster_centers[1][1]**2) +((list(data['r']))[i]**2 - budgetcluster_centers[1][2]**2) + ((list(data['s']))[i]**2 - budgetcluster_centers[1][3]**2) + ((list(data['t']))[i]**2 - budgetcluster_centers[1][4]**2) + ((list(data['u']))[i]**2 - budgetcluster_centers[1][5]**2) + ((list(data['v']))[i]**2 - budgetcluster_centers[1][6]**2)
            result[list(data['a'])[i]]['BUDGET_3'] = ((list(data['p']))[i]**2 - budgetcluster_centers[2][0]**2) + ((list(data['q']))[i]**2 - budgetcluster_centers[2][1]**2) +((list(data['r']))[i]**2 - budgetcluster_centers[2][2]**2) + ((list(data['s']))[i]**2 - budgetcluster_centers[2][3]**2) + ((list(data['t']))[i]**2 - budgetcluster_centers[2][4]**2) + ((list(data['u']))[i]**2 - budgetcluster_centers[2][5]**2) + ((list(data['v']))[i]**2 - budgetcluster_centers[2][6]**2)
            result[list(data['a'])[i]]['BUDGET_4'] = ((list(data['p']))[i]**2 - budgetcluster_centers[3][0]**2) + ((list(data['q']))[i]**2 - budgetcluster_centers[3][1]**2) +((list(data['r']))[i]**2 - budgetcluster_centers[3][2]**2) + ((list(data['s']))[i]**2 - budgetcluster_centers[3][3]**2) + ((list(data['t']))[i]**2 - budgetcluster_centers[3][4]**2) + ((list(data['u']))[i]**2 - budgetcluster_centers[3][5]**2) + ((list(data['v']))[i]**2 - budgetcluster_centers[3][6]**2)
            result[list(data['a'])[i]]['BUDGET_5'] = ((list(data['p']))[i]**2 - budgetcluster_centers[4][0]**2) + ((list(data['q']))[i]**2 - budgetcluster_centers[4][1]**2) +((list(data['r']))[i]**2 - budgetcluster_centers[4][2]**2) + ((list(data['s']))[i]**2 - budgetcluster_centers[4][3]**2) + ((list(data['t']))[i]**2 - budgetcluster_centers[4][4]**2) + ((list(data['u']))[i]**2 - budgetcluster_centers[4][5]**2) + ((list(data['v']))[i]**2 - budgetcluster_centers[4][6]**2)
            result[list(data['a'])[i]]['STYLE_1'] = ((list(data['c']))[i]**2 - stylegenre_clustcenters[0][0]**2) + ((list(data['d']))[i]**2 - stylegenre_clustcenters[0][1]**2) +((list(data['e']))[i]**2 - stylegenre_clustcenters[0][2]**2) + ((list(data['f']))[i]**2 - stylegenre_clustcenters[0][3]**2) + ((list(data['g']))[i]**2 - stylegenre_clustcenters[0][4]**2) + ((list(data['h']))[i]**2 - stylegenre_clustcenters[0][5]**2) + ((list(data['i']))[i]**2 - stylegenre_clustcenters[0][6]**2) + ((list(data['j']))[i]**2 - stylegenre_clustcenters[0][7]**2) + ((list(data['k']))[i]**2 - stylegenre_clustcenters[0][7]**2) + ((list(data['m']))[i]**2 - stylegenre_clustcenters[0][8]**2)
            result[list(data['a'])[i]]['STYLE_2'] = ((list(data['c']))[i]**2 - stylegenre_clustcenters[1][0]**2) + ((list(data['d']))[i]**2 - stylegenre_clustcenters[1][1]**2) +((list(data['e']))[i]**2 - stylegenre_clustcenters[1][2]**2) + ((list(data['f']))[i]**2 - stylegenre_clustcenters[1][3]**2) + ((list(data['g']))[i]**2 - stylegenre_clustcenters[1][4]**2) + ((list(data['h']))[i]**2 - stylegenre_clustcenters[1][5]**2) + ((list(data['i']))[i]**2 - stylegenre_clustcenters[1][6]**2) + ((list(data['j']))[i]**2 - stylegenre_clustcenters[1][7]**2) + ((list(data['k']))[i]**2 - stylegenre_clustcenters[1][7]**2) + ((list(data['m']))[i]**2 - stylegenre_clustcenters[1][8]**2)
            result[list(data['a'])[i]]['STYLE_3'] = ((list(data['c']))[i]**2 - stylegenre_clustcenters[2][0]**2) + ((list(data['d']))[i]**2 - stylegenre_clustcenters[2][1]**2) +((list(data['e']))[i]**2 - stylegenre_clustcenters[2][2]**2) + ((list(data['f']))[i]**2 - stylegenre_clustcenters[2][3]**2) + ((list(data['g']))[i]**2 - stylegenre_clustcenters[2][4]**2) + ((list(data['h']))[i]**2 - stylegenre_clustcenters[2][5]**2) + ((list(data['i']))[i]**2 - stylegenre_clustcenters[2][6]**2) + ((list(data['j']))[i]**2 - stylegenre_clustcenters[2][7]**2) + ((list(data['k']))[i]**2 - stylegenre_clustcenters[2][7]**2) + ((list(data['m']))[i]**2 - stylegenre_clustcenters[2][8]**2)
            result[list(data['a'])[i]]['STYLE_4'] = ((list(data['c']))[i]**2 - stylegenre_clustcenters[3][0]**2) + ((list(data['d']))[i]**2 - stylegenre_clustcenters[3][1]**2) +((list(data['e']))[i]**2 - stylegenre_clustcenters[3][2]**2) + ((list(data['f']))[i]**2 - stylegenre_clustcenters[3][3]**2) + ((list(data['g']))[i]**2 - stylegenre_clustcenters[3][4]**2) + ((list(data['h']))[i]**2 - stylegenre_clustcenters[3][5]**2) + ((list(data['i']))[i]**2 - stylegenre_clustcenters[3][6]**2) + ((list(data['j']))[i]**2 - stylegenre_clustcenters[3][7]**2) + ((list(data['k']))[i]**2 - stylegenre_clustcenters[3][7]**2) + ((list(data['m']))[i]**2 - stylegenre_clustcenters[3][8]**2)
            result[list(data['a'])[i]]['STYLE_5'] = ((list(data['c']))[i]**2 - stylegenre_clustcenters[4][0]**2) + ((list(data['d']))[i]**2 - stylegenre_clustcenters[4][1]**2) +((list(data['e']))[i]**2 - stylegenre_clustcenters[4][2]**2) + ((list(data['f']))[i]**2 - stylegenre_clustcenters[4][3]**2) + ((list(data['g']))[i]**2 - stylegenre_clustcenters[4][4]**2) + ((list(data['h']))[i]**2 - stylegenre_clustcenters[4][5]**2) + ((list(data['i']))[i]**2 - stylegenre_clustcenters[4][6]**2) + ((list(data['j']))[i]**2 - stylegenre_clustcenters[4][7]**2) + ((list(data['k']))[i]**2 - stylegenre_clustcenters[4][7]**2) + ((list(data['m']))[i]**2 - stylegenre_clustcenters[4][8]**2)
    i = 0
    for uid in list(data_df['uid']):
        if uid in result.keys():
            result[uid]['BODY_1'] = (list(data_df['height'])[i]**2 - clustcenters[0][0]**2) + (list(data_df['weight'])[i]**2 - clustcenters[0][1]**2)
            result[uid]['BODY_2'] = (list(data_df['height'])[i]**2 - clustcenters[1][0]**2) + (list(data_df['weight'])[i]**2 - clustcenters[1][1]**2)
            result[uid]['BODY_3'] = (list(data_df['height'])[i]**2 - clustcenters[2][0]**2) + (list(data_df['weight'])[i]**2 - clustcenters[2][1]**2)
            result[uid]['BODY_4'] = (list(data_df['height'])[i]**2 - clustcenters[3][0]**2) + (list(data_df['weight'])[i]**2 - clustcenters[3][1]**2)
            result[uid]['BODY_5'] = (list(data_df['height'])[i]**2 - clustcenters[4][0]**2) + (list(data_df['weight'])[i]**2 - clustcenters[4][1]**2)
        i += 1
    user_dist_dict = result

#@app.route('/makebudgetcluster')
def makebudgetcluster():
    global userdict
    data = pd.DataFrame.from_dict(userdict, orient='index')
    data.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w']
    new_df = data[['p', 'q', 'r', 's', 't', 'u', 'v', 'w']]
    clust_labels, centers = doKmeans(new_df, 5)
    with open('budgetclustercenter.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['label', 'budget_pant', 'budget_westerndress', 'budget_top', 'budget_skirt', 'budget_kurta', 'budget_jacket', 'budget_scarf', 'budget_jewellery'])
        writer.writeheader()
        for i in range(len(centers)):
            writer.writerow({'label':i, 'budget_pant':centers[i][0], 'budget_westerndress':centers[i][1], 'budget_top':centers[i][2], 'budget_skirt':centers[i][3], 'budget_kurta':centers[i][4], 'budget_jacket':centers[i][5], 'budget_scarf':centers[i][6], 'budget_jewellery':centers[i][7]})
    with open('budgetcluster.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['uid', 'label', 'budget_pant', 'budget_westerndress', 'budget_top', 'budget_skirt', 'budget_kurta', 'budget_jacket', 'budget_scarf', 'budget_jewellery'])
        writer.writeheader()
        for i in range(len(data['a'])):
            writer.writerow({'uid':data['a'][i], 'label':clust_labels[i], 'budget_pant':new_df['p'][i], 'budget_westerndress':new_df['q'][i], 'budget_top':new_df['r'][i], 'budget_skirt':new_df['s'][i], 'budget_kurta':new_df['t'][i], 'budget_jacket':new_df['u'][i], 'budget_scarf':new_df['u'][i], 'budget_jewellery':new_df['v'][i]})
    return "Success"

#@app.route('/makestylegenrecluster')
def makestylegenrecluster():
    global userdict, stylegenre_clustcenters
    data = pd.DataFrame.from_dict(userdict, orient='index')
    data.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w']
    new_df = data[['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm']]
    clust_labels, centers = doKmeans(new_df, 5)
    with open('stylegenreclustercenter.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['label', 'western_classic', 'western_feminine', 'western_contemporary', 'western_boho', 'indo_western', 'indian_traditional', 'indian_classic', 'indian_contemporary', 'indian_funky', 'clothes_work'])
        writer.writeheader()
        for i in range(len(centers)):
            writer.writerow({'label':i, 'western_classic':centers[i][0], 'western_feminine':centers[i][1], 'western_contemporary':centers[i][2], 'western_boho':centers[i][3], 'indo_western':centers[i][4], 'indian_traditional':centers[i][5], 'indian_classic':centers[i][6], 'indian_contemporary':centers[i][7], 'indian_funky':centers[i][8], 'clothes_work':centers[i][9]})
    with open('stylegenrecluster.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['uid', 'label', 'western_classic', 'western_feminine', 'western_contemporary', 'western_boho', 'indo_western', 'indian_traditional', 'indian_classic', 'indian_contemporary', 'indian_funky', 'clothes_work'])
        writer.writeheader()
        for i in range(len(data['a'])):
            writer.writerow({'uid':list(data['a'])[i], 'label':clust_labels[i], 'western_classic':new_df['c'][i], 'western_feminine':new_df['d'][i], 'western_contemporary':new_df['e'][i], 'western_boho':new_df['f'][i], 'indo_western':new_df['g'][i], 'indian_traditional':new_df['h'][i], 'indian_classic':new_df['i'][i], 'indian_contemporary':new_df['j'][i], 'indian_funky':new_df['k'][i] , 'clothes_work':new_df['m'][i]})
    return "Success"

#@app.route('/makebodyshapecluster')
def makebodyshapecluster():
    global clustcenters
    data = {'uid':[],'height':[],'weight':[]}
    with open('userprofiles.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if (row[27] != '') and (row[28] != '') and (row[28] != 'Barcelona'):
                data['uid'].append(row[1])
                data['height'].append(row[27])
                data['weight'].append(float(row[28]))
    data_df = pd.DataFrame({'uid':data['uid'], 'height':data['height'], 'weight':data['weight']})
    heights = []
    for i in data_df['height']:
        b = i.split()
        a = float(b[0])*12 + float(b[2])
        heights.append(a)
    new_df = pd.DataFrame(OrderedDict({'height':heights, 'weight': data_df['weight']}))
    clust_labels, centers = doKmeans(new_df, 5)
    with open('shapeclustercenter.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ['label', 'x', 'y'])
        writer.writeheader()
        for i in range(len(centers)):
            writer.writerow({'label':i, 'x':centers[i][0], 'y':centers[i][1]})
    with open('bodyshapecluster.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['u_id','label','height', 'weight'])
        writer.writeheader()
        for i in range(len(data_df['uid'])):
            writer.writerow({'u_id':data_df['uid'][i],'label':clust_labels[i],'height':new_df['height'][i], 'weight':new_df['weight'][i]})
    return "Success"

#@app.route('/makereturncountseperate')
def makereturncountseperate():
    orderids = {}
    with open('order_final_products.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
                if (row[11].split(' ')[0]).split('-')[0] > '2016':
                    if row[2] not in orderids.keys():
                        orderids[row[2]] = 1
                    else:
                        orderids[row[2]] += 1
    data = {'u_id':[],'s_id':[],'o_id':[],'return_count':[],'return_count nms':[],'return_count similar':[],'nonreturn_count':[], 'return_shape':[], 'return_budget':[]}
    returnidsnms = []
    returnidsstih = []
    returnshape = []
    returnbudget = []
    allreturns = []
    with open('returns.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[2] in orderids.keys():
                if(("not my style" in row[6]) or ("Not my style" in row[6]) or ("Not my colour" in row[6]) or ("Not work wear" in row[6]) or ("Not apt for my work" in row[6])):
                    returnidsnms.append(row[2])
                elif(("similar to something I have" in row[6]) or ("Similar style" in row[6]) or ("Similar color" in row[6])):
                    returnidsstih.append(row[2])
                elif(('too big' in row[6]) or ('too small' in row[6]) or ('Too big' in row[6]) or ('Too short' in row[6]) or ('Too long' in row[6]) or ('Too high' in row[6]) or ('Too small' in row[6])):
                    returnshape.append(row[2])
                elif(('Too expensive' in row[6]) or ('Poor fabric' in row[6]) or ('too expensive' in row[6]) or ('Poor finish' in row[6]) or ('Not worth it' in row[6]) or ('poor quality' in row[6])):
                    returnbudget.append(row[2])
                if(row[2] != '1' or row[2] != '550'):
                    allreturns.append(row[2])
    returnorderids = Removedup(returnidsnms)
    returnorderids1 = Removedup(returnidsstih)
    with open('stylist_assignment.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
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
                            data['return_shape'].append(0)
                            data['return_budget'].append(0)
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
    for oid in returnshape:
    	if oid in data['o_id']:
    		i = data['o_id'].index(oid)
    		data['return_shape'][i] += 1
    for oid in returnbudget:
        if oid in data['o_id']:
            i = data['o_id'].index(oid)
            data['return_budget'][i] += 1
    with open('returncountsepe.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['u_id','s_id','o_id','return_count','return_count nms','return_count similar','nonreturn_count', 'return_shape', 'return_budget'])
        writer.writeheader()
        for i in range(len(data['u_id'])):
            writer.writerow({'u_id':data['u_id'][i],'s_id':data['s_id'][i],'o_id':data['o_id'][i],'return_count':data['return_count'][i],'return_count nms':data['return_count nms'][i],'return_count similar':data['return_count similar'][i],'nonreturn_count':data['nonreturn_count'][i], 'return_shape':data['return_shape'][i], 'return_budget':data['return_budget'][i]})

#@app.route('/makedistinctfirstuser')
def makedistinctfirstuser():
    data = {}
    with open('returncountsepe.csv', 'r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c!= 0:
                if tuple([row[0], row[1]]) not in data:
                    data[ tuple([row[0], row[1]]) ] = {'o_id': int(row[2]),'return_count':int(row[3]), 'returns nms':int(row[4]), 'return_count similar': int(row[5]), 'nonreturn_count': int(row[6]), 'return_shape':int(row[7])}
            c += 1
    keys = list(data.keys())
    distinctuser = {}
    for key in keys:
        if key[1] not in distinctuser:
            distinctuser[ key[1] ] = [ key[0] ]
        else:
            distinctuser[ key[1] ].append( key[0] )
    with open('distinctfirstuser.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames = [ 'u_id', 's_id', 'o_id','return_count', 'returns nms', 'return_count similar', 'nonreturn_count', 'return_shape'])
        writer.writeheader()
        for sid in distinctuser:
            for uids in distinctuser[ sid ]:
                writer.writerow({'u_id': uids, 's_id': sid, 'o_id' : data[ tuple([uids, sid]) ]['o_id'], 'return_count': data[ tuple([uids, sid]) ]['return_count'], 'returns nms' : data[ tuple([uids, sid]) ]['returns nms'], 'return_count similar' : data[ tuple([uids, sid]) ]['return_count similar'], 'nonreturn_count' : data[ tuple([uids, sid]) ]['nonreturn_count'], 'return_shape' : data[ tuple([uids, sid]) ]['return_shape']})

#@app.route('/makedistinctuser')
def makedistinctuser():
    data = {}
    with open('returncountsepe.csv', 'r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c!= 0:
                if tuple([row[0], row[1]]) not in data:
                    data[ tuple([row[0], row[1]]) ] = {'return_count':int(row[3]), 'returns nms':int(row[4]), 'return_count similar': int(row[5]), 'nonreturn_count': int(row[6]), 'return_shape':int(row[7])}
                else:
                    data[ tuple([row[0], row[1]]) ]['return_count'] += int(row[3])
                    data[ tuple([row[0], row[1]]) ]['returns nms'] += int(row[4])
                    data[ tuple([row[0], row[1]]) ]['return_count similar'] += int(row[5])
                    data[ tuple([row[0], row[1]]) ]['nonreturn_count'] += int(row[6])
                    data[ tuple([row[0], row[1]]) ]['return_shape'] += int(row[7])
            c += 1
    keys = list(data.keys())
    distinctuser = {}
    for key in keys:
        if key[1] not in distinctuser:
            distinctuser[ key[1] ] = [ key[0] ]
        else:
            distinctuser[ key[1] ].append( key[0] )
    with open('distinctuser.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames = ['s_id', 'u_id', 'return_count', 'returns nms', 'return_count similar', 'nonreturn_count', 'return_shape'])
        writer.writeheader()
        for sid in distinctuser:
            for uids in distinctuser[ sid ]:
                writer.writerow({'s_id': sid, 'u_id': uids, 'return_count': data[ tuple([uids, sid]) ]['return_count'], 'returns nms' : data[ tuple([uids, sid]) ]['returns nms'], 'return_count similar' : data[ tuple([uids, sid]) ]['return_count similar'], 'nonreturn_count' : data[ tuple([uids, sid]) ]['nonreturn_count'], 'return_shape' : data[ tuple([uids, sid]) ]['return_shape']})

app = bottle.app()

@app.route('/trigger_to_reload_data')
def trigger():
    datadownloader()
    print('Data downloaded!!')
    #fghjnk
    globaldataloader()
    cleanuserprofile()
    makeuserdistdict()
    makestylistdata()
    makevariablesagain()
    print('Variables made!!')
    #fghjk
    makereturncountseperate()
    makebudgetcluster()
    makebodyshapecluster()
    makedistinctuser()
    makedistinctfirstuser()
    makestylegenrecluster()
    print('Clusters ready!!')
    #sdfgthyjk
    globaldataloader()
    cleanuserprofile()
    makeuserdistdict()
    makestylistdata()
    makevariablesagain()
    print('Variables ready')

@app.route('/getstylistreturngenrecluster/<sid>')
def stylistreturngenrecluster(sid):
    global stylegenreclusterlabels
    data = {}
    with open('returncountsepe.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        c = 0
        for row in reader:
            if c != 0:
                if sid == row[1]:
                    if stylegenreclusterlabels[row[0]] in data.keys():
                        data[stylegenreclusterlabels[row[0]]]['return'] += int(row[3])
                        data[stylegenreclusterlabels[row[0]]]['non-return'] += int(row[6])
                        data[stylegenreclusterlabels[row[0]]]['return-nms'] += int(row[4])
                    else:
                        data[stylegenreclusterlabels[row[0]]] = {'return':int(row[3]) , 'non-return':int(row[6]), 'percent':0.0, 'return-nms':int(row[4])}
            c += 1
    for keys in data:
        if (data[keys]['return'] + data[keys]['non-return']) != 0:
            data[keys]['percent'] = (data[keys]['return-nms'] * 100)/(data[keys]['return'] + data[keys]['non-return'])
        else:
            data[keys]['percent'] = 0.0
    yield json.dumps(data)

@app.route('/getstylegenrecluster_centers')
def getgenreclustercenters():
    global stylegenre_clustcenters
    yield json.dumps(stylegenre_clustcenters)

@app.route('/getcluster_centers')
def getclustercenters():
    global clustcenters
    yield json.dumps(clustcenters)

@app.route('/getclusterdata/<oid>')
def getclusterdata(oid):
    global stylegenreclusterlabels, userclusterdata, clustcenters, stylegenre_clustcenters, orderuser, budgetcluster_centers, budgetclusterlabels
    uid = orderuser[oid]
    data = {}
    if uid in stylegenreclusterlabels and uid in userclusterdata:
        data['val'] = 'True'
        data['1'] = stylegenreclusterlabels[uid]
        data['2'] = userclusterdata[uid]
        data['3'] = clustcenters
        data['4'] = stylegenre_clustcenters
        data['5'] = budgetcluster_centers
        data['6'] = budgetclusterlabels[uid]
        data['uid'] = uid
    else:
        data['val'] = 'False'
        data['uid'] = uid
    yield json.dumps(data)

@app.route('/getstylistnames')
def getstylistnames():
    global stylistnames
    yield json.dumps(stylistnames)

@app.route('/getstylistdict/<sid>')
def stylistdictdata(sid):
    global stylistdict
    global mediandata
    result = []
    for i in range(len(stylistdict[sid][0])):
        result.append([str(round(stylistdict[sid][0][i], 4)) ,str(round(mediandata[i], 4))])
    yield json.dumps(result)

@app.route('/stylistreturncluster/<sid>')
def getstylistclusterreturn(sid):
    global stylistnames
    global userclusterdata
    global sizeclusters
    data = {'1':{'return': 0, 'non-return':0, 'return-shape':0}, '2':{'return': 0, 'non-return':0, 'return-shape':0}, '3':{'return': 0, 'non-return':0, 'return-shape':0}, '4':{'return': 0, 'non-return':0, 'return-shape':0}, '0':{'return': 0, 'non-return':0, 'return-shape':0}}
    with open('returncountsepe.csv','r') as f:
        reader = csv.reader(f)
        c = 0
        for row in reader:
            if c!= 0 :
                if row[1] == sid:
                    if row[0] in userclusterdata.keys():
                        data[userclusterdata[row[0]]]['return'] += int(row[3])
                        data[userclusterdata[row[0]]]['non-return'] += int(row[6])
                        data[userclusterdata[row[0]]]['return-shape'] += int(row[7])
            c += 1
    for keys in data:
        if (data[keys]['return'] + data[keys]['non-return']) != 0:
            data[keys]['percent'] = (data[keys]['return-shape'] * 100)/(data[keys]['return'] + data[keys]['non-return'])
        else:
            data[keys]['percent'] = 0
    yield json.dumps(data)

@app.route('/stylistassignment/<oids>/<sids>/<rep>')
def stylistassignment(oids, sids, rep):
    global orderuser, stylistidnames
    sids = sids.split(',')
    oids = oids.split(',')
    tupleList = []  #threetuples
    user = []       #array for user
    count = {}      #stylist
    for sid in sids:
        count[sid] = 0
    for oid in oids:
        rankings = matchstylist2(orderuser[oid])
        for i in rankings:
            tupleList.append(tuple([i[0], i[1], orderuser[oid],oid]))  #(stylistid, probablity, uid, oid)
    tupleList.sort(key=lambda tup: tup[1])    # sortedtuple list of above
    result=[]
    for samples in tupleList:
        if(samples[0]  in sids):
         if((samples[2] not in user) and (count[samples[0]]<int(rep))):
            user.append(samples[2])
            count[samples[0]] +=1
            result.append([samples[3], samples[2],samples[0], stylistidnames[samples[0]]])
    yield json.dumps(result)

@app.route('/stylistidusers/<oid>/<sids>')
def ranksidforuid_maxusers(oid,sids):
    global stylistnames, stylistreturnpercentdistinct, stylistdistinctuser
    global stylist, stylistdict, orderuser
    uid = orderuser[oid]
    sids = sids.split(',')
    max_o = -10000
    for sid in sids:
        if (stylistdistinctuser[sid]) >= max_o:
            max_o = stylistdistinctuser[sid]
    rankings = matchstylist2(uid)
    sid = {}
    for i in range(len(rankings)):
        if rankings[i][0] in sids:
            sid[rankings[i][0]] = rankings[i][1] #* (float(stylistdistinctuser[ rankings[i][0] ])/float(max_o))
    sid = sorted(sid.items(), key=lambda item: (item[1], item[0]), reverse=True)
    data = []
    data1 = [x[0] for x in sid]
    lol = getnames1(data1)
    for ids in sid:
        for i in range(len(lol)):
            if lol[i][0] == ids[0]:
                data.append(lol[i])
    result = {'data':[], 'uid':uid}
    for i in range(len(data)):
        result['data'].append([data[i][0], data[i][1], round(sid[i][1],2) , round(stylistreturnpercentdistinct[data[i][0]]['percent'],2), stylistreturnpercentdistinct[data[i][0]]['return'] + stylistreturnpercentdistinct[data[i][0]]['non-return'], stylistreturnpercentdistinct[data[i][0]]['return'], stylistdistinctuser[data[i][0]]])
    yield json.dumps(result)

@app.route('/stylistreturncolumn/<sid>/<num>')
def stylistreturnaccordingtocolumn(sid,num):
    ifile1 = open('returncountsepe.csv', "r")
    reader1 = csv.reader(ifile1)
    returns = 0
    nonreturns = 0
    uids = []
    user = {}
    for row in reader1:
        if row[1] == sid:
            uids.append(row[0])
            returns += int(row[3]) + int(row[4]) + int(row[5])
            nonreturns += int(row[6])
            if row[0] not in user.keys():
                user[row[0]] = {'return':int(row[3]) , 'nonreturn':int(row[6])}
            else:
                user[row[0]]['return'] += int(row[3])
                user[row[0]]['nonreturn'] += int(row[6])
    data = {}
    ifile1.close()
    ifile2 = open('userprofiles.csv','r')
    reader2 = csv.reader(ifile2)
    for row in reader2:
        if row[1] in uids:
            data[row[1]] = [row[int(num)]]
            if int(num) == 6:
                if (row[6].strip().lower()=="never"):
                    data[row[1]].append(1)
                elif ((row[6].strip().lower()=="sometimes") or (row[6].strip().lower()=="a little bit")):
                    data[row[1]].append(2)
                elif (row[6].strip().lower()=="all the time!"):
                    data[row[1]].append(3)
                else:
                    data[row[1]].append(0)
            if int(num) in [10,11,12,13,14,15,16,17,18]:
                if ("Umm OK" in row[int(num)]) or ("OK." in row[int(num)]):
                    data[row[1]].append(2)
                elif ("Love it!" in row[int(num)]) or ("Love this collection!" in row[int(num)]):
                    data[row[1]].append(4)
                elif "Quite like this range" in row[int(num)]:
                    data[row[1]].append(3)
                elif 'Hate this collection!' in row[int(num)]:
                    data[row[1]].append(1)
                else:
                    data[row[1]].append(0)
            if int(num) == 23:
                if ('mostly western' in row[23].strip().lower()) and ('indian' not in row[23].strip().lower()):
                    data[row[1]].append(1)
                elif ('mix' in row[23].strip().lower()) and ('western' in row[23].strip().lower()) and ('indian' in row[23].strip().lower()):
                    data[row[1]].append(2)
                elif ('indian' in row[23].strip().lower()) and ('ethnic' in row[23].strip().lower()):
                    data[row[1]].append(3)
                elif ('western' not in row[23].strip().lower()) and ('indian' in row[23].strip().lower()):
                    data[row[1]].append(4)
                else:
                    data[row[1]].append(0)
            if int(num) == 25:
                if (("stick" in row[25]) and ("professional" in row[25])):
                    data[row[1]].append(4)
                elif (("bit" in row[25]) and ("add" in row[25])):
                    data[row[1]].append(3)
                elif ("experiment a bit" in row[25]):
                    data[row[1]].append(2)
                elif ("individualistic" in row[25]):
                    data[row[1]].append(1)
                else:
                    data[row[1]].append(0)
            if int(num) == 36:
                if "a" in row[36].strip().lower():
                    data[row[1]].append('A')
                elif "b" in row[36].strip().lower():
                    data[row[1]].append('B')
                elif "c" in row[36].strip().lower():
                    data[row[1]].append('C')
                elif "d" in row[36].strip().lower():
                    data[row[1]].append('D')
                elif "e" in row[36].strip().lower():
                    data[row[1]].append('E')
                elif "f" in row[36].strip().lower():
                    data[row[1]].append('F')
                elif "g" in row[36].strip().lower():
                    data[row[1]].append('G')
                elif "h" in row[36].strip().lower():
                    data[row[1]].append('H')
                elif "i" in row[36].strip().lower():
                    data[row[1]].append('I')
                else:
                    data[row[1]].append('J')
            if int(num) == 37:
                if (('18' in row[37]) and ('24' in row[37])):
                    data[row[1]].append(1)
                elif (('25' in row[37]) and ('29' in row[37])):
                    data[row[1]].append(2)
                elif (('30' in row[37]) and ('34' in row[37])):
                    data[row[1]].append(3)
                elif (('35' in row[37]) and ('40' in row[37])):
                    data[row[1]].append(4)
                elif (('40' in row[37]) and ('35' not in row[37]) and ('+' in row[37])):
                    data[row[1]].append(5)
                else:
                    data[row[1]].append(0)
            if int(num) in [38,39,40,41,42,43,44,45]:
                if (('upto' in row[int(num)]) and ('750' in row[int(num)])):
                    data[row[1]].append(1)
                elif (('upto' in row[int(num)]) and ('1000' in row[int(num)])):
                    data[row[1]].append(2)
                elif (('upto' in row[int(num)]) and ('1500' in row[int(num)])):
                    data[row[1]].append(3)
                elif (('upto' in row[int(num)]) and ('2000' in row[int(num)])):
                    data[row[1]].append(4)
                elif (('2000' in row[int(num)]) and ('upto' not in row[int(num)])):
                    data[row[1]].append(5)
                else:
                    data[row[1]].append(0)
    check = {}
    for ids in data.keys():
        if data[ids][1] not in check.keys():
            check[data[ids][1]] = [ids]
        else:
            check[data[ids][1]].append(ids)
    tot = 0
    result = {}
    ifile2.close()
    for cloth in check.keys():
        ret = 0
        nonret =0
        for ids in check[cloth]:
            ret += user[ids]['return']
            nonret += user[ids]['nonreturn']
        result[cloth] = (float(ret*100)/float(ret+nonret))
    finalresult = {}
    for keys in result.keys():
        if int(num) == 6:
            if keys == 1:
                finalresult["never"] = result[1]
            elif keys == 2:
                finalresult["sometimes (or) a little bit"] = result[2]
            elif keys == 3:
                finalresult["all the time!"] = result[3]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
        if int(num) in [10,11,12,13,14,15,16,17,18]:
            if keys == 2:
                finalresult["Umm OK"] = result[2]
            elif keys == 4:
                finalresult["Love this collection!"] = result[4]
            elif keys == 3:
                finalresult["Quite like this range"] = result[3]
            elif keys == 1:
                finalresult["Hate this collection!"] = result[1]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
        if int(num) == 23 :
            if keys == 1:
                finalresult["Mostly Western Clothes"] = result[1]
            elif keys == 2:
                finalresult["Mix of Western and Indian Clothes"] = result[2]
            elif keys == 3 :
                finalresult["Mostly Indian Ethnic Clothes"] = result[3]
            elif keys == 4 :
                finalresult["Mostly Indian Clothes"] = result[4]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
        if int(num) == 25:
            if keys == 1:
                finalresult['be highly individualistic creating your own look'] = result[1]
            elif keys == 3:
                finalresult['add your bit to the professional work look'] = result[3]
            elif keys == 4:
                finalresult['stick to the professional work look'] = result[4]
            elif keys == 2:
                finalresult['experiment a bit more'] = result[2]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
        if int(num) == 36:
            if keys == 'A':
                finalresult['A'] = result['A']
            elif keys == 'B':
                finalresult['B'] = result['B']
            elif keys == 'C':
                finalresult['C'] = result['C']
            elif keys == 'D':
                finalresult['D'] = result['D']
            elif keys == 'E':
                finalresult['E'] = result['E']
            elif keys == 'F':
                finalresult['F'] = result['F']
            elif keys == 'G':
                finalresult['G'] = result['G']
            elif keys == 'H':
                finalresult['H'] = result['H']
            elif keys == 'I':
                finalresult['I'] = result['I']
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result['J']
        if int(num) == 37:
            if keys == 1:
                finalresult['18 - 24 years'] = result[1]
            elif keys == 2:
                finalresult['25 - 29 years'] = result[2]
            elif keys == 3:
                finalresult['30 - 34 years'] = result[3]
            elif keys == 4:
                finalresult['35 - 40 years'] = result[4]
            elif keys == 5:
                finalresult['40 + years'] = result[5]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
        if int(num) in [38,39,40,41,42,43,44,45]:
            if keys == 1:
                finalresult['Upto Rs 750'] = result[1]
            elif keys == 2:
                finalresult['Upto Rs 1000'] = result[2]
            elif keys == 3:
                finalresult['Upto Rs 1500'] = result[3]
            elif keys == 4:
                finalresult['Upto Rs 2000'] = result[4]
            elif keys == 5:
                finalresult['Rs 2000+ '] = result[5]
            else:
                finalresult['GARBAGE VALUES (OR) NULL'] = result[0]
    yield json.dumps(finalresult)

trigger()

app.install(EnableCors())

app.run(host='0.0.0.0', port=4000, debug=True, server='gevent')
