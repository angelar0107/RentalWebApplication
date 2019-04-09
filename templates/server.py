#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, Response, redirect, url_for, session, flash
from werkzeug.security import check_password_hash,generate_password_hash
from config import *

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'key'

USER = "yw3152"
PASSWORD = "reganmian"

DATABASEURI = "postgresql://"+ USER + ":" + PASSWORD +"@"+ "34.73.21.127/proj1part2"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/tenant_base')
def tenant_base():
    return render_template('tenantbase.html')

@app.route('/landlord_base')
def landlord_base():
    return render_template('landlordbase.html')


@app.route('/landlord_signup', methods=['GET','POST'])
def landlord_signup():
    error = None
    if session.get('logged_in') == True:
        return redirect(url_for('landlord_base'))

    if request.method == 'POST':
        email = request.form['lusername']
        password = request.form['lpassword']
        name = request.form.get('lname')
        phone = request.form.get('lphone')
        gender = request.form['lgender']
        age = request.form['lage']

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif g.conn.execute(
            '''SELECT landlord_id FROM landlords WHERE email = '{}';'''.format(email)
        ).fetchone() is not None:
            return render_template('landlordbase.html',
                                   error='This email has already been registered.')

        cursor = g.conn.execute(
          "SELECT max(landlord_id) FROM landlords"
        )
        landlord_id = cursor.fetchone()[0] + 1

        if error is None:
            g.conn.execute(
                '''INSERT INTO landlords (landlord_id, email, gender, name, phone, age, password ) VALUES ({0}, '{1}', '{2}','{3}','{4}',{5},'{6}')'''.format(
                    landlord_id, email, gender, name, phone, age, generate_password_hash(password))
                )
            flash('User created successfully, please login')
            return redirect(url_for('landlord_login'))

    return render_template('landlordsignup.html')

@app.route('/landlord_login', methods=['GET','POST'])
def landlord_login():
    error = None
    session.permanent = False
    if session.get('logged_in') == True:
      return redirect(url_for('landlord_base'))

    if request.method == 'POST':
      email = request.form['lusername']
      password = request.form['lpassword']

      landlord = g.conn.execute(
            '''SELECT * FROM landlords WHERE email = '{}';'''.format(email)
        ).fetchone()

      if landlord is None:
          error = 'Invalid username'
      elif not check_password_hash(landlord['password'], password):
          error = 'Incorrect password.'

      if error is None:
        session['logged_in'] = True
        session['id'] = landlord['landlord_id']
        session['landlord'] = True
        return redirect(url_for('landlord_base'))
    return render_template('landlordlogin.html', error=error)


@app.route('/tenant_signup', methods=['GET','POST'])
def tenant_signup():
    error = None
    if session.get('logged_in') == True:
        return redirect(url_for('tenant_base'))

    if request.method == 'POST':
        email = request.form['tusername']
        password = request.form['tpassword']
        name = request.form.get('tname')
        phone = request.form.get('tphone')
        gender = request.form['tgender']
        age = request.form['tage']

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif g.conn.execute(
            '''SELECT tenant_id FROM tenants WHERE email = '{}';'''.format(email)
        ).fetchone() is not None:
            return render_template('tenantbase.html',
                                   error='This email has already been registered.')

        cursor = g.conn.execute(
          "SELECT max(tenant_id) FROM tenants"
        )
        tenant_id = cursor.fetchone()[0] + 1

        if error is None:
            g.conn.execute(
                '''INSERT INTO tenants (tenant_id, email, gender, name, phone, age, password ) VALUES ({0}, '{1}', '{2}','{3}','{4}',{5},'{6}')'''.format(
                    tenant_id, email, gender, name, phone, age, generate_password_hash(password))
                )
            flash('User created successfully, please login')
            return redirect(url_for('tenant_login'))
    return render_template('tenantsignup.html')

@app.route('/tenant_login', methods=['GET','POST'])
def tenant_login():
    error = None
    session.permanent = False
    if session.get('logged_in') == True:
      return redirect(url_for('tenant_base'))

    if request.method == 'POST':
      email = request.form['tusername']
      password = request.form['tpassword']

      tenant = g.conn.execute(
            '''SELECT * FROM tenants WHERE email = '{}';'''.format(email)
        ).fetchone()

      if tenant is None:
          error = 'Invalid username'
      elif not check_password_hash(tenant['password'], password):
          error = 'Incorrect password.'

      if error is None:
        session['logged_in'] = True
        session['id'] = tenant['tenant_id']
        session['tenant'] = True
        return redirect(url_for('tenant_base'))
    return render_template('tenantlogin.html', error=error)

