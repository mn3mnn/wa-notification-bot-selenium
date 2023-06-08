# wa-notification-bot
send Whatsapp message to list of numbers when an event is added to any of these sites:
  
  1- Ittihad club site: https://ittihadclub.etickets.com.sa/Pages/Home.aspx?show=events

  2- (developing..)


- **NOTES**

  - you can easily add a new site to the bot by creating a new function for it and handle the logic for sending the notification, then call it in main function


- **Dependencies**

  - Google Chrome : I expect you've it already installed.

  - Chromedriver : download Chromedriver from the official download page, https://sites.google.com/a/chromium.org/chromedriver/downloads


- **Usage**

  1- open ```numbers.txt``` and write all numbers, each on a separate line. (include country code)
  
  2- make sure all requirements are installed 
  
  3- replace ```chromedriver.exe``` with compatible version of your chrome browser
  
  4- run ```notification_bot.py```
  
  5- scan the qr code to sign in to whatsapp web
  
  6- keep the script running, when there is a new event the message will be sent to all numbers
  
