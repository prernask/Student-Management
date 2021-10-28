from datetime import datetime
from myprint import print_bar

TABLE_NAME = "students"


class Student:
    def __init__(self):
        self.student_id = ""
        self.name = ""
        self.gender = ""
        self.date_of_birth = ""
        self.address = ""
        self.phone_no = ""
        self.date_of_admission = ""

    def create(self, student_id, name, gender, date_of_birth, address, phone_no, date_of_admission):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_no = phone_no
        self.date_of_admission = date_of_admission
        return self

    def create_from_record(self, record):
        self.student_id = record['id']
        self.name = record['name']
        self.gender = record['gender']
        self.date_of_birth = record['date_of_birth']
        self.address = record['address']
        self.phone_no = record['phone_no']
        self.date_of_admission = record['date_of_admission']
        return self

    def print_all(self):
        print(str(self.student_id).ljust(5),
              self.name[0:15].ljust(15),
              self.gender.ljust(15),
              self.date_of_birth.strftime("%d %b %Y").ljust(15),
              self.address[0:10].ljust(15),
              self.phone_no.ljust(15),
              self.date_of_admission.strftime("%d %b %Y").ljust(15)
              )

    def print_full(self):
        print_bar()
        print("ID: ", self.student_id)
        print("Name: ", self.name)
        print("Gender: ", self.gender)
        print("Date Of Birth: ", self.date_of_birth.strftime("%d %b %y"))
        print("Address: ", self.address)
        print("Phone No: ", self.phone_no)
        print("Admission Date: ", self.date_of_admission.strftime("%d %b %y"))
        print_bar()


def create_student():
    name = input("Enter the name: ")
    gender = input("Enter the gender (Male/Female): ")
    date_of_birth = datetime.strptime(input("Enter the date of birth (DD-MM-YYYY): "),"%d-%m-%Y")
    address = input("Enter the address: ")
    phone_no = input("Enter the phone number: ");
    admission_date = datetime.now()
    return Student().create(None, name, gender, date_of_birth, address, phone_no, admission_date)


def print_header():
    print("="*100)
    print("ID".ljust(5),
          "Name".ljust(15),
          "Gender".ljust(15),
          "Date Of birth".ljust(15),
          "Address".ljust(15),
          "phone no".ljust(15),
          "addmission date".ljust(15)
          )
    print("="*100)


def create_medicine_table(cursor):
    cursor.execute("DROP table if exists {0}".format(TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "name varchar(20) not null,"
                   "gender varchar(20) not null,"
                   "date_of_birth date not null,"
                   "address varchar(50) not null,"
                   "phone_no varchar(10) not null,"
                   "date_of_admission date not null)".format(TABLE_NAME))
