from datetime import datetime
from myprint import print_bar

TABLE_NAME = "fees"


class Fee:
    def __init__(self):
        self.record_id = 0
        self.student_id = ""
        self.student_name = ""
        self.date_of_payment = ""
        self.amount = ""

    def create(self, record_id, student_id, student_name, date_of_payment, amount):
        self.record_id = record_id
        self.student_id = student_id
        self.student_name = student_name
        self.date_of_payment = date_of_payment
        self.amount = amount
        return self

    def create_from_record(self, record):
        self.record_id = record['id']
        self.student_id = record['student_id']
        self.student_name = record['name']
        self.date_of_payment = record['date_of_payment']
        self.amount = record['amount']
        return self

    def print_all(self):
        print(str(self.record_id).ljust(10),
              str(self.student_id).ljust(10),
              self.student_name.ljust(15),
              self.date_of_payment.strftime("%d-%b-%Y").ljust(15),
              str(self.amount)[0:30].ljust(15))

    def print_full(self):
        print_bar()
        print("Record id: ", self.record_id)
        print("Student id: ", self.student_id)
        print("Student Name: ", self.student_name)
        print("Date of Payment: ", self.date_of_payment.strftime("%d-%b-%y"))
        print("Amount: ", self.amount)
        print_bar()


def create_fee_record(student):
    record_id = None
    date_of_payment = datetime.now()
    amount = int(input("Enter the amount: "))
    return Fee().create(record_id, student.student_id, student.name, date_of_payment, amount)


def print_header():
    print("="*100)
    print("id".ljust(10),
          "student id".ljust(10),
          "name".ljust(15),
          "payment date".ljust(15),
          "amount".ljust(15))
    print("="*100)


def create_sale_table(database):
    cursor = database.cursor()
    cursor.execute("DROP table if exists {0}".format(TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "student_id int not null,"
                   "name varchar(20) not null,"
                   "date_of_payment date not null,"
                   "amount int not null)".format(TABLE_NAME))
