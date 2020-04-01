import TwilioAPI as tapi
import pandas as pd


#################################
## Lookup end to end
# Importdata()
#       receives a text file of phone numbers
#       creates pandas dataframe and formats for data entry
# numbersIsValid()
#       performs Lookup and places data in dataframe
# savedata()
#       saves dataframe to csv file
###############################

def importdata(fullpathfilename, fullrun, start, stop):
    """
    Receives text file of phone numbers:
    Sets up file to receive information from Twilio Lookup
    :param fullpathfilename: full path to the file
    :param fullrun: Boolean: Determine whether to execute full file or partial
    :param start: if partial, start row
    :param stop: if partial, end row (won't be run)
    :return: pandas dataframe formatted for Twilio Lookup data entry
    """
    #create pandas dataframe from file
    data = pd.read_csv(fullpathfilename,
                       header=0,    #header is the first line
                       sep=",")
    #add columns and names
    data['VALID'] = ""
    data['AccountName'] = ""        ##{"caller_name":{"caller_name":"data"}}
    data['AccountType'] = ""        ##{"caller_name":{"caller_type":"data"}}
    data['Carrier'] = ""            ##{"carrier":{"name":"data"}}
    data['CarrierType'] = ""        ##{"carrier":{"type":"data"}}
    print("Number of records {}".format(data.count()))
    #print(data.head())
    if fullrun == True:     #whether to use ALL the data
        newdata = data
    else:
        newdata = data[start:stop]  #segment dataframe
    return newdata


def numbersIsValid(data):
    """
    Checks to see if a given phone number is valid : Twilio Lookup
    Receives a pandas datafrome
    Looks up data on a particular phone
    Adds validation information to the dataframe
    :param data: pandas dataframe
    :return: updated pandas dataframe
    """
    comms = tapi.TwilioAPI()
    #for ind in data:
    for index, row in data.iterrows():
        result = comms.is_valid_number(number=row['Mobile_Phone'])
        print("phone result {}:".format(result))
        if result == False:
            data.loc[index, 'VALID'] = "NOT VALID"
        else:
            try:
                data.loc[index, 'VALID'] = result
                data.loc[index, 'AccountName'] = result.caller_name["caller_name"]  ##{"caller_name":{"caller_name":"data"}}
                data.loc[index, 'AccountType'] = result.caller_name["caller_type"]  ##{"caller_name":{"caller_type":"data"}}
                data.loc[index, 'Carrier'] = result.carrier["name"]  ##{"carrier":{"name":"data"}}
                data.loc[index, 'CarrierType'] = result.carrier["type"]  ##{"carrier":{"type":"data"}}
            except Exception as e:
                print(e)
    print("done checking phones")
    #print(data)
    return data


def savedata(fullpathfilename, data):
    """
    Save data to a file: csv from a pandas dataframe
    :param fullpathfilename: Full path to the file
    :param data: pandas dataframe to save
    :return: True if successful, False if not
    """
    try:
        data.to_csv(fullpathfilename,
                    header=True
                    )
        return True
    except Exception as e:
        print('Exception occurred: {} '.format(e))
        return False

#################################
## Utilities:  testing utility functions
# find add-ons associated with the Twilio account
# test lookup function - provide a LIST of phone numbers
# test to send a SMS message
###############################
def findaddons():
    """
    Purpose: find add-ons associated with the Twilio account
    :return: print out of all Twilio add-on for connected account
    """
    comms = tapi.TwilioAPI()
    comms.add_ons_available()

def testnumbers(listofphonenumbers):
    """
    Purpose: Test identification of phones -
    * validates: what result returns is dependent on Twilio add-ons
    associated with SID account.
    :param listofphonenumbers: uses a list of phone strings  ['11112223333', '11234567890']
    :return: print out validation for specific phone
    """
    comms = tapi.TwilioAPI()
    for phone in listofphonenumbers:
        result = comms.is_valid_number(number=phone)
        print("{} is considered {}:".format(phone, result))
    print("done checking phones")

def sendamessage(phone, msg):
    """

    :param phone: phone number in string format '11234567890'
        * NOTE: internationall, use '+' with country code
    :param msg: SMS message to send
    :return: print Twilio response message
    """
    comms = tapi.TwilioAPI()
    response = comms.send_message(numberTO=phone,
                                  messagebody=msg)
    print(response)

if __name__=="__main__":
    #### Utility functions
    findaddons()
    testnumbers(listofphonenumbers=['', ''])
    sendamessage("enterphonenumber",
                 "This is a test of the COVID-19 messaging system.")
    #################
    ## Process to validate mobile phone text file
    # df= importdata(fullpathfilename='E:\\Covid19_Mobile_Phone.txt',
    #                fullrun=False, start=1200, stop=1300)   #row stop is not selected
    # df2 = numbersIsValid(df)
    # if savedata(fullpathfilename='rE:\validatedmobiledata13.csv',
    #             data=df2) == True:
    #     print("WooHoo - saved successfully")
    # else:
    #     print("Time to fix it - check exceptions")

