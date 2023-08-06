from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this-is-secrect'

app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql6637839'
app.config['MYSQL_PASSWORD'] = 'H4SEpRlrcf'
app.config['MYSQL_DB'] = 'sql6637839'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

INSERT_QUERY = """insert into users(name, regno, email, phoneno, password, gender) values(%s, %s, %s, %s, %s, %s)"""
SELECT_QUERY = """SELECT * FROM users where regno = %s"""

INSERT_LEAVE = """
    INSERT INTO leaverequests(name, regno, block, roomno, fromdate, todate, reason) 
    VALUES(%s, %s, %s, %s, %s, %s, %s)
"""
REJECT_LEAVE_QUERY = "UPDATE leaverequests set status='rejected' where id = %s"
APPROVE_LEAVE_QUERY = "UPDATE leaverequests set status='approved' where id = %s"

INSERT_OUTING = """
    INSERT INTO outingrequests(name, regno, block, roomno, fromdate, todate, reason) 
    VALUES(%s, %s, %s, %s, %s, %s, %s)
"""
REJECT_OUTING_QUERY = "UPDATE outingrequests set status='rejected' where id = %s"
APPROVE_OUTING_QUERY = "UPDATE outingrequests set status='approved' where id = %s"

@app.route('/')
def index():            
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        regno = request.form.get('regno')
        email = request.form.get('email')
        phoneno = request.form.get('phoneno')
        gender = request.form.get('gender')
        password1 = request.form.get('password')
        password2 = request.form.get('confirmpassword')
        
        cursor = mysql.connection.cursor()
        cursor.execute(SELECT_QUERY, (regno, ))
        
        result = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
        
        
        if result:
            flash('Regstration number already registered....')
            return redirect(url_for('register'))
        
        if password1 != password2:
            flash('password doesnot match')
            return redirect(url_for('register'))
        
        else:
            try:
                password_hash = bcrypt.generate_password_hash(password1)
                print(password_hash)
                values = (name, regno, email, phoneno, password_hash, gender)
                
                cursor = mysql.connection.cursor()
                cursor.execute(INSERT_QUERY, values)
                
                mysql.connection.commit()
                cursor.close()
                
                flash('Account created succesfully')
                return redirect(url_for('register'))
            
            except MySQLdb.IntegrityError as e:
                flash('Regstration number already registered....')
                return redirect(url_for('register'))
        
    
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('login post')
        username = request.form.get('username')
        password = request.form.get('password')
        
        cursor = mysql.connection.cursor()
        cursor.execute(SELECT_QUERY, (username, ))
        
        result = cursor.fetchone()
        
        mysql.connection.commit()
        cursor.close()
        
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin_home'))
        
        if result:
            hashed_password = result['password']
            print(hashed_password)
            if bcrypt.check_password_hash(hashed_password, password):
                # flash('Login success')
                return redirect(url_for('student_home'))
            
            else:
                flash('Invalid username or password1')
                return redirect(url_for('login'))
            
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('signin.html')

@app.route('/admin-home')
def admin_home():
    return render_template('admin/admindashboard.html')

@app.route('/student-home')
def student_home():
    return render_template('student/studentdashboard.html')

@app.route('/apply-leave', methods=['GET', 'POST'] )
def apply_leave():
    if request.method == 'POST':
        name = request.form.get('name')
        regno = request.form.get('regno')
        bname = request.form.get('bname')
        rno = request.form.get('rno')
        fromdate = request.form.get('fromdate')
        todate = request.form.get('todate')
        reason = request.form.get('reason')
        
        values = (name, regno, bname, rno, fromdate, todate, reason, )
        
        cursor = mysql.connection.cursor()
        cursor.execute(INSERT_LEAVE, values)
        mysql.connection.commit()
        cursor.close()
        
        flash('Applied for leave successfully')
        
        return redirect(url_for('apply_leave'))
    
    return render_template('student/applyleave.html')

