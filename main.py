from flask import Flask, render_template, request
import sqlite3
import textwrap
import pyodbc
import time
import os

app = Flask(__name__)


driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'assign1server'
database_name = 'assignment1'
server = 'tcp:database.windows.net,1433'
username = "saitheja"
password = "9705004946S@i"

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/q5')
def q5():
   return render_template('q5.html')
@app.route('/q6')
def q6():
   return render_template('q6.html')


@app.route('/q8')
def q8():
   return render_template('q8.html')

@app.route('/q')
def q():
   return render_template('newrecord.html')



@app.route('/mag', methods=['POST','GET'])
def list():
    
   
    e1=request.form['e1']
    e2=request.form['e2']
    d1=request.form['d1']
    d2=request.form['d2']
    querry="Select count(*) from q WHERE etime  between '"+e1+"' and '"+e2+"' and depth  between '"+d1+"' and '"+d2+"' "
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    crsr.execute(querry)
    count=crsr.fetchone()
    querry1="Select top(5) id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE etime  between '"+e1+"' and '"+e2+"' and depth  between '"+d1+"' and '"+d2+"' ORDER BY mag asc"
    crsr.execute(querry1)
    rows = crsr.fetchall()
    print(count)
    cnxx.close()
    return render_template("list.html",rows = rows,count=count)

@app.route('/all', methods=['POST','GET'])
def fulllist():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select type,count(*) from all_month group by type"
    crsr.execute(querry)
    rows=crsr.fetchall()
    cnxx.close()
    return render_template("pie.html",rows = rows)


@app.route('/dn', methods=['POST','GET'])
def dn():

    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    
    querry="SELECT 'Night',COUNT(*) FROM all_month where DATEPART(HOUR,time) >=18 or DATEPART(HOUR,time) <=6 "
    crsr.execute(querry)
    rows=crsr.fetchall()
    querry="SELECT 'Day',COUNT(*) FROM all_month where DATEPART(HOUR,time) <=18 or DATEPART(HOUR,time) >=6 "
    crsr.execute(querry)
    row1=crsr.fetchall()
    rows.append(row1[0])
    cnxx.close()
    return render_template("Bar.html",rows = rows)

@app.route('/range', methods=['POST','GET'])
def range():
    
    list=[1,2,3,4,5]
    
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    row=[]
    p1=int(request.form['p1'])
    p2=int(request.form['p2'])
    
    querry="Select StateName,TotalPop from voting where TotalPop>"+str(p1)+" and TotalPop<"+str(p2)+"group by StateName,TotalPop"
    crsr.execute(querry)
    rows=crsr.fetchall()
    
       
    return render_template("pie.html",rows = rows)

@app.route('/votes', methods=['POST','GET'])
def votes():
    
    list=[1,2,3,4,5]
    
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    row=[]
    p1=int(request.form['v1'])
    p2=int(request.form['v2'])
    
    querry="Select StateName,VotePop from voting where VotePop>"+str(p1)+" and VotePop<"+str(p2)+"group by StateName,VotePop"
    crsr.execute(querry)
    rows=crsr.fetchall()
    
       
    return render_template("Bar.html",rows = rows)

@app.route('/total', methods=['POST','GET'])
def total():
    
    list=[1,2,3,4,5]
    
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    row=[]
    p1=int(request.form['t1'])
    p2=int(request.form['t2'])
    
    querry="Select TotalPop,Voted from voting where VotePop>"+str(p1)+" and VotePop<"+str(p2)
    crsr.execute(querry)
    rows=crsr.fetchall()
    
       
    return render_template("sc.html",rows = rows)

@app.route('/top', methods=['POST','GET'])
def top():
    n=request.form['n']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select top("+n+") latitude,longitude,mag from all_month order by time desc"
    crsr.execute(querry)
    rows=crsr.fetchall()
    cnxx.close()
    return render_template("sc.html",rows = rows)

@app.route('/rangesearch',methods=['POST','GET'])
def rangesearch():
    lat=request.form['lat']
    log=request.form['log']
    d=request.form['d']
    r=request.form['r']
    n=int(r)
    latf = float(lat)
    logf = float(log)
    df = float(d)
    

    latstart = str(latf-df)
    latend = str(latf+df)

    logstart = (logf-df)
    logend = (logf+df)


    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="Select top(5) id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE latitude between ? and ? and longitude between ? and ? order by mag desc"
    crsr.execute(querry,(latstart,latend,logstart,logend))
    rows = crsr.fetchall()
    cnxx.close()
    return render_template("list.html",rows = rows)



@app.route('/locsearch',methods=['POST','GET'])
def locsearch():
    m=request.form['m']
    n=request.form['n']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry1="select id,magType,net from q where latitude=(select max(latitude) from q) and magType='"+m+"' and net='"+n+"' group by magType , net,id"
    crsr.execute(querry1)
    north = crsr.fetchall()
    querry2="select id,magType,net from q where latitude=(select min(latitude) from q) and magType='"+m+"' and net='"+n+"' group by magType, net,id"
    crsr.execute(querry2)
    south = crsr.fetchall()
    
    
    count="2"
    print(count)
    cnxx.close()
    return render_template("a8.html",north = north,south=south)


@app.route('/cluster',methods=['POST','GET'])
def cluster():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="SELECT mag,COUNT(*) FROM all_month  group by mag"
    crsr.execute(querry)
    rows = crsr.fetchall()
    cnxx.close()
    return render_template("cluster.html",rows = rows)



@app.route('/nightdata',methods=['POST','GET'])
def nightdata():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    crsr.execute('SELECT COUNT(*) FROM all_month where DATEPART(HOUR,time) >=18 or DATEPART(HOUR,time) <=6 ')
    count=crsr.fetchone()
    crsr.execute('SELECT COUNT(*) FROM all_month ')
    count2=crsr.fetchone()

    display=""

    if(count[0]>(count2[0]-count[0])):
        display="Earthqakes occur more at night(6pm to 6am) than in the day,out of "+str(count2[0])+" earth quakes "+str(count[0])+" occured in the night"
    else:
        display="Earthqakes occur more at day(6am to 6pm) than in the night,out of "+str(count2[0])+" earth quakes "+str(count2[0]-count[0])+" occured in the day time"
    cnxx.close()
    return render_template("newrecord.html",display = display)


@app.route("/q7",methods=['POST','GET'])
def q7():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    time1 = request.form['t1']
    time2 = request.form['t2']
    nv = request.form['n']
    nv='%'+nv+'%'
    r = request.form['r']
    crsr.execute('update q set etime= ? where etime between ? and ? and place Like ?',(r,time1,time2,nv))
    cnxx.commit()
    dis="updates successful"
    
    return render_template('cluster.html',co=dis)
if __name__ == '__main__':
    app.debug=True
    app.run()
    