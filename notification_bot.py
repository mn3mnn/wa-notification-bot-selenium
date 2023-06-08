import json
import time

import pywhatkit

import requests
from bs4 import BeautifulSoup

import send_whatsapp_msg


events_from_first_site = []
items_from_second_site = []

# xml_text_false = '''<?xml version="1.0" encoding="utf-8"?>
# <string xmlns="http://tempuri.org/">[{"EventDatetime_arabic":null,"EventHour":"20:45 ","EventDate":"2023/6/08","EndDateTime":"2023/06/08 03:00:00 PM","DecreptedEventID":"Cb7Ub8iDAO4yI8RrPV1Ikg==","Minute":5,"EventDay":8,"EventMonth":"يونيو","TimeType":"م","IsOpend":true,"EventsID":5544,"EventTicketsCount":35865,"EventTicketsCountFree":0,"EnableSeasonalUsers":false,"FirstClubID":0,"SecondClubID":0,"EventDateTime":"2023-06-08T20:45:00","StadiumId":0,"StartTime":"0001-01-01T00:00:00","EndTime":"0001-01-01T00:00:00","FirstClubSeatPercentage":0,"SecondClubSeatPercentage":0,"KickOffAway":0,"KickOffHome":0,"KickOffOther":0,"MaxNumberOfTicktes":0,"IsEnabledforPurchase":false,"StopSellingBeforeHours":0,"Title":"حفل استقبال اللاعب العالمي","CompetitionId":0,"RelatedEventID":null,"EnableProfile":null,"EnableSuites":false,"PaymentTime":null,"EventImage":"","FirstClub":"الاتحاد","SecondClub":" ","stadiumName":"استاد مدينة الملك عبدالله - جدة ","category_Name_Arabic":"Sport","Comp_Name":"حفل استقبال اللاعب العالمي","FirstClubImage":"~/Assets/Images/Ittihad.png","SecondClubImage":"~/Assets/Images/BNZ.png","r":null}]</string>'''
#
# soup = BeautifulSoup(xml_text_false, 'xml')
# events_from_first_site = json.loads(soup.string)


def get_new_events(new: list, old: list):
    if len(new) > len(old):
        return list(set(new) - set(old))
    else:
        return []


def send_notification(message):
    global driver, numbers
    try:
        # recipient = '+201122960525'  # Replace with the recipient's phone number in the international format
        # pywhatkit.sendwhatmsg(recipient, message, time.localtime().tm_hour, time.localtime().tm_min + 1)
        send_whatsapp_msg.send_to_all(driver, message, numbers)
    except Exception as e:
        print("An exception occurred: ", e)


def check_first_site():
    global events_from_first_site

    # send post request to get the events
    resp = requests.post("https://ittihadclub.etickets.com.sa/HomeService/HomeService.asmx/GetEvents",
                         data={'UserID': '', 'CategoryID': '0', 'PageSize': '30', 'LastIndex': '0'})
    # Create a BeautifulSoup object from the XML text
    soup = BeautifulSoup(resp.text, 'xml')
    # Parse the JSON data
    curr_events = json.loads(soup.string)

    if not events_from_first_site:  # if events_from_first_site is empty (i.e. first run)
        events_from_first_site = curr_events
        return

    # if there is any new events that is not in events_from_first_site and its IsEnabledforPurchase prop is true
    new_events = get_new_events(curr_events, events_from_first_site)
    if new_events:
        for event in new_events:
            if event['IsEnabledforPurchase']:
                send_notification(f"New event opened: {event['Comp_Name']}")
                events_from_first_site.append(event)

    # check for any event in the current events that its IsEnabledforPurchase has changed from false to true
    # if any event is changed, send notification and update events_from_first_site
    for event in curr_events:
        if event['IsEnabledforPurchase']:
            # check if this event is in events_from_first_site and its IsEnabledforPurchase prop was false
            for old_event in events_from_first_site:
                if event['DecreptedEventID'] == old_event['DecreptedEventID'] and not old_event['IsEnabledforPurchase']:
                    send_notification(f"New event opened: {event['Comp_Name']}")
                    # update events_from_first_site
                    events_from_first_site.append(event)
                    events_from_first_site.remove(old_event)
                    break


def check_second_site():
    pass


def main():
    while True:
        try:
            check_first_site()
        except Exception as e:
            print("An exception occurred: ", e)
        try:
            check_second_site()
        except Exception as e:
            print("An exception occurred: ", e)

        time.sleep(30)


if __name__ == '__main__':
    numbers = send_whatsapp_msg.read_numbers()
    driver = send_whatsapp_msg.init_driver()
    send_whatsapp_msg.open_whatsapp(driver)

    # main()
    send_notification("New event opened: حفل استقبال اللاعب العالمي")
    time.sleep(5)
    send_notification("New event opened: مباراه الاتحاد والنصر")

    driver.quit()
