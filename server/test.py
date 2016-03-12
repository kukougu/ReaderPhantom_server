# -*- coding:utf-8 -*-
#from recommend import recommend
from hello import rec
from flask import Flask,request,jsonify,render_template
from manage import *
import random as jayrand
import simplejson as json
app = Flask(__name__)

@app.route('/')
def welcome():
    
    return 'Welcome to ReaderPhantom'

@app.route('/regist',methods=['POST'])
def regist():
    form=request.form
    musername = form['username']
    mpassword = form['password']
    u = str(musername)
    p = str(mpassword)
    con = Connect()
    query = 'select * from users u where username=%s'
    param = (u)
    result = Exec(con, query, param)
    if len(result) != 0:
        return jsonify(success=False,msg=u'The username existed, please input another')
    else:
        con = Connect()
        query = 'insert into users values(%s,%s,%s,%s,%s)'
        param = (u, p, "--", "--", "--")
        result = Exec(con, query, param)
        return jsonify(success=True,msg=u'Regist successful!')




@app.route('/login',methods=['POST'])
def login():
    form=request.form
    musername = form['username']
    mpassword = form['password']
    u = str(musername)
    p = str(mpassword)
    con = Connect()
    query = 'select * from users u where username=%s'
    param = (u)
    result = Exec(con, query, param)

    if len(result) != 0 and str(result[0][1]) == p:
        return jsonify(success=True,msg=u'Login successful!')
    else:
        return jsonify(success=False,msg=u'password error')

@app.route('/addrecommend', methods=['POST'])
def addrecommend():
    form = request.form
    userid = int(form['userid'])
    result = rec(userid)[1:]
    count = 0
    jsonStr = []
    for item in result:
        temp = str(result[count][0])
        if len(temp) == 9: ISBN = str('0'+temp)
        elif len(temp) == 8: ISBN = str('00'+temp)
        elif len(temp) == 7: ISBN = str('000'+temp)
        else : ISBN = temp

        con = Connect()
        query = 'select * from `BX-Books` where ISBN=%s'
        param = (ISBN)
        result2 = Exec(con, query, param)
        if len(result2) == 0:
            continue
        bookname = str(result2[0][1])
        mauthor = str(result2[0][2])
        imageUrl = str(result2[0][6])
        jsonStr0 = {'ISBN':ISBN, 'bookname':bookname, 'author':mauthor, 'imageUrl':imageUrl}
        jsonStr.append(jsonStr0)
        count = count + 1
    
    return json.dumps(jsonStr)



@app.route('/addtouser',methods=['POST'])
def addtouser():
    form=request.form
    musername = form['username']
    msex = form['sex']
    mphone = form['phone']
    mstar = form['star']

    username = str(musername)
    sex = str(msex)
    phone = str(mphone)
    star = str(mstar)

    con = Connect()
    query = 'update users set sex=%s, phone=%s, star=%s where username=%s'
    param = (sex, phone, star, username)
    result = Exec(con, query, param)

    return jsonify(success=True)

@app.route('/getusermessage', methods=['POST'])
def getusermessage():
    form=request.form
    musername = form['username']
    username = str(musername)
    
    con = Connect()
    query = 'select * from users where username=%s'
    param = (username)
    result = Exec(con, query, param)
    msex = result[0][2]
    mphone = result[0][3]
    mstar = result[0][4]
    return jsonify(sex=msex, phone=mphone, star=mstar)

@app.route('/getinsterest',methods=['POST'])
def getinsterest():
    form=request.form
    musername = form['username']
    u = str(musername)
    con = Connect()
    query = 'select * from insterest where username=%s'
    param = (u)
    result = Exec(con, query, param)
    jsonStr = []

    for count in range(3):
    	ISBN = str(result[count][1])
    	query = 'select * from `BX-Books` where ISBN=%s'
    	param = (ISBN)
    	result2 = Exec(con, query, param)
        bookname = str(result2[0][1])
        mauthor = str(result2[0][2])
    	imageUrl = str(result2[0][6])
    	jsonStr0 = {'ISBN':ISBN, 'bookname':bookname, 'author':mauthor, 'imageUrl':imageUrl}
    	jsonStr.append(jsonStr0)

    return json.dumps(jsonStr)




