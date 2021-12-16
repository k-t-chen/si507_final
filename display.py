import os
import time
import sys
# imports datetime to reformat the created data received from json
from datetime import datetime
from get_data import Data
from tree import buildDict


class Ticket():
    def __init__(self):
        self.getJson = Data()
        self.tree = buildDict()
        self.tickets_count = self.getJson.get_data().get('count', 0)
        self.retry_flags = ["1", "y", "yes"]
        self.non_retry_flags = ["2", "n", "no"]
        self.quit_flags = ["q", "quit"]
        self.sliding_next = ["1", "next"]
        self.sliding_prev = ["2", "prev"]
        self.sliding_home = ["3", "home", "home page"]

    def monitor_cleaner(self):
        try:
            time.sleep(1)
            os.system("clear")
        except Exception as e:
            print("Oops! There is something wrong : ", e)
            return False
        return True

    def title_display(self):
        print("Ticket Id", 2 * " ", "Subject", 41 * " ", "Created at", 10 * " ", "Assigned by")
        print(100 * "*")
        print("\n")
        return


    def show_ticket(self, ticket):
        ticket_id = ticket.get("id", "")
        assinged_by = str(ticket.get("assignee_id", ""))
        subject = ticket.get('subject', "")

        # gets created_at from data json and formats into date format
        # and then converts into strings. ps. use of T and Z
        # is for satification of the format
        # received by data json
        created_at = str(datetime.strptime(ticket.get("created_at",  ""), '%Y-%m-%dT%H:%M:%SZ')) # add a default value by your self
        string = "{:{fill}{align}{width}}"

        # passing format codes as arguments to format
        # the output easily readable
        print(string.format(ticket_id, fill='', align='<', width=13) + 
            string.format(subject, fill='', align='<', width=50) + 
            string.format(created_at, fill='', align='<', width=22) +
            string.format(assinged_by, fill='', align='<', width=14))
        return
    # This method loops through all the tickets and displays
    # in individual page
    def show_tickets(self, tickets, page):
        page_count = page * self.getJson.MAX_PAGE
        for ticket in tickets:
            self.show_ticket(ticket)
            page_count += 1
        return
    
    def get_valid_ticket_id(self):
        ticket_id = input('Please Enter the Ticket ID to get the ticket: ')
        while (not ticket_id.isnumeric() or not (1 <= int(ticket_id) <= self.tickets_count)):
            print("\nYour input is invalid, please enter from 1 to", str(self.tickets_count))
            print("Please try Again!")
            self.monitor_cleaner()
            ticket_id = input('Please Re-Enter the Ticket ID to get your ticket: ')
            continue
        return ticket_id
    
    def get_ticket_retry(self):
        print("\n" + 6 * "*", "Do you want to search again?" + 6 * "*"+"\n")
        print("1. Yes (Enter 1) ")
        print("2. No (Enter 2) ")
        print("\nQuit (type q or Q to Quit) ")

        choice  = input("\nEnter your choice: ").lower()
        while choice not in (self.quit_flags + self.retry_flags + self.non_retry_flags):
            print("""\nPlease enter the above options!""")
            choice  = input("\nEnter your choice: ").lower()

        return choice

    def get_ticket(self):
        while True:
            ticket_id = self.get_valid_ticket_id()
            self.monitor_cleaner()

            # gets data of a single ticket with validated ticket id
            target_data = self.getJson.get_one(ticket_id)
            ticket = target_data.get("ticket", {}) # change default by your self

            if ticket:
                self.title_display()
                self.show_ticket(ticket)  # displays the ticket
            else:
                print("\nThere is no such ticket. Please try again!")
            
            choice = self.get_ticket_retry()
            if choice in self.retry_flags:
                self.monitor_cleaner()
                continue
            elif choice in self.non_retry_flags:
                print("Returning to Home Page.............")
                self.monitor_cleaner()
                break
            elif choice in self.quit_flags:
                print("\nBye! Have a good day!\n")
                exit()

    def sliding_page(self):
        print("")
        print("")
        print("OPTIONS")
        print("1. Enter 1 to view next page ")
        print("2. Enter 2 to view previous page ")
        print("3. Enter 3 to return to Home page ")
        print("")
        print("4. type q or Q to Quit ")
        print("")

        choice = input("Please enter your choice: ")
        while choice not in (self.sliding_next + self.sliding_prev + self.sliding_home + self.quit_flags):
            print("""\nPlease enter the above options!""")
            choice  = input("\nEnter your choice: ").lower()
        return choice

    # This method is used to get all tickets.

    def get_all_tickets(self):
        while True:
            tickets = self.getJson.get_data().get("tickets", [])
            next_page = self.getJson.get_data().get("next_page", "") # change default value by your self
            prev_page = self.getJson.get_data().get("previous_page", "") # change default value by your self

            self.monitor_cleaner()

            print("\nCurrent Page: " + str(self.getJson.params.get('page', "cannot get page info")))
            print(9 * "*")
            self.title_display()
            # please look error handler when you can not get page info
            self.show_tickets(tickets, self.getJson.params.get('page', 0))
            choice = self.sliding_page()
            if choice in self.sliding_next:
                if next_page:
                    self.monitor_cleaner()
                    print("Now loading.........")
                    print("Wait a second")
                    self.getJson.params['page'] += 1                    
                else:
                    self.monitor_cleaner()
                    print('No page left')
                continue
            elif choice in self.sliding_prev:
                if prev_page:
                    self.monitor_cleaner()
                    print("Now loading.........")
                    print("Wait a second")
                    self.getJson.params['page'] -= 1                    

                else:
                    self.monitor_cleaner()    
                    print('You are in the first page!')
                continue
            elif choice in self.sliding_home:
                self.monitor_cleaner()
                print("Redirect to Home Page.........")
                print("Wait a second")
                time.sleep(1)
                break

            elif choice in self.quit_flags:
                print("\nBye! Have a good day!\n")
                sys.exit()


    def get_description(self):
        name = input('Please Enter words to find the description and ticket id: ')
        while not self.tree.search(name):
            print("\nThere are no tickets descriptions from your typing")
            print("Please try Again!")
            self.monitor_cleaner()
            name = input('Please Re-Enter the description to find your ticket: ')
            continue
        return self.tree.search(name)

    def get_the_description(self):
        while True:
            ticket = self.get_description()
            print(ticket)
            self.monitor_cleaner()
            ticket_id = input('Please enter the ticket_id: ')
            # gets data of a single ticket with validated ticket id
            target_data = self.getJson.get_one(ticket_id)
            ticket = target_data.get("ticket", {}) # change default by your self

            if ticket:
                self.title_display()
                self.show_ticket(ticket)  # displays the ticket
            else:
                print("\nThere is no such ticket. Please try again!")
            
            choice = self.get_ticket_retry()
            if choice in self.retry_flags:
                self.monitor_cleaner()
                continue
            elif choice in self.non_retry_flags:
                print("Returning to Home Page.............")
                self.monitor_cleaner()
                break
            elif choice in self.quit_flags:
                print("\nBye! Have a good day!\n")
                exit()

