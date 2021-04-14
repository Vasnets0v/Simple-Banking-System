import sqlite3
from random import randint

db = sqlite3.connect('card.s3db')
sql_request = db.cursor()
sql_request.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER default 0);")
sql_request.execute("INSERT INTO card VALUES (0, 0, 0, 0)")

class CardSystem():

    def do_transfer(self):
        number = []
        print("Enter card number:")
        card_number = input()
        sql_request.execute(f"SELECT balance FROM card WHERE id = '{self.id}'")
        a = sql_request.fetchone()
        money = a[0]

        for num in card_number:
            number.append(int(num))

        if self.luhn(card_number) == int(number[15]):
            sql_request.execute(f"SELECT number FROM card WHERE number = '{card_number}'")
            if sql_request.fetchone() is None:
                print("Such a card does not exist.")
            else:
                print("Enter how much money you want to transfer:")
                transfer_amount = int(input())
                if transfer_amount > money:
                    print("Not enough money!")
                else:
                    rest = money - transfer_amount
                    sql_request.execute(f"SELECT balance FROM card WHERE number = '{card_number}'")
                    add_money = sql_request.fetchone()
                    add_money = add_money[0]
                    add_money += transfer_amount
                    sql_request.execute(f"UPDATE card SET balance = '{rest}' WHERE id = '{self.id}'")
                    sql_request.execute(f"UPDATE card SET balance = '{add_money}' WHERE number = '{card_number}'")
                    db.commit()
                    print("Success!")
        else:
            print("Probably you made a mistake in the card number. Please try again!")

    def close_account(self):
        sql_request.execute(f"DELETE FROM card WHERE id = '{self.id}'")
        self.log_in = False
        self.id = None
        db.commit()

    def add_money(self):
        print("Enter income:")
        income_money = int(input())
        sql_request.execute(f"SELECT balance, id from CARD WHERE id = '{self.id}'")
        a = sql_request.fetchone()
        a = a[0]
        _sum_money = a + income_money
        sql_request.execute(f"UPDATE card SET balance = '{_sum_money}' WHERE id = '{self.id}'")
        db.commit()

    def counter(self):
        sql_request.execute("SELECT MAX(id) FROM card")
        a = sql_request.fetchone()
        a = a[0]
        sql_request.execute("DELETE FROM card WHERE id = 0")
        return a + 1

    def luhn(self, num):
        _sum = 0
        dic = []

        for i in num:
            dic.append(int(i))

        i = 0
        while i < 15:
            if dic[i] * 2 > 9:
                a = str(dic[i] * 2)
                _sum += int(a[0]) + int(a[1])
            else:
                _sum += dic[i] * 2
            if i == 14:
                break
            i += 1
            _sum += dic[i]
            i += 1
        
        if _sum % 10 == 0:
            return 0
        else:
            return 10 - (_sum % 10)

    def outpun_info(self):
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.pin)

    def text_one(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

    def text_two(self):
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

    def create_card_number(self):
        random_nine = []
        i = 0
        person_number = ""

        while i < 9:
            random_nine.append(randint(1, 9))
            i += 1

        for number in random_nine:
            person_number += str(number)

        self.card_number = int("400000" + str(person_number) + str(self.luhn("400000" + str(person_number))))

    def create_pin(self):
        random_four = []
        i = 0
        pin = ""

        while i < 4:
            random_four.append(randint(1, 9))
            i += 1

        for pin_num in random_four:
            pin += str(pin_num)

        self.pin = int(pin)

    def login(self):
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        pin = input()

        temp = sql_request.execute("SELECT number, pin, id FROM card")

        for i in temp:
            if i[0] == card_number:
                if i[1] == pin:
                    print("You have successfully logged in!")
                    self.log_in = True
                    self.id = i[2]
                    break
        else:
            print("Wrong card number or PIN!")

    def _loop(self):
        while True:
            
            if self.log_in == False:
                
                self.text_one()

                user_input = int(input())

                if user_input == 1:
                    self.create_card_number()
                    self.create_pin()
                    self.outpun_info()
                    sql_request.execute(f"INSERT INTO card  VALUES (?, ?, ?, ?)", (int(self.counter()), str(self.card_number), str(self.pin), 0))
                    db.commit()
                elif user_input == 2:
                    self.login()
                elif user_input == 0:
                    print("Bye!")
                    break
                else:
                    print("Error")

            else:
                self.text_two()

                user_input = int(input())

                if user_input == 1:
                    sql_request.execute(f"SELECT balance FROM card WHERE id = '{self.id}'")
                    a = sql_request.fetchone()
                    a = a[0]
                    print(a)

                elif user_input == 2:
                    self.add_money()
                    print("Income was added!")

                elif user_input == 3:
                    self.do_transfer()

                elif user_input == 4:
                    self.close_account()
                    print("The account has been closed!")

                elif user_input == 5:
                    self.log_in = False
                    self.id = None

                elif user_input == 0:
                    print("Bye!")
                    break

                else:
                    print("Error")

    def __init__(self):
        self.withount_lun = None
        self.log_in = False
        self.card_number = None
        self.pin = None
        self.bal = None
        self.id = None


simple_banking_system = CardSystem()

simple_banking_system._loop()
