# coding = UTF-8
from flask import Flask, request
import os

c_lst = [[] for i in range(8)]
ID = []
ary = ["Service", "Quantity", "Delicious", "Price", "Environment", "Transportation", "Mood", "Others"] 

app = Flask(__name__)

def wrapper (ins):
    s = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>IR Final Project</title>
    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">

  </head>
  <body>
    %s

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""
    s = s % ins
    return s

def menu(idx):
    s = """
<nav class="navbar navbar-inverse">
<div class="container">

<div class="navbar-header">
<a class="navbar-brand" href="/">IR Finals</a>
</div>
"""
    s += """
<div class="navbar-collapse collapse">
<ul class="nav navbar-nav">
"""
    url = "/category/"

    for i in range(len(ary)):
        option = ""
        if i == idx :
            option = "class = active"
        s += '<li %s><a href="%s%d">%s</a></li>' % ( option, url, i, ary[i] )

    s += """
</ul>
</div>
"""
    s += """
</div>
</nav>
"""
    return s

def text(i, each):
    # auther and subject 
    s = """
    <div class= "panel panel-default"> 
        <div class= "panel-heading"> 
            <h3 class= "panel-title"> %s </br> %s </br> 
            </h3>
        </div>
    """ % (ID[i][0], ID[i][1])
    
    # body
    s += '<div class = "panel-body">'
    size = len(each)
    for j in range(size):
        s += " " + each[j] + "</br>"
    s += "</br>Total : %d </br>" % size
    s += "</div></div>"
    return s


def execute (q):
    with open("temp.txt", "w") as f:
        f.write(q)

    # TODO

    with open("result.txt", "r") as f:
        res = f.read()

    return parse_result(res)

    
    
@app.route("/search", methods=['POST'])
def search():
    q = request.form['q']
    q = q.encode('utf-8')

    s = menu(-1)

    s += '<div class="container">'

    # execute
    title, author, res = execute(q)
    
    # HTML
    for idx in range(len(res)):
        s += """
            <div class = "panel panel-info">
                <div class = "panel-heading">
                    <h3 class = "panel-title"> %s </h3>
                </div>
                <div class = "panel-body">
            """ % ary[idx]

        if len(res[idx]) != 0:
            for x in res[idx] :
                s += x + "</br>"
       
        s += "</br>Total : " + str(len(res[idx])) + "</br>"
        s += '</div></div>'
    s += '</div>'
    
    return wrapper(s)


@app.route("/")
def homepage():
    q = ''

    s = menu(-1)

    s += '<div class="container">'

    # form
    s += """
<form role="form" action="/search" method="POST">

<div class="form-group">
    <textarea class="form-control" name="q" rows="10" value="%s"></textarea>
</div>

<button type="submit" class="btn btn-default">Submit</button>

</form>
""" % q
        
    s += '</div>'
    
    return wrapper(s)


@app.route("/category/<int:idx>")
def category(idx):
    s = menu(idx)

    #sort
    order = []
    for i, each in enumerate(c_lst[idx]):
        order.append((len(each), i))
    order = sorted(order, reverse=True)
    #text
    s += '<div class="container">'
    for lenth, i in order :
        if lenth == 0:
            continue
        s += text( i, c_lst[idx][i] )
    s += '</div>'

    return wrapper(s)


def parse_result(s, article=False):
    t_split = s.split("\n")
    t_split = [i for i in t_split if i != ""]
    
    if article:
        author, title = t_split[0][2:], t_split[1][2:]
        t_split = t_split[2:]
    else:
        author, title = None, None
    
    tmp = [[] for i in range(8)]
    for line in t_split:
        #get which catecory
        tmpt = line[0: line.find(" ")]
        tmpt = tmpt.split(",")
            
        #get the string 
        ss = line[line.find(" ")+1:]
        
        #put the string to the correct
        for x in tmpt :
            tmp[int(x)-1].append(ss)


    # return title, author, category_list
    return title, author, tmp


def pre_process (name):
    with open(name, "r") as f:
        s = f.read()

    if s == '':
        return


    title, author, res = parse_result(s, article=True)
    
    ID.append((author, title))

    # put into c_lst
    for i in range(8):
        c_lst[i].append(res[i])
    

if __name__ == "__main__" :
    path = "../training/training_train/"
    files = os.listdir(path)
    files.sort()
    files = [x for x in files if x[0] != '.']

    # pro_process each file
    for x in files :
        pre_process(path + "/" + x)

    #run the server
    app.run(host="0.0.0.0")
    
