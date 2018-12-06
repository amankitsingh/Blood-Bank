from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User, Base, BRequest, Donor, BloodBank, Hospital

engine = create_engine('sqlite:///data.db')
#engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#creating first User
#donot add data in this table
user1 = User(staffid = 1, name = "ankit", password = "neveraskit")

session.add(user1)
session.commit()

user2 = User(staffid = 2, name = "abhishek", password = "chalbey")

session.add(user2)
session.commit()

#Donation table
#add more 3 different data
donor = Donor(name="Abhishek", sex="Male", phno=7895784865, age=20, bloodgroup="A+", address="Bihar")

session.add(donor)
session.commit()

doner = Donor(name="Anand", sex="Male", phno=9867541876, age=22, bloodgroup="Ab-", address="Utter pradesh")

session.add(doner)
session.commit()

doner = Donor(name="Komal", sex="Female", phno=9807654897, age=23, bloodgroup="Ab+", address="Delhi")

session.add(doner)
session.commit()

doner = Donor(name="Riya", sex="Female", phno=7876453458, age=19, bloodgroup="O+", address="Pune")

session.add(doner)
session.commit()

donor = Donor(name="Ram", sex="Male", phno=7853784865, age=21, bloodgroup="B+", address="Goa")

session.add(donor)
session.commit()

#Request for blood table
brequest = BRequest(name="Abhijeet", emailid="abhijeet@protonmail.com", phno=7788994455, sex="Male", bloodgroup="A+", hospitalname="Manipal")

session.add(brequest)
session.commit()

brequest = BRequest(name="Sonu kumar", emailid="sonukumar12@gmail.com", phno=7787653590, sex="Male", bloodgroup="Ab-", hospitalname="SKMCH")

session.add(brequest)
session.commit()


brequest = BRequest(name="Ashutosh", emailid="ashutosh132@gmail.com", phno=9080065425, sex="Male", bloodgroup="Ab+", hospitalname="PMCH")

session.add(brequest)
session.commit()

brequest = BRequest(name="Sonali singh", emailid="sonslisingh12@gmail.com", phno=7895432527, sex="Female", bloodgroup="B+", hospitalname="Appolo")

session.add(brequest)
session.commit()

brequset = BRequest(name="Nishant c", emailid="nishantc456@gmail.com", phno=8970543268, sex="Male", bloodgroup="O+", hospitalname="AIIMS")

session.add(brequest)
session.commit()


# bloodgroup is the Column which tell varient of bloodgroup available with Hospital
bank = BloodBank(name="Manipal", location="Delhi", phno=7799784865,  bloodgroup="A+, B+, O+, O-", hospitalid=7845)

session.add(bank)
session.commit()

bank = BloodBank(name="SKMCH", location="Muzaffarpur", phno=7788994455,  bloodgroup="A+, Ab-,B+, O+, O-", hospitalid=7834)

session.add(bank)
session.commit()

bank = BloodBank(name="PMCH", location="Patna", phno=7799784865,  bloodgroup="A-,B+, O+, O-", hospitalid=8791)

session.add(bank)
session.commit()

bank = BloodBank(name="Appolo", location="Bangalore", phno=7799784865,  bloodgroup="O+, O-", hospitalid=45632)

session.add(bank)
session.commit()

bank = BloodBank(name="AIIMS", location="Goa", phno=7799784865,  bloodgroup="Ab-,Ab+,B+,B-, O+, O-", hospitalid=45623)

session.add(bank)
session.commit()

#Hospital Table
hospital = Hospital( id=7845, name="Manipal", phone=9999984865, location="Delhi")

session.add(hospital)
session.commit()

hospital = Hospital( id=7834, name="SKMCH", phone=9975984865, location="Muzaffarpur")

session.add(hospital)
session.commit()

hospital = Hospital( id=8791, name="PMCH", phone=8965437896, location="Patna")

session.add(hospital)
session.commit()

hospital = Hospital( id=45632, name="Appolo", phone=90704575686, location="Bangalore")

session.add(hospital)
session.commit()

hospital = Hospital( id=45623, name="AIIMS", phone=9771213456, location="Goa")
session.add(hospital)

session.commit()

print "Database is populated"
