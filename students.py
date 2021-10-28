from datetime import datetime
import mysql
from student import Student, create_student, TABLE_NAME, create_medicine_table, print_header


def add_student(database, cursor):
    student = create_student()
    query = "insert into {0}(name,gender,date_of_birth,address,phone_no,date_of_admission) " \
            "values('{1}','{2}','{3}','{4}','{5}','{6}')".\
            format(TABLE_NAME,student.name, student.gender,student.date_of_birth.strftime("%Y-%m-%d"), student.address,
                   student.phone_no, student.date_of_admission.strftime("%Y-%m-%d"))
    try:
        cursor.execute(query)
        database.commit()
    except mysql.connector.Error:
        create_medicine_table(cursor)
        cursor.execute(query)
        database.commit()
    print("Operation Successful")


def show_record(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        record = records[0]
        student = Student().create_from_record(record)
        student.print_full()
        return student
    except mysql.connector.Error as err:
        print(err)


def show_records(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No Matching Records")
            return
        print_header()
        students = []
        for record in records:
            student = Student().create_from_record(record)
            students.append(student)
            student.print_all()
        return students
    except mysql.connector.Error as err:
        print(err)


def get_and_print_student_by_id(cursor):
    student_id = input("Enter the id: ")
    query = "select * from {0} where id={1}".format(TABLE_NAME, student_id)
    student = show_record(cursor, query)
    return student


def edit_student_record(database, cursor):
    student = get_and_print_student_by_id(cursor)
    if student is None:
        print("No match")
    else:
        query = "update {0} set".format(TABLE_NAME)
        print("Input new values (leave blank to keep previous value)")
        name = input("Enter the new name: ")
        if len(name) > 0:
            query += " name='{0}',".format(name)
        gender = input("Enter new gender: ")
        if len(gender) > 0:
            query += " gender='{0}',".format(gender)

        date_of_birth = input("Enter the new date of birth (DD-MM-YYYY): ")
        if len(date_of_birth) > 0:
            date_of_birth = datetime.strptime(date_of_birth,"%d-%m-%Y")
            query += " date_of_birth='{0}',".format(date_of_birth.strftime("%Y-%m-%d"))

        address = input("Enter new address: ")
        if len(address) > 0:
            query += " address='{0}',".format(address)

        phone_no = input("Enter new phone number: ")
        if len(phone_no) > 0:
            query += " phone_no='{0}',".format(phone_no)

        date_of_admission = input("Enter the new date of admission (DD-MM-YYYY): ")
        if len(date_of_admission) > 0:
            date_of_admission = datetime.strptime(date_of_admission, "%d-%m-%Y")
            query += " date_of_admission='{0}',".format(date_of_admission.strftime("%Y-%m-%d"))

        query = query[0:-1] + " where id={0}".format(student.student_id)
        confirm = input("Confirm Update (Y/N): ").lower()
        if confirm == 'y':
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")


def delete_student_by_id(database, cursor):
    student = get_and_print_student_by_id(cursor)
    if student is None:
        print("No match")
    else:
        confirm = input("Confirm Deletion (Y/N): ").lower()
        if confirm == 'y':
            query = "delete from {0} where id='{1}'".format(TABLE_NAME,student.student_id)
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")


def student_menu(database, cursor):
    while True:
        print()
        print("============================")
        print("==========Students Menu=========")
        print("============================")
        print()

        print("1. Add a student")
        print("2. Get student details by name")
        print("3. Get student details by id")
        print("4. Get student details by address")
        print("5. Get student details by date of admission")
        print("6. Edit Student details")
        print("7. Delete Student")
        print("8. View all students")
        print("0. Go Back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_student(database, cursor)
        elif choice == 2:
            name = input("Enter the name: ")
            query = "select * from {0} where name like '%{1}%'".format(TABLE_NAME, name)
            show_records(cursor, query)
        elif choice == 3:
            get_and_print_student_by_id(cursor)
        elif choice == 4:
            address = input("Enter the address: ")
            query = "select * from {0} where address like '%{1}%'".format(TABLE_NAME, address)
            show_records(cursor, query)
        elif choice == 5:
            date_of_admission = datetime.strptime(input("Enter the date of admission (DD-MM-YYYY): "), "%d-%m-%Y")
            date_of_admission = date_of_admission.strftime("%Y-%m-%d")
            query = "select * from {0} where date_of_admission='{1}'".format(TABLE_NAME, date_of_admission)
            show_records(cursor,query)
        elif choice == 6:
            edit_student_record(database, cursor)
        elif choice == 7:
            delete_student_by_id(database, cursor)
        elif choice == 8:
            query = "select * from {0}".format(TABLE_NAME)
            show_records(cursor, query)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to go back)")