@app.route('/leave-requests', methods=['GET', 'POST'])
def leave_requests():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM leaverequests")
    
    result = cursor.fetchall()
    print(result)
    
    mysql.connection.commit()
    cursor.close()
    
    return render_template('admin/leaverequests.html', result=result)

@app.route('/leave-status')
def leave_status():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM leaverequests")
    
    result = cursor.fetchall()
    # print(result)
    
    mysql.connection.commit()
    cursor.close()
    
    return render_template('student/leavestatus.html', result=result)

@app.route('/reject-leave/<id>')
def reject_leave(id):
    cursor = mysql.connection.cursor()
    cursor.execute(REJECT_LEAVE_QUERY, (id, ))
    mysql.connection.commit()
    cursor.close()
    
    flash('leave request rejected successfully')
    
    return redirect(url_for('leave_requests'))

@app.route('/approve-leave/<id>')
def approve_leave(id):
    cursor = mysql.connection.cursor()
    cursor.execute(APPROVE_LEAVE_QUERY, (id, ))
    mysql.connection.commit()
    cursor.close()
    
    flash('leave request approved successfully')
    
    return redirect(url_for('leave_requests'))

@app.route('/apply-outing', methods=['GET', 'POST'] )
def apply_outing():
    if request.method == 'POST':
        name = request.form.get('name')
        regno = request.form.get('regno')
        bname = request.form.get('bname')
        rno = request.form.get('rno')
        fromdate = request.form.get('fromdate')
        todate = request.form.get('todate')
        reason = request.form.get('reason')
        
        values = (name, regno, bname, rno, fromdate, todate, reason, )
        
        cursor = mysql.connection.cursor()
        cursor.execute(INSERT_OUTING, values)
        mysql.connection.commit()
        cursor.close()
        
        flash('Applied for outing successfully')
        
        return redirect(url_for('apply_outing'))
    
    return render_template('student/applyouting.html')

@app.route('/outing-requests', methods=['GET', 'POST'])
def outing_requests():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM outingrequests")
    
    result = cursor.fetchall()
    # print(result)
    
    mysql.connection.commit()
    cursor.close()
    
    return render_template('admin/outingrequests.html', result=result)

@app.route('/outing-status')
def outing_status():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM outingrequests")
    
    result = cursor.fetchall()
    # print(result)
    
    mysql.connection.commit()
    cursor.close()
    
    return render_template('student/outingstatus.html', result=result)

@app.route('/reject-outing/<id>')
def reject_outing(id):
    cursor = mysql.connection.cursor()
    cursor.execute(REJECT_OUTING_QUERY, (id, ))
    mysql.connection.commit()
    cursor.close()
    
    flash('outing request rejected successfully')
    
    return redirect(url_for('outing_requests'))

@app.route('/approve-outing/<id>')
def approve_outing(id):
    cursor = mysql.connection.cursor()
    cursor.execute(APPROVE_OUTING_QUERY, (id, ))
    mysql.connection.commit()
    cursor.close()
    
    flash('outing request approved successfully')
    
    return redirect(url_for('outing_requests'))

@app.route('/raise-complaint', methods = ['GET', 'POST'])
def raise_complaint():
    if request.method == 'POST':
        regno = request.form.get('regno')
        complaint = request.form.get('complaint')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO complaints values(%s, %s)", (regno, complaint))
        
        result = cursor.fetchall()
        # print(result)
        
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('student_home'))
    
    return render_template('student/raisecomplaint.html')

@app.route('/student-details')
def student_details():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    
    result = cursor.fetchall()
    # print(result)
    
    mysql.connection.commit()
    cursor.close()
    return render_template('admin/studentdetails.html', result=result)

@app.route('/complaint-details')
def complaint_details():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM complaints")
    
    result = cursor.fetchall()
    # print(result)
    
    mysql.connection.commit()
    cursor.close()
    return render_template('admin/complaints.html', result=result)


@app.route('/dispaly-image/<filename>')
def display_image(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
