from datetime import datetime
import mysql
from fee import create_fee_record, TABLE_NAME, create_sale_table, print_header,Fee
from students import get_and_print_student_by_id


def register_fees(database, cursor):
    student = get_and_print_student_by_id(cursor)
    if student is not None:
        fee_record = create_fee_record(student)
        if fee_record is not None:
            confirm = input("Complete the operation? (Y/N) ").lower()
            if confirm == 'y':
                query = "insert into {0}(student_id,name,date_of_payment,amount) " \
                        "values ({1},'{2}','{3}',{4})".\
                    format(TABLE_NAME, fee_record.student_id, fee_record.student_name,
                           fee_record.date_of_payment.strftime("%Y-%m-%d"), fee_record.amount)
                try:
                    cursor.execute(query)
                    database.commit()
                except mysql.connector.Error as err:
                    create_sale_table(database)
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
        issue_record = Fee().create_from_record(record)
        issue_record.print_full()
        return issue_record
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
        for record in records:
            sale_record = Fee().create_from_record(record)
            sale_record.print_all()
        return records
    except mysql.connector.Error as err:
        print(err)


def get_and_print_record_by_id(cursor):
    record_id = int(input("Enter the id: "))
    query = "select * from {0} where id = {1}".format(TABLE_NAME, record_id)
    sale_record = show_record(cursor, query)
    return sale_record


def edit_record_by_id(database, cursor):
    fee_record = get_and_print_record_by_id(cursor)
    if fee_record is None:
        print("No such record")
    else:
        query = "update {0} set".format(TABLE_NAME)
        print("Input new values (leave blank to keep previous value)")

        date_of_payment = input("Enter the new date of payment (DD-MM-YYYY): ")
        if len(date_of_payment) > 0:
            date_of_payment = datetime.strptime(date_of_payment, "%d-%m-%Y")
            query += " date_of_payment='{0}',".format(date_of_payment.strftime("%Y-%m-%d"))

        amount = input("Enter new amount: ")
        if len(amount) > 0:
            query += " amount='{0}',".format(amount)

        query = query[0:-1] + " where id={0}".format(fee_record.record_id)
        confirm = input("Confirm Update (Y/N): ").lower()
        if confirm == 'y':
            cursor.execute(query)
            database.commit()
            print("Operation Successful")
        else:
            print("Operation Cancelled")


def delete_record_by_id(database, cursor):
    fee_record = get_and_print_record_by_id(cursor)
    if fee_record is not None:
        confirm = input("Complete the operation? (Y/N) ").lower()
        if confirm == 'y':
            query = "delete from {0} where id={1}".format(TABLE_NAME,fee_record.record_id)
            cursor.execute(query)
            database.commit()
            print("Operation Successful")


def fees_menu(database, cursor):
    while True:
        print()
        print("============================")
        print("==========Fees Menu=========")
        print("============================")
        print()

        print("1. Register Fees")
        print("2. Show fee record by id")
        print("3. Show fee record by payment date")
        print("4. Show list of last 10 payments")
        print("5. Edit Record")
        print("6. Delete Record")
        print("7. View all Records")
        print("0. Go Back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            register_fees(database, cursor)
        elif choice == 2:
            get_and_print_record_by_id(cursor)
        elif choice == 3:
            date_of_payment = datetime.strptime(input("Enter the date (DD-MM-YYYY): "), "%d-%m-%Y")
            date_of_payment = date_of_payment.strftime("%Y-%m-%d")
            query = "select * from {0} where date_of_payment='{1}'".format(TABLE_NAME, date_of_payment)
            show_records(cursor, query)
        elif choice == 4:
            query = "select * from {0} order by date_of_payment desc limit 10".format(TABLE_NAME)
            show_records(cursor, query)
        elif choice == 5:
            edit_record_by_id(database, cursor)
        elif choice == 6:
            delete_record_by_id(database, cursor)
        elif choice == 7:
            query = "select * from {0}".format(TABLE_NAME)
            show_records(cursor, query)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to go back)")
