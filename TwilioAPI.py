from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import json

class TwilioAPI():
    """
    Purpose: Leverage Twilio APIs to provide verification and communication
    """

    def __init__(self):
        with open("twilio_config.json", "r") as json_data_file:
            twilioconfig = json.load(json_data_file)
        self.TWILIO_ACCOUNT_SID = twilioconfig["TWILIO_ACCOUNT_SID"]
        self.TWILIO_AUTH_TOKEN = twilioconfig["TWILIO_AUTH_TOKEN"]
        self.TWILIO_PHONENUMBER = twilioconfig["TWILIO_PHONENUMBER"]
        self.TWILIO_PHONENUMBER_ALPHA = twilioconfig["TWILIO_PHONENUMBER_ALPHA"]


    def add_ons_available(self):
        """
        prints a list of available add-ons associated with Twilio account
        :return: list
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        add_ons = client.preview.available_add_ons.list()
        for add_on in add_ons:
            print("Add ons:  name: {}  and SID: {}".format(add_on.friendly_name,
                                                           add_on.sid))


    def is_valid_number(self, number):
        """
        Twilio sourced code to test whether number is valid
        Adapted from LOOKKUP: https://www.twilio.com/blog/2016/02/how-to-verify-phone-numbers-in-python-with-the-twilio-lookup-api.html
        :param number: phone number: international or national
        :return: True if the response is a valid number; FALSE if not valid
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        try:
            response = client.lookups\
                .phone_numbers(number)\
                .fetch(type=["carrier", "caller-name"])  #returns additional info at cost
            #response = client.lookups\
            #    .phone_numbers(number)\
            #    .fetch() #returns general validation format
            return response
        except TwilioRestException as e:
            if e.code == 20404:             #When the Twilio Python library encounters a 404 it will throw a TwilioRestException
                return False
            else:
                return e


    def send_message(self, numberTO, messagebody):
        """
        Sends a message to a mobile number
        Adapted from LOOKKUP: https://www.twilio.com/blog/2016/02/how-to-verify-phone-numbers-in-python-with-the-twilio-lookup-api.html

        :param number: phone number: international or national
        :return: True if the response is a valid number; FALSE if not valid
        """
        #logger = logging.getLogger(__name__)
        #logger.info('in Twilio.send_message: - sending notification')
        #if
        #numberTO = "+"+numberTO
        print(('revised numberTO: {}'.format(numberTO)))
        #logger.info('Tophone: {}  message: {} '.format(numberTO, messagebody))
        print(('message : {}'.format(messagebody)))
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        try:
            response = client.messages.create(
                body=messagebody,
                from_=self.TWILIO_PHONENUMBER,
                to=numberTO)
            print((response.sid))
            return response
            #add to message log
            #msglog.savemessagelog(phonenumber=numberTO, adirection='OUTGOING',
            #                      messagebody=messagebody, loc_country="",
            #                      loc_city="")
        except TwilioRestException as e:
            #logger.info('Exception occurred: {} '.format(e))
            print('Exception occurred: {} '.format(e))
            if e.code == 20404:             #When the Twilio Python library encounters a 404 it will throw a TwilioRestException
                return False
            else:
                return False


    # def messagewithalias(self,numberTO, messagebody):
    #     try:
    #         client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
    #         response = client.messages.create(
    #             body=messagebody,
    #             from_=self.TWILIO_PHONENUMBER_ALPHA,
    #             to=numberTO)
    #         print((response.sid))
    #     except TwilioRestException as e:
    #         # logger.info('Exception occurred: {} '.format(e))
    #         print('Exception occurred: {} '.format(e))
    #         if e.code == 21612:
    #             self.messsagewithoutalias(numberTO, messagebody)
    #         else:
    #             return False
    #
    #
    # def messsagewithoutalias(self, numberTO, messagebody):
    #     try:
    #         client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
    #         response = client.messages.create(
    #             body=messagebody,
    #             from_=self.TWILIO_PHONENUMBER,       #TWILIO_PHONENUMBER_ALPHA,
    #             to=numberTO)
    #         print((response.sid))
    #     except TwilioRestException as e:
    #         # logger.info('Exception occurred: {} '.format(e))
    #         print('Exception occurred: {} '.format(e))
    #         return False