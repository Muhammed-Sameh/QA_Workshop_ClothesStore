import db
from flask import Flask, render_template, request, redirect, url_for, session,flash
import sqlite3
import os

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")
    return filename


@app.route('/Client Home')
def clientMain():
    connect = db.get_db()
    cursor = connect.cursor()

    sql_fetch_blob_query = """SELECT id from product"""
    cursor.execute(sql_fetch_blob_query)
    record = cursor.fetchall()
     
    connect.commit()
    cursor.close()

    con = db.get_db()
   
    cur = con.cursor()
    cur.execute("select * from product")
   
    rows = cur.fetchall()
                

    return render_template("client_main.html",rows = rows, active_page='client_main')

@app.route('/Client Accessories')
def clientAccessories():
    connect = db.get_db()
    cursor = connect.cursor()

    sql_fetch_blob_query = """SELECT id from product where name like 'A%'"""
    cursor.execute(sql_fetch_blob_query)
    record = cursor.fetchall()
     
    connect.commit()
    cursor.close()

    con = db.get_db()
   
    cur = con.cursor()
    cur.execute("select * from product where name like 'A%'")
   
    rows = cur.fetchall()
            
    return render_template("client_accessories.html",rows = rows, active_page='client_main')

@app.route('/Client Clothes')
def clientClothes():
    connect = db.get_db()
    cursor = connect.cursor()

    sql_fetch_blob_query = """SELECT id from product where name Not like 'A%'"""
    cursor.execute(sql_fetch_blob_query)
    record = cursor.fetchall()
     
    connect.commit()
    cursor.close()

    con = db.get_db()
   
    cur = con.cursor()
    cur.execute("select * from product where name Not like 'A%'")
   
    rows = cur.fetchall()
            
    return render_template("client_clothes.html",rows = rows, active_page='client_main')


@app.route('/')
def loginPage():
    return render_template('login.html', msg = "")

@app.route('/about')
def aboutPage():
    return render_template('about.html', active_page='about')

@app.route('/contact')
def contactPage():
    return render_template('contact.html', active_page='contact')

@app.route('/empty_transaction')
def emptyTransactionPage():
    return render_template('empty_transaction.html')


###**************** Log In Page ***********************
@app.route('/login', methods=['GET', 'POST'])
def LoginPage():
    
    r=""   
    if request.method == 'POST':
        if ( request.form['email'] != "" and request.form['password'] != ""):
            email = request.form['email']
            password = request.form['password']
            
            connect = db.get_db()
            c = connect.cursor()
            print("Email Not empty")
            c.execute("SELECT * FROM users WHERE email = ? AND password = ?" ,(email, password))
            print("Query Not empty")

            #connect.commit()
            account = c.fetchone()
            if account:
                session['logged_in'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                msg = "Logged in successfully !"
                #clientMain()
                return redirect(url_for("clientMain"))
                #return render_template('client_main.html')
            else:
                msg = 'Incorrect email or password !'
        return render_template('login.html', msg = msg)
           
    
###**************** Sign Up Page ***********************
@app.route('/signup', methods=['GET', 'POST'])
def SignupPage():
    msg=""
    if request.method == 'POST' and request.form['name'] != "" and request.form['email'] != "" and request.form['password'] != "" and request.form['phone_number'] != "" and request.form['role'] != "":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        connect = db.get_db()
        c = connect.cursor()
        c.execute("SELECT * FROM users WHERE name = ?", (name))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists !"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid email address !"
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = "Username must contain only characters and numbers !"
        elif not name or not password or not email:
            msg = "Please fill out the form !"
        else:
            c.execute("INSERT INTO users (name, email, password, phone_number, role) VALUES (?, ?, ?, ?, ?)" ,(name, email, password, phone_number, role))
            connect.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for("clientMain"))

    elif request.method == 'POST':
        msg = "Please fill out the form !"
    
    return render_template('signup.html', msg = msg)

        

@app.route('/search', methods=['GET','POST'])
def search():
    
    if request.method == 'POST':
        if (request.form['search'] != ""):

            search = request.form['search']
            
            connect = db.get_db()
            c = connect.cursor()
            c.execute("select * from product where name = ?" ,(search,))
            result = c.fetchall()
            
            db.close_db(connect)
    return render_template("search.html", record = result)


###*************** Client Add to Cart Page *****************************

@app.route('/clientAddToCart/<string:name>', methods=['GET', 'POST'])
def clientAddToCart(name = None):
    if request.method == 'POST':
        name = request.form['name'] 
    
    cur1 = db.get_db().cursor()
    cur1.execute(f"select * from buy where product = ?", (name,))
    data = cur1.fetchall()

    cur = db.get_db().cursor()
    cur.execute(f"select * from product where name = ?", (name,))
    row = cur.fetchone()

    return render_template('client_add_to_cart.html', row = row, data = data)    

