import os
import time 
from display import Ticket

class ZenDesk:
    def __init__(self):
        self.Ticket = Ticket()
        self.quit_flags = ["q", "quit"]
        self.get_all_tickets_flags = ["1"]
        self.get_ticket_flags = ["2"]
        self.retry_attemps = 3

    def main_menu(self):
        print("")
        print("Welcome to the Ticket viewer")
        print("")
        print("Please select an option from below:\n")
        print("Press 1 to view all the tickets ")
        print("Press 2 to view a single ticket ")
        print("Quit (Enter q or Q or quit to Quit ) \n")
    
    def monitor_cleaner(self):
        try:
            os.system("clear")
        except Exception as e:
            print("Oops! There is something wrong : ", e)
            return False
        return True
    
    def get_user_input(self):
        try:
            choice = input("Enter your choice:")
        except Exception as e:
            print("Oops! There is something wrong : ", e)
            return ""
        return choice
    
    def auto_retry(self, func):
        retry_count = 0
        while not func and self.retry_attemps < 3:
             retry_count += 1
        if retry_count == self.retry_attemps:
            return False
        return True

    def run(self):
        # clears out the screen everytime method menu is called
        if not self.auto_retry(self.monitor_cleaner()):
            print("Sorry we can not clean or monitor now, the program will keep go on")

        while True:
            # displays the main menu in the console everytime
            if not self.auto_retry(self.main_menu()):
                print("Sorry we can not display our menu now, you can keep using or stop it with ctrl+c")
            
            input_result = self.get_user_input()

            if not input_result: # if input invalid, we will show the menu again
                print("Oops!, your input may be invalid, the error messgae is : ", input_result)
                continue

            if input_result.lower() in self.quit_flags:
                # Quits the main console-based menu
                print("\nBye! Have a good day!\n")
                return

            elif input_result in self.get_all_tickets_flags:
                # calls get_all_tickets from display.py file to retrieve all tickets
                self.auto_retry(self.monitor_cleaner)
                self.auto_retry(self.Ticket.get_all_tickets())
                continue

            elif input_result in self.get_ticket_flags:
                # calls get_ticket from tickets.py file to get a single ticket
                self.auto_retry(self.monitor_cleaner)
                self.auto_retry(self.Ticket.get_ticket())
                continue
                
            else:
                print( " Your input is invalid, please try again! ")
                time.sleep(1)
                self.auto_retry(self.monitor_cleaner)
                continue

if __name__ == '__main__':
    executor = ZenDesk()
    executor.run()
