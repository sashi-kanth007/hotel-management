#app.py
from html.entities import codepoint2name
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "hotel2"
DB_USER = "postgres"
DB_PASS = "password12345"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addcolumn',methods=['GET', 'POST'])
def addcolumn():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'Tname' in request.form and 'Cname' in request.form and 'Dtype' in request.form:
        table = request.form['Tname']
        column = request.form['Cname']
        dtype = request.form['Dtype']

        cursor.execute('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=%s',(table,))
        account = cursor.fetchone()

        cursor.execute('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=%s and column_name=%s',(table.lower(),column.lower()))
        acc = cursor.fetchone()

        if not account:
            flash('Table doesnot exist!!')
        elif acc:
            flash('Column already exists!!')
        else:
            #s1= 'ALTER TABLE '+table+' ADD COLUMN '+column
            # cursor.execute(f'ALTER TABLE %s ADD COLUMN %s',(table,column,))
            cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {dtype}')
            #cursor.execute ('ALTER {{table}} ALTER COLUMN {{column}} TYPE {{dtype}}')
            conn.commit()
            return render_template('common.html')

    return render_template('addcolumn.html')

@app.route('/hotelcity',methods=['GET', 'POST'])
def hotelcity():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'search' in request.form:
        search = request.form['search']
        cursor.execute('SELECT hotel_name FROM HOTEL WHERE hotel_city ilike %s',(search,))
        hotels = cursor.fetchall()
        print(hotels)
        conn.commit()
        return render_template('hotelcity.html',  hotel = hotels)

    return render_template('hotelcity.html')



