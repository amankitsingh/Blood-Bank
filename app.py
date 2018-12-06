from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database import User, Base, BRequest, Donor, BloodBank, Hospital

import time
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///data.db')
#engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#main page
@app.route('/')
@app.route('/mainpage/')
def mainpages():
    return render_template('mainpage.html')


#get complete details
@app.route('/login/adminlist/')
def completelist():
    donation = session.query(Donor).order_by(asc(Donor.name))
    blrequest = session.query(BRequest).order_by(asc(BRequest.name))
    hospitals = session.query(Hospital).order_by(asc(Hospital.id))
    bank = session.query(BloodBank).order_by(asc(BloodBank.hospitalid))
    return render_template('adminlist.html', donate=donation, blrequest=blrequest,hospitals=hospitals ,bloodbank=bank)

#login for admin
@app.route('/login/', methods=['GET', 'POST'])
def showlogin():
    if request.method == 'POST':
        admin = session.query(User).order_by(asc(User.staffid))
        #donation = session.query(Donor).order_by(asc(Donor.name))
        #blrequest = session.query(BRequest).order_by(asc(BRequest.name))
        #hospitals = session.query(Hospital).order_by(asc(Hospital.id))
        for users in admin:
            if request.form['username'] == users.name and request.form['password'] == users.password:
                return redirect(url_for('completelist'))
        for users in admin:
            if request.form['username'] != users.name and request.form['password'] == users.password or request.form['username'] == users.name and request.form['password'] != users.password:
                flash('Incorrect Username/Password')
                return redirect(url_for('showlogin'))
            else:
                flash('Sorry! Only Admin is allowed')
                return render_template('mainpage.html')

    else:
        return render_template('login.html')


#donation hospital list
@app.route('/mainpage/donate/')
def donates():
        hospitals = session.query(Hospital).order_by(asc(Hospital.id)).all()
        return render_template('hospitallist.html', hospitals=hospitals)


#redirect to the registration page of donation
@app.route('/mainpage/donate/register/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        donat = Donor(
            name=request.form['name'],
             sex=request.form['sex'],
              phno=request.form['phno'],
               age=request.form['age'],
                bloodgroup=request.form['bloodgroup'],
                 address=request.form['address'])

        session.add(donat)
        session.commit()
        flash('Thankyou for placing the Donation request! Hospital will Contact you Within 2 hours')
        return redirect(url_for('mainpages'))
    else:
        return render_template('donate.html')


#request blood from hospital
@app.route('/mainpage/request/', methods=['GET'])
def requestblood():
        hospital = session.query(Hospital).order_by(asc(Hospital.location)).all()
        bank = session.query(BloodBank).order_by(asc(BloodBank.location)).all()
        return render_template('bloodhospitallist.html', hospital=hospital, bloodbank=bank)


#request page
@app.route('/mainpage/request/bloodavail/<hospital_name>/', methods=['GET','POST'])
def requestfromhospital(hospital_name):
    if request.method == 'POST':
        pullrequest = BRequest(
                        name=request.form['name'], emailid=request.form['emailid'],
                        phno=request.form['phno'], sex=request.form['sex'],
                        bloodgroup=request.form['bloodgroup'], hospitalname=hospital_name)
        session.add(pullrequest)
        session.commit()
        flash('You Request is Successfull Placed in %s hospital' % hospital_name)
        flash('hospital will contact you within 2 hours')
        return redirect(url_for('mainpages'))
    else:
        return render_template('requestlist.html',hosp=hospital_name)


#delete after donatiion request when rejected
@app.route('/login/adminlist/responses/reject/<donation_name>/', methods=['GET','POST'])
def deldonar(donation_name):
    #if request.method == 'POST':
    RequestDelete = session.query(Donor).filter_by(name=donation_name).one()
    session.delete(RequestDelete)
    session.commit()
    flash(' %s Donation Request Processed' % donation_name)
    return redirect(url_for('completelist'))


#delete after bloodrequest is rejected
@app.route('/login/adminlist/responses/reject/reject/<brequest_name>/', methods=['GET'])
def delrequest(brequest_name):
    #if request.method == 'POST':
    RequestDelete = session.query(BRequest).filter_by(name=brequest_name).one()
    session.delete(RequestDelete)
    session.commit()
    flash('%s Request For Blood is Processed' % brequest_name)
    return redirect(url_for('completelist'))


#add hospitals
@app.route('/login/adminlist/responses/addhospital/', methods=['GET','POST'])
def addhospital():
    if request.method == "POST":
        pullrequest = Hospital(
                        id=request.form['id'], name=request.form['name'],
                        phone=request.form['phone'], location=request.form['location'])
        session.add(pullrequest)
        session.commit()
        pullbank = BloodBank(
                        name=request.form['bname'],location=pullrequest.location,
                        phno=request.form['phno'],bloodgroup=request.form['bloodgroup'],
                        hospitalid=request.form['id'])
        session.add(pullbank)
        session.commit()
        flash('%s Hospital added' % pullrequest.name)
        return redirect(url_for('completelist'))
    else:
        return render_template("addhospital.html")


#edit hospital
@app.route('/login/adminlist/responses/edit/<hospital_id>/', methods=['GET','POST'])
def edithospital(hospital_id):
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()
    bblood = session.query(BloodBank).filter_by(hospitalid=hospital_id).one()
    if request.method == "POST":
        editbloodbank = session.query(BloodBank).filter_by(location=hospital.location).one()
        if request.form['name']:
            hospital.id = hospital_id
            hospital.name = request.form['name']
            bblood.name = request.form['name']
        if request.form['phone']:
            hospital.phone = request.form['phone']
        if request.form['location']:
            hospital.location = request.form['location']
        if request.form['bname']:
            editbloodbank.name = request.form['bname']
        if request.form['blocation']:
            editbloodbank.location = request.form['blocation']
        if request.form['phno']:
            editbloodbank.phno = request.form['phno']
        if request.form['bloodgroup']:
            editbloodbank.bloodgroup = request.form['bloodgroup']
        flash('%s Hospital Edited' % hospital.name)
        return redirect(url_for('completelist'))
    else:
        return render_template('edithospital.html', hospital=hospital, bloodbank=bblood)


#delete hospital
@app.route('/login/adminlist/responses/delete/<hospital_name>/')
def deletehospital(hospital_name):
    RequesttoDelete = session.query(Hospital).filter_by(name=hospital_name).one()
    session.delete(RequesttoDelete)
    session.commit()
    flash('%s Hospital is Deleted' % hospital_name)
    return redirect(url_for('completelist'))

@app.route('/Deverlopers')
def Deverlopers():
    return render_template('developers.html')

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