###*************** client Buy A Product Page *****************************
'''@app.route('/clientBuyProduct/<string:name>', methods=['GET', 'POST'])
def clientBuyProduct(name = None):
    if request.method == 'POST':
        name = request.form['name'] 
    
    cur1 = db.get_db().cursor()
    cur1.execute(f"select * from buy where product = ?", (name,))
    data = cur1.fetchall()

    cur = db.get_db().cursor()
    cur.execute(f"select * from product where name = ?", (name,))
    row = cur.fetchone()

    return render_template('client_add_to_cart.html', row = row, data = data)    
'''
  


@app.route('/Add_comment', methods=['GET', 'POST'])
def Add_comment():
    
    if request.method == 'POST':

        if (request.form['name'] != "" and request.form['email'] != "" and request.form['comment'] != "" and session['logged_in'] == True):
            name = request.form['name']
            email = request.form['email']
            comment = request.form['comment']
            connect = db.get_db()
            c = connect.cursor()

            c.execute("INSERT INTO comment (name, email, comment_text) VALUES (?, ?, ?)" ,(name, email, comment))
            connect.commit()

            cur = db.get_db().cursor()
            cur.execute(f"select * from product where name = ?", (name,))
            row = cur.fetchone()

            cur = db.get_db().cursor()
            cur.execute(f"select * from comment where movie_name = ?", (name,))
            data = cur.fetchall()

            db.close_db(connect)

            return render_template('Browse_movie.html', row = row, data = data)
        
        return render_template('Add_comment.html', msg = "*** Please Full All Fields ***")    

    return render_template('Add_comment.html')    


@app.route('/Add_favorite', methods=['GET', 'POST'])
def Add_favorite():
    if request.method == 'POST' and session['logged_in'] == True:

        if (request.form['favorite_movie'] != "" and request.form['email'] != ""):
            name = request.form['favorite_movie']
            email = request.form['user_email']
            
            connect = db.get_db()
            c = connect.cursor()

            c.execute("INSERT INTO favorite (movie_name, user_email) VALUES (?, ?)" ,(name, email))
            connect.commit()

            cur = db.get_db().cursor()
            cur.execute(f"select * from product where name = ?", (name,))
            row = cur.fetchone()

            '''cur = db.get_db().cursor()
            cur.execute(f"select * from favorite where movie_name = ?", (name,))
            data = cur.fetchall()'''

            db.close_db(connect)

            return render_template('Browse_movie.html', row = row)

        return render_template('Add_favorite.html', msg = "*** Please Full All Fields ***")    


    return render_template('Add_favorite.html')    


@app.route('/favorite_list')
def favorite_list():
    if session['logged_in'] == True:
        con = db.get_db()
    
        cur = con.cursor()
        cur.execute("select * from favorite where user_email = ?", (session['email'], ))
    
        row = cur.fetchall()
                
        return render_template("favoriteList.html",row = row)


@app.route('/admin', methods=['GET', 'POST'])
def delClientAccount():
    if request.method == 'POST':
        if request.form['phone_number'] and request.form['password']:
            phone = request.form['phone_number']
            password = request.form['password']
            
            connect = db.get_db()
            c = connect.cursor()

            c.execute("DELETE FROM users WHERE phone_number = ? AND password = ?", (phone, password))
            connect.commit()

            if c.rowcount > 0:
                # Deletion was successful
                db.close_db(connect)
                return render_template('adminPage.html', msg = "Client's data is deleted successfully")
            else:
            # No account matched the provided information
                db.close_db(connect)
                return render_template('adminPage.html', msg="Please, check your information and try again")
            
    return render_template('adminPage.html')


@app.route('/delete_accessories', methods=['GET', 'POST'])
def deleteAccessories():
    if request.method == 'POST':
        if request.form['phone_number'] and request.form['password']:
            phone = request.form['phone_number']
            password = request.form['password']
            
            connect = db.get_db()
            c = connect.cursor()

            c.execute("DELETE FROM users WHERE phone_number = ? AND password = ?", (phone, password))
            connect.commit()

            if c.rowcount > 0:
                # Deletion was successful
                db.close_db(connect)
                return render_template('adminPage.html', msg = "Client's data is deleted successfully")
            else:
            # No account matched the provided information
                db.close_db(connect)
                return render_template('adminPage.html', msg="Please, check your information and try again")
            
    return render_template('adminPage.html')



@app.route('/LogOut')
def LogOut():
    #session.clear()
    #return redirect(url_for("clientMain"))
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('LoginPage'))


if __name__ == "__main__":
    app.run(debug=True)