@app.route('/changenum',methods=['GET', 'POST'])
def changenum():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'Aadhar' in request.form and 'Pno' in request.form:
        Aadharnumber = request.form['Aadhar']
        Phonenumber = request.form['Pno']

        cursor.execute('SELECT * FROM Customer_ContactNumber WHERE contact_number=%s',(int(Phonenumber),))
        account = cursor.fetchone()

        cursor.execute('SELECT * FROM Customer WHERE aadhar_number=%s',(Aadharnumber,))
        ac1 = cursor.fetchone()

        if (account):
            flash('Number already exists')
        elif not ac1:
            flash('Customer doesnot exist!')
        elif not Aadharnumber or not Phonenumber:
            flash('Please fill the form!!!')
        else:
            cursor.execute('INSERT INTO Customer_ContactNumber VALUES (%s,%s)',(Phonenumber,Aadharnumber))
            conn.commit()
            return render_template('common.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('changenum.html')

@app.route('/Hotel',methods=['GET', 'POST'])
def Hotel():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'Hotelname' in request.form and 'Adminid' in request.form:
        hotelname = request.form['Hotelname']
        street = request.form['Hotelstreet']
        city = request.form['Hotelcity']
        postal = request.form['Hotelpostal']
        contact = request.form['Hotelcontact']
        adminid = request.form['Adminid']

        cursor.execute('SELECT * FROM Hotel ORDER BY hotel_id DESC LIMIT 1')
        hotelid = cursor.fetchone()
        if hotelid:

            cursor.execute('SELECT * FROM Administrator where admin_id=%s',(int(adminid),))
            adid=cursor.fetchone()

            if not hotelname or not adminid:
                flash('Please fill out the form!')
            elif not adid:
                print("I AM AID")

                flash('Admin is not there!!')
            else:
                cursor.execute("INSERT INTO Hotel (hotel_name,hotel_street,hotel_city,hotel_postalcode,admin_id) VALUES (%s,%s,%s,%s,%s)",(hotelname,street,city,postal,adminid))
                cursor.execute('SELECT * FROM Hotel ORDER BY hotel_id DESC LIMIT 1')
                hid = cursor.fetchone()
                if (contact):
                    cursor.execute('INSERT INTO Hotel_HotelContactNumber VALUES (%s,%s)',(contact,hid['hotel_id'],))
                cursor.execute("SELECT * FROM Hotel WHERE hotel.hotel_id=%s",(hid['hotel_id'],))
                account = cursor.fetchone()
                cursor.execute('SELECT * FROM Administrator_PhoneNumber WHERE admin_id=%s',(adminid,))
                adminphone = cursor.fetchone()
                conn.commit()
                return render_template('hotelprofile.html',account = account,admin = adminphone)
        else:
            cursor.execute('SELECT * FROM Administrator where admin_id=%s',(adminid,))
            adid=cursor.fetchone()

            if not hotelname or not adminid:
                flash('Please fill out the form!')
            elif not adid:
                print("I AM AID")
                flash('Admin is not there!!')
            else:
                cursor.execute("INSERT INTO Hotel (hotel_name,hotel_street,hotel_city,hotel_postalcode,admin_id) VALUES (%s,%s,%s,%s,%s)",(hotelname,street,city,postal,adminid))
                cursor.execute('SELECT * FROM Hotel ORDER BY hotel_id DESC LIMIT 1')
                hid = cursor.fetchone()
                if (contact):
                    cursor.execute('INSERT INTO Hotel_HotelContactNumber VALUES (%s,%s)',(contact,hid['hotel_id'],))
                cursor.execute("SELECT * FROM Hotel WHERE hotel.hotel_id=%s",(hid['hotel_id'],))
                account = cursor.fetchone()
                cursor.execute('SELECT * FROM Administrator_PhoneNumber WHERE admin_id=%s',(adminid,))
                adminphone = cursor.fetchone()
                conn.commit()
                return render_template('hotelprofile.html',account = account,admin = adminphone)


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('Hotel.html')

@app.route('/hotelprofile',methods=['GET', 'POST'])
def hotelprofile():
    return render_template('hotelprofile.html')

@app.route('/Admin', methods=['GET', 'POST'])
def Admin():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'AdminFname' in request.form and 'Adminemail' in request.form:
        firstname = request.form['AdminFname']
        lastname = request.form['AdminLname']
        email = request.form['Adminemail']
        contact = request.form['Admincontact']

        cursor.execute('SELECT * FROM Administrator ORDER BY admin_id DESC LIMIT 1')
        adminid = cursor.fetchone()
        if adminid:
            cursor.execute('SELECT * FROM Administrator WHERE email_admin=%s',(email,))
            account=cursor.fetchone()

            if (account):
                flash('Admin already exists')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not firstname or not email:
                flash('Please fill out the form!')
            else:
                cursor.execute("INSERT INTO Administrator (Email_admin,first_name,last_name) VALUES (%s,%s,%s)",(email,firstname,lastname))
                cursor.execute('SELECT * FROM Administrator ORDER BY admin_id DESC LIMIT 1')
                adminid = cursor.fetchone()
                if (contact):
                    cursor.execute('INSERT INTO Administrator_PhoneNumber VALUES (%s,%s)',(contact,adminid['admin_id']))
                cursor.execute("SELECT * FROM Administrator WHERE administrator.admin_id=%s",(adminid['admin_id'],))
                account = cursor.fetchone()
                conn.commit()
                return render_template('adminprofile.html',account = account)
        else:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not firstname or not email:
                flash('Please fill out the form!')
            else:

                cursor.execute("INSERT INTO Administrator (Email_admin,first_name,last_name) VALUES (%s,%s,%s)",(email,firstname,lastname))
                cursor.execute('SELECT * FROM Administrator ORDER BY admin_id DESC LIMIT 1')
                adminid = cursor.fetchone()
                if (contact):
                    cursor.execute('INSERT INTO Administrator_PhoneNumber VALUES (%s,%s)',(contact,adminid['admin_id']))
                cursor.execute("SELECT * FROM Administrator WHERE administrator.admin_id=%s",(adminid['admin_id'],))
                account = cursor.fetchone()
                conn.commit()
                return render_template('adminprofile.html',account = account)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')

    return render_template('Admin.html')

@app.route('/adminprofile',methods=['GET', 'POST'])
def adminprofile():
    return render_template('adminprofile.html')

@app.route('/amenities',methods=['GET', 'POST'])
def amenities():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'Amenname' in request.form and 'Hotelid' in request.form:
        amenname = request.form['Amenname']
        starttime = request.form['Stime']
        endtime = request.form['Etime']
        hotelid = request.form['Hotelid']

        cursor.execute('SELECT * FROM Hotel WHERE hotel_id=%s',(hotelid,))
        account = cursor.fetchone()
        print(account)

        cursor.execute('SELECT * FROM Amenities WHERE amen_name=%s and hotel_id=%s',(amenname,hotelid))
        acc = cursor.fetchone()

        if not account:
            flash('Hotel doesnot exist!!')
        elif acc:
            flash('Amenity already exists')
        else:
            cursor.execute('INSERT INTO Amenities VALUES (%s,%s,%s,%s)',(amenname,starttime,endtime,hotelid))
            cursor.execute('SELECT * FROM Amenities WHERE hotel_id=%s and amen_name=%s',(hotelid,amenname))
            account = cursor.fetchone()
            conn.commit()
            return render_template('amenityprofile.html',account = account)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('amenities.html')

@app.route('/amenityprofile',methods=['GET', 'POST'])
def amenityprofile():
    return render_template('amenityprofile.html')

@app.route('/customerprofile',methods=['GET', 'POST'])
def customerprofile():
    return render_template('customerprofile.html')

@app.route('/customer/', methods=['GET', 'POST'])
def customer():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'Firstname' in request.form and 'Aadharnumber' in request.form and 'Age' in request.form:
        firstname = request.form['Firstname']
        middlename = request.form['Middlename']
        lastname = request.form['Lastname']
        email = request.form['Email']
        contact = request.form['Contactnumber']
        contact1 = request.form['Cnumber']
        aadhar = request.form['Aadharnumber']
        age = request.form['Age']
        postalcode = request.form['Postalcode']
        city = request.form['City']
        street = request.form['street']

        cursor.execute('SELECT * FROM Customer WHERE Aadhar_Number = %s', (aadhar,))
        account = cursor.fetchone()
        print(account)
        cursor.execute("SELECT * FROM Customer_ContactNumber WHERE contact_number = %s ",(int(contact),))
        contactexists = cursor.fetchone()
        
        if account:
            flash('Customer already exists!')
        elif (contactexists):
            flash('Contact number-1 already exists!!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not aadhar or not firstname or not age:
            flash('Please fill out the form!')
        else:
            if (contact1):
                cursor.execute("SELECT * FROM Customer_ContactNumber WHERE contact_number = %s ",(int(contact1),))
                contact1exists = cursor.fetchone()
                if (contact1exists):
                    flash('Contact number-2 already exists!!')
                    return render_template('customer.html')

            cursor.execute("INSERT INTO Customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(aadhar,age,firstname,middlename,lastname,postalcode,street,city,email))
            
            if (contact and contact1):
                cursor.execute("INSERT INTO Customer_ContactNumber VALUES (%s,%s)",(contact,aadhar))
                cursor.execute("INSERT INTO Customer_ContactNumber VALUES (%s,%s)",(contact1,aadhar))
            elif (contact):
                cursor.execute("INSERT INTO Customer_ContactNumber VALUES (%s,%s)",(contact,aadhar))
            cursor.execute("SELECT * FROM customer WHERE customer.aadhar_number=%s",(aadhar,))
            account = cursor.fetchone()
            conn.commit()
            return render_template('customerprofile.html',account = account)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('customer.html')
    

if __name__ == "__main__":
    app.run(debug=True)