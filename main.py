import sys
from students import student_menu
from fees import fees_menu
from myprint import print_center, input_center
from database import get_database


if __name__ == '__main__':
    database, cursor = get_database()
    if database is None:
        print("Unable to open database, make sure user name and password are correct and has sufficient privileges.")
        sys.exit(1)
    while True:
        print()
        print_center("===================================")
        print_center("=====Student Management System=====")
        print_center("===================================")
        print_center("1. Manage Fees")
        print_center("2. Manage Students")
        print_center("0. Exit")
        print()
        choice = int(input_center("Enter your choice: "))
        if choice == 1:
            fees_menu(database, cursor)
        elif choice == 2:
            student_menu(database, cursor)
        elif choice == 0:
            break
        else:
            print("Invalid choice (Press 0 to exit)")
    database.close()
    print_center("GoodBye")