@app.route('/logout')
def logout():
    session['tenant'] = False
    session['landlord'] = False
    session['id'] = None
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/editoffer/landlord', methods=['GET','POST'])
def editoffer():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('landlord_login'))
    landlord_id = session.get('id')

    live_in = []
    cursor = g.conn.execute(
        "SELECT price,type,size,house_number,building_id FROM apartment_belong where apartment_id in (select apartment_id from offer where landlord_id = {})".format(landlord_id)
    ).fetchall()
    all_avl = g.conn.execute(
        "SELECT availability FROM offer where apartment_id in (select apartment_id from offer where landlord_id = {})".format(landlord_id)
    ).fetchall()

    for result in cursor:
        live_in.append(result)
    for i in range(len(live_in)):
        live_in[i] = list(live_in[i])
        live_in[i].append(all_avl[i][0])

    if request.method == 'POST':
        price = request.form['price']
        size = request.form['size']
        type = request.form.get('type')
        hnumber = request.form.get('hnumber')
        avaliability = request.form['avaliability']
        building_id = request.form['building_id']

        if not price:
            error = 'Price is required.'
        elif not type:
            error = 'Type is required.'
        elif not building_id:
            error = 'You should choose one building your apartment belong.'
        elif g.conn.execute(
            '''SELECT building_id FROM buildings WHERE building_id = {};'''.format(building_id)
        ).fetchone() is None:
            return render_template('editoffer.html',
                                   error='This building_id is invalid.')
        flash(error)

        cursor = g.conn.execute(
          "SELECT max(apartment_id) FROM apartment_belong"
        )
        apartment_id = cursor.fetchone()[0] + 1

        if error is None:
            g.conn.execute(
                '''INSERT INTO apartment_belong (apartment_id, price, size, type, house_number, building_id) VALUES ({0}, '{1}', '{2}','{3}','{4}','{5}')'''.format(
                    apartment_id, price, size, type, hnumber, building_id)
                )
            g.conn.execute(
                '''INSERT INTO offer (apartment_id, landlord_id, availability ) VALUES ({0}, {1}, '{2}')'''.format(
                    apartment_id, landlord_id, avaliability)
            )
            flash('Landlord edits apartment offered successfully')
            return redirect(url_for('landlord_base'))

    return render_template('editoffer.html', self_login=session.get('logged_in'),live_in = live_in)

@app.route('/editrequirement/tenant', methods=['GET','POST'])
def editpost():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('tenant_login'))
    tenant_id = session.get('id')

    post = []
    cursor = g.conn.execute(
        "SELECT price,type,size FROM requirement where requirement_id in (select requirement_id from post where tenant_id = {})".format(tenant_id)
    ).fetchall()


    for result in cursor:
        post.append(result)

    if request.method == 'POST':
        price = request.form['price']
        size = request.form['size']
        type = request.form.get('type')

        if not price:
            error = 'Price is required.'
        elif not type:
            error = 'Type is required.'
        flash(error)

        cursor = g.conn.execute(
          "SELECT max(requirement_id) FROM requirement"
        )
        requirement_id = cursor.fetchone()[0] + 1

        if error is None:
            g.conn.execute(
                '''INSERT INTO requirement (requirement_id, price, size, type) VALUES ({0}, {1}, '{2}','{3}')'''.format(
                    requirement_id, price, size, type)
                )
            g.conn.execute(
                '''INSERT INTO post (requirement_id, tenant_id ) VALUES ({0}, {1})'''.format(
                    requirement_id, tenant_id)
            )
            flash('Tenant edits apartment requirement successfully')
            return redirect(url_for('tenant_base'))

    return render_template('editpost.html', self_login=session.get('logged_in'),post = post)

@app.route('/companylist', methods=['GET','POST'])
def companylist():
    company_list = []
    cursor = g.conn.execute(
        "SELECT company_id,name FROM company"
    ).fetchall()
    for result in cursor:
        company_list.append(result)
    return render_template('companylist.html',  company_list = company_list)


@app.route('/buildinglist', methods=['GET','POST'])
def buildinglist():
    building_list = []
    cursor = g.conn.execute(
        "SELECT building_id,address FROM buildings"
    ).fetchall()
    for result in cursor:
        building_list.append(result)
    return render_template('buildinglist.html',  building_list = building_list)


@app.route('/editworkin/tenant', methods=['GET','POST'])
def editworkin():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('tenant_login'))
    tenant_id = session.get('id')

    work_in = []
    cursor = g.conn.execute(
        "SELECT C.name,W.salary,W.since_, C.email,C.address,C.phone FROM company as C, work_in as W where C.company_id = W.company_id and W.tenant_id = {}".format(tenant_id)
    ).fetchall()

    for result in cursor:
        work_in.append(result)

    if request.method == 'POST':
        company_id = request.form['companyid']
        salary = request.form['salary']
        since_ = request.form['since']

        if not company_id:
            error = 'Please input companyid.'
        elif g.conn.execute(
                '''SELECT company_id FROM company WHERE company_id = {};'''.format(company_id)
        ).fetchone() is None:
            error='Company ID you input is invalid.'
        elif g.conn.execute(
                '''SELECT company_id,salary,since_ FROM work_in WHERE company_id = {0} and salary = {1} and since_= '{2}';'''.format(company_id,salary,since_)
        ).fetchone() is not None:
            error='This experience already in database.'
        flash(error)

        if error is None:
            g.conn.execute(
                '''INSERT INTO work_in (company_id, tenant_id, salary, since_) VALUES ({0}, {1}, {2}, '{3}')'''.format(
                    company_id, tenant_id, salary, since_)
            )
            flash('Tenant edits work_in successfully')
            return redirect(url_for('tenant_base'))

    return render_template('editworkin.html', self_login=session.get('logged_in'),work_in = work_in)