@app.route('/getmyhistory',methods=['POST'])
def getmyhistory():
    form = request.form
    musername = form['username']
    u = str(musername)
    con = Connect()
    query = 'select * from history where username=%s'
    param = (u)
    result = Exec(con, query, param)
    count = 0
    jsonStr = []
    for item in result:
        ISBN = str(result[count][1])
        mtime = str(result[count][3])
        query = 'select * from `BX-Books` where ISBN=%s'
        param = (ISBN)
        result2 = Exec(con, query, param)
        bookname = str(result2[0][1])
        mauthor = str(result2[0][2])
        imageUrl = str(result2[0][6])
        jsonStr0 = {'ISBN':ISBN, 'bookname':bookname, 'author':mauthor, 'imageUrl':imageUrl, 'time':mtime}
        jsonStr.append(jsonStr0)
        count = count + 1

    return json.dumps(jsonStr)


@app.route('/addtohistory',methods=['POST'])
def addtohistory():
    form=request.form
    musername = form['username']
    mISBN = form['ISBN']
    mscore = form['score']
    mtime0 = form['time']

    username = str(musername)
    ISBN = str(mISBN)
    score = str(mscore)
    mtime = str(mtime0)

    con = Connect()
    query = 'select * from history where username=%s and ISBN=%s'
    param = (username, ISBN)
    result = Exec(con, query, param)
    if len(result) == 0:
        con = Connect()
        query = 'insert into history values(%s,%s,%s,%s)'
        param = (username, ISBN, score, mtime)
        result2 = Exec(con, query, param)

    else :
        query = 'update history set score=%s, time=%s where username=%s and ISBN=%s'
        param = (score, mtime, username, ISBN)
        result2 = Exec(con, query, param)

    return jsonify(success=True)






@app.route('/getbookslib',methods=['POST'])
def getbookslib():
    form=request.form
    musername = form['request']
    #mindex_min = int(musername)
    mindex_min = jayrand.randint(0,20)
    #mindex_min = 0
    mindex_max = mindex_min+50
    str_min = str(mindex_min)
    str_max = str(mindex_max)
    con = Connect()
    query = 'select * from `BX-Books` limit %s,%s' % (str_min, str_max)
    #param = (mindex, mindex+100)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    #result = Exec(con, query, param)
    count = 0
    jsonStr = []

    for item in result:
        ISBN = str(result[count][0])
        bookname = str(result[count][1])
        mauthor = str(result[count][2])
        imageUrl = str(result[count][6])
        
        jsonStr0 = {'ISBN':ISBN, 'bookname':bookname, 'author':mauthor, 'imageUrl':imageUrl}
        jsonStr.append(jsonStr0)
        count = count + 1

    return json.dumps(jsonStr)


@app.route('/getonebook',methods=['POST'])
def getonebook():
    form=request.form
    ISBN = form['ISBN']
    u = str(ISBN)
    con = Connect()
    query = 'select * from `BX-Books` where ISBN=%s'
    param = (u)
    result = Exec(con, query, param)

    ISBN = str(result[0][0])
    bookname = str(result[0][1])
    mauthor = str(result[0][2])
    imageUrl = str(result[0][6])
    jsonStr0 = {'ISBN':ISBN, 'bookname':bookname, 'author':mauthor, 'imageUrl':imageUrl}

    return json.dumps(jsonStr0)



@app.route('/addtocomment',methods=['POST'])
def addtocomment():
    form=request.form
    musername = form['username']
    mISBN = form['ISBN']
    mcontent = form['content']
    mtime0 = form['time']

    username = str(musername)
    ISBN = str(mISBN)
    content = str(mcontent)
    mtime = str(mtime0)

    con = Connect()
    query = 'insert into comment values(%s,%s,%s,%s)'
    param = (username, ISBN, content, mtime)
    result = Exec(con, query, param)
    
    return jsonify(success=True)


@app.route('/getcomment',methods=['POST'])
def getcomment():
    form=request.form
    mISBN = form['ISBN']
    
    ISBN = str(mISBN)
    
    con = Connect()
    query = 'select * from comment where ISBN=%s'
    param = (ISBN)
    result = Exec(con, query, param)
    count = 0
    jsonStr = []

    for item in result:
        username = str(result[count][0])
        
        content = str(result[count][2])
        time = str(result[count][3])
        
        jsonStr0 = {'username':username, 'content':content, 'time':time}
        jsonStr.append(jsonStr0)
        count = count + 1

    return json.dumps(jsonStr)






if __name__ == '__main__':
    app.run()

