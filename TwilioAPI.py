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
        self.TWILIO_FLOW_SID = twilioconfig["TWILIO_FLOW_SID"]


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

    #######################################################
    #  Functions supporting Studio Flow
    #######################################################
    def studio_execute_flow(self, numbertocall, params):
        """
        Triggers a Twilio Studio Flow

        :param numbertocall: phone number: formatted as E.164 formatting "+11231234567"
        :param params: additional parameters to use in the Twilio Flow
        :return: Results of the FLOW execution
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

        #Use a parameter for which Twilio Flow to execute
        try:
            execution = client.studio.v1\
                .flows(self.TWILIO_FLOW_SID)\
                .executions\
                .create(to=numbertocall, from_=self.TWILIO_PHONENUMBER,
                        parameters=params)
            return execution
        except TwilioRestException as e:
            print("Exceptiono occurred: code: {} msg: {}".format(e.code, e.msg))
            return False

    def fetch_execution(self,execution_sid):
        """
        Return an single execution that was performed by a FLOW
        :param sid: specific flow sid of an executed FLOW
        :return: results of the flows execution
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

        try:
            #Use a parameter for which Twilio Flow to execute
            execution = client.studio.v1\
                .flows(self.TWILIO_FLOW_SID)\
                .executions(execution_sid)\
                .fetch()
            return execution
        except TwilioRestException as e:
            print("Exceptiono occurred: code: {} msg: {}".format(e.code, e.msg))
            return False

    def fetch_executioncontext(self,execution_sid):
        """
        Return the context of an execution instead of an executed FLOW
        :param sid: specific flow sid of an executed FLOW
        :return: results of the flows execution
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

        try:
            #Use a parameter for which Twilio Flow to execute
            execution_context = client.studio.v1\
                .flows(self.TWILIO_FLOW_SID)\
                .executions(execution_sid)\
                .execution_context()\
                .fetch()
            return execution_context
        except TwilioRestException as e:
            print("Exceptiono occurred: code: {} msg: {}".format(e.code, e.msg))
            return False

    def fetch_stepcontext(self,execution_sid, step_sid):
        """
        Return the context of a specific step
        :param execution_sid: specific flow sid of an executed FLOW
        :param step_sid: specific step side
        :return: results of the flows step
        """
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

        try:
            #Use a parameter for which Twilio Flow to execute
            step_context = client.studio.v1\
                .flows(self.TWILIO_FLOW_SID)\
                .executions(execution_sid)\
                .steps(step_sid)\
                .step_context()\
                .fetch()
            return step_context
        except TwilioRestException as e:
            print("Exception occurred: code: {} msg: {}".format(e.code, e.msg))
            return False