@app.route('/editlivein/tenant', methods=['GET','POST'])
def editlivein():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('tenant_login'))
    tenant_id = session.get('id')

    live_in = []
    cursor = g.conn.execute(
        "SELECT  l.from_, l.to_ ,a.size, a.price, a.type, a.house_number, b.address FROM apartment_belong as a, buildings as b, live_in as l where a.building_id = b.building_id and l.apartment_id = a.apartment_id and l.tenant_id =  {}".format(tenant_id)
    ).fetchall()

    for result in cursor:
        live_in.append(result)

    if request.method == 'POST':
        from_ = request.form['from']
        to_ = request.form['to']
        size = request.form['size']
        price = request.form['price']
        type = request.form['type']
        house_number = request.form['house_number']
        building_id = request.form['building_id']

        if not building_id:
            error = 'Please input buildingid.'
        elif g.conn.execute(
                '''SELECT building_id FROM buildings WHERE building_id = {};'''.format(building_id)
        ).fetchone() is None:
            error='Building ID you input is invalid.'
        flash(error)

        if error is None:
            if g.conn.execute(
                '''SELECT size,price,type,house_number,building_id 
                FROM apartment_belong 
                WHERE size = '{0}' and price = {1} and type = '{2}' and house_number = '{3}' and building_id = {4};'''
                        .format(size,price,type,house_number,building_id )
        ).fetchone() is None:
                cursor = g.conn.execute(
                    "SELECT max(apartment_id) FROM apartment_belong"
                )
                apartment_id = cursor.fetchone()[0] + 1
                g.conn.execute(
                    '''INSERT INTO apartment_belong (apartment_id,size,price,type,house_number,building_id ) VALUES ({0},'{1}',{2},'{3}','{4}',{5})'''.format(apartment_id,size,price,type,house_number,building_id )
                )
            else:
                apartment_id = g.conn.execute(
                '''SELECT apartment_id
                FROM apartment_belong 
                WHERE size = '{0}' and price = {1} and type = '{2}' and house_number = '{3}' and building_id = {4};'''
                        .format(size,price,type,house_number,building_id)
                ).fetchone()[0]

            g.conn.execute(
                '''INSERT INTO live_in (tenant_id, apartment_id, from_, to_) VALUES ({0}, {1}, '{2}','{3}')'''.format(
                    tenant_id, apartment_id, from_, to_)
            )
            flash('Tenant edits live_in successfully')
            return redirect(url_for('tenant_base'))

    return render_template('editlivein.html', self_login=session.get('logged_in'),live_in = live_in)

@app.route('/view_recommended_apartments')
def view_recommended_apartments():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('tenant_login'))
    tenant_id = session.get('id')

    max_price = g.conn.execute(
                    "SELECT max(price) FROM requirement WHERE requirement_id in (SELECT requirement_id FROM post WHERE tenant_id = {})".format(tenant_id)
                ).fetchone()[0] + 500
    apt = g.conn.execute(
                    '''select a.size, a.type, a.price, a.house_number, b.address
    from apartment_belong as a, buildings as b, offer as o
    where a.building_id = b.building_id and a.apartment_id = o.apartment_id and o.availability = True and price <= {}'''.format(max_price)
                ).fetchall()
    return render_template('view_recommended_apartments.html', self_login=session.get('logged_in'), apt = apt)

@app.route('/view_recommended_tenants')
def view_recommended_tenants():
    error = None
    if session.get('logged_in') == False:
        return redirect(url_for('landlord_login'))
    landlord_id = session.get('id')

    min_price = g.conn.execute(
                    "SELECT min(price) FROM apartment_belong WHERE apartment_id in (SELECT apartment_id FROM offer WHERE landlord_id = {})".format(landlord_id)
                ).fetchone()[0] - 500
    tenants = g.conn.execute(
                    '''select t.name, t.email, t.gender, t.age, r.price, r.type
    from tenants as t , requirement as r, post as p
    where t.tenant_id = p.tenant_id and p.requirement_id = r.requirement_id and r.price >= {}'''.format(min_price)
    ).fetchall()


    return render_template('view_recommended_tenants.html', self_login=session.get('logged_in'), tenants = tenants)





if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()
