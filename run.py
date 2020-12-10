#Importing needed libraries
import requests
import re
import urllib.request  as urllib2
from datetime import datetime
from instabot import Bot
import time

accounts = ["https://www.instagram.com/account/", "https://www.instagram.com/account2/"]
regex = [r"\"display_url\":\"(.*?)\":\"(.*?)\\u0026(.*?)\\u0026(.*?)\\u0026(.*?)\\u0026(.*?)\"", r"\"thumbnail_src\":\"(.*)", r"{\"node\":{\"text\":\"(.*?)\"}}", r"username\":\"(.*?)\"},\"is_video", r"oe=(.*)"]

def basicregex(regex, data, type):
    url = ""
    for match in enumerate(re.finditer(regex, data, re.MULTILINE), start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if(type == 1):
                return match.group(groupNum)
            if(type == 2):
                url += str(match.group(groupNum)) #Appending the matches to our final url
                if groupNum == len(match.groups()):   
                    return url
                else:
                    url = url[:-1]
                    url += "&" #Appending the & symbol after we add another match for the url to be valid  
        if(type == 0):   
                return match.group(groupNum)
            
bot = Bot()
bot.login(username = "YOUR USERNAME", password = "YOUR INSTAGRAM PASSWORD")

while True:
    for i in range(0,len(accounts)):
        time.sleep(4)

        finalname = "Via @"
        working_url = ""
        can_write = True

        url = accounts[i] #Getting the latest post url
        page = urllib2.urlopen(url)
        data = page.read()

        working_url = basicregex(regex[0], str(data), 2)
        description = basicregex(regex[2], str(working_url), 0)
        name = basicregex(regex[3], str(working_url), 1)
        working_url = basicregex(regex[1], str(working_url), 1)
        photo_index = basicregex(regex[4], str(working_url), 0)
                            
        finalname += "" if name is None else name
        finalname += ": "
        finalname += "" if description is None else description

        file1 = open("stranky.txt","r") #Text file manipulation
        for line in file1.readlines():
            if(line.strip() == photo_index):
                can_write = False
        file1.close()

        if(can_write == True):
            file1 = open("stranky.txt","a") 
            file1.write("{}\n".format(photo_index))
            file1.close()
            momentalni_cas = datetime.now().strftime("%d-%m-%Y %H-%M-%S") #Getting the current datetime and passing it into a string variable and declaring the filename of the downloaded image
            filename = 'imgs/INSTADOWNLOAD - ' + str(momentalni_cas) + '.jpg'
            r = requests.get(working_url, allow_redirects=True) #Downloading and saving the image
            open(filename, 'wb').write(r.content)
            print("File downloaded succesfully")
            bot.upload_photo(filename, finalname) #Uploading the image with our caption
            print("BOT JUST UPLOADED A PHOTO")
