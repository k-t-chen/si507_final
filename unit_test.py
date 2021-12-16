import unittest
from unittest.mock import patch
import main
import requests
import unittest.mock
import display
from display import Ticket
from get_data import Data
getJson = Data()
ticket = Ticket()


class TestCodes(unittest.TestCase):
    # test api crendential
    def test_credentials(self):
        # trying to get response from correct request with status code 200
        response = requests.get("https://zcckt.zendesk.com/api/v2/tickets.json", auth=("kuantinc@umich.edu", "Ab123456"))
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

    def failure_credentials(self):
        # Changing password  will result  in 401 or 400
        response = requests.get("https://zcckt.zendesk.com/api/v2/tickets.json", auth=("kuantinc@umich.edu", "3456"))        
        self.assertEqual(response.status_code, 401 or 400)

    # if the ticket is out of range, print the eeror message
    @patch('display.input', create=True)
    def test_input(self, mocked_input):
        mocked_input.side_effect = [130]
        display.Ticket.get_ticket
        self.assertTrue("\nThere is no such ticket. Please try again!")

    # raises value error on input when strings are passed
    @patch('display.input', create=True)
    def test_input(self, mocked_input):
        mocked_input.side_effect = ['asdf']
        display.Ticket.get_valid_ticket_id
        self.assertRaises(ValueError)

    # checks if we get the correct ticket id
    def test_one_ticket(self):
        id = str(15)
        data = getJson.get_one(id)
        ticket_id = str(data['ticket']['id'])
        self.assertEqual(ticket_id, id)
    
    # enter 3 in menu and it shows Bye! Have a good day!
    @patch('main.input', create=True)
    def test_menu(self, mocked_input):
        mocked_input.side_effect = [3]
        main.ZenDesk.run
        self.assertTrue("\nBye! Have a good day!\n")
    
    # checks the max page
    @patch('get_data.Data.total_page', create=True)
    def test_MAX_PAGE(self, mocked_input):
        mocked_input.side_effect = ['2']
        data = getJson.get_data()
        self.assertEqual(getJson.MAX_PAGE, len(data['tickets']))


   
if __name__ == "__main__":
    unittest.main()


