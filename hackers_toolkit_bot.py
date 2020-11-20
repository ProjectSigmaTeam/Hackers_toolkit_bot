# !/usr/bin/python3.6
# Hackers toolkit telegram bot
# developer : Khalil Abbas - Syria ( https://t.me/khalil_abbas )


import telepot
import time
import urllib3
from pprint import pprint
import requests
import json
import folium
import string
import random
import os
import sys
import shutil
import socket
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone


tmpchannelid = "-1001345765635"
admin = 676036252


render_api = "https://api.screenshotmachine.com/?key=xxxxxx&url={}/zzz.html&dimension=1024x768".format("#url")

# proxy section   -  use this section if you are using free account
# from pythonanywhere python hosting service provider (don't change
# proxy servers ) otherwise comment it .

# START PROXY SECTION
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# END PROXY SECTION

bot = telepot.Bot("TOKEN")
proxies = {'http':'http://proxy.server:3128','https':'https://proxy.server:3128'}
bot.sendMessage(tmpchannelid,"I'm on ")


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def get_ip_info(ip):
    url = "http://ip-api.com/json/{}".format(ip)
    response = requests.get(url,proxies=proxies).text
    return json.loads(response)

def get_pnone_info(msg):
    number = msg['text'].split(' ')[1]
    info = ''
    num = phonenumbers.parse(number)
    country_data = geocoder.description_for_number(num, "en")
    carrier_data = carrier.name_for_number(num, "en")
    timezone_data = timezone.time_zones_for_number(num)
    info = "[+] Details about {} :\nCountry : {}\ncarrier: {}\ntimezone: {}".format(number,country_data,carrier_data,timezone_data)
    return info



def generateRandomName(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
def log(msg):
    bot.forwardMessage(tmpchannelid,msg['chat']['id'],msg['message_id'])
def handle(msg):
    #pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        if (chat_id == 67603622):
            #load_admin_panel
            print("pass")
        else:
            command = msg['text'].split(' ')[0]
            if (command == "/start"):
                log(msg)
                bot.sendMessage(chat_id,"Welcome to Hackers toolkit bot \nsend /help to check commands list",reply_to_message_id=msg['message_id'])
            elif(command == "/iplocation"):
                log(msg)
                if (len(msg['text'].split(' ')) == 2):
                    ip = msg['text'].split(' ')[1]
                    if(validate_ip(ip)):
                        bot.sendMessage(chat_id,"[+] Getting ip info ..",reply_to_message_id=msg['message_id'])
                        raw_info = get_ip_info(ip)
                        info = ''
                        for i in raw_info.keys():
                            if ((i != "status") and (i != "query")):
                                info += "{}: {}\n".format(i,raw_info[i])
                        bot.sendMessage(chat_id,info)
                        bot.sendMessage(chat_id,"[*] Rendering ..")
                        zoom = 13
                        mprev = folium.Map(location=[raw_info["lat"],raw_info["lon"]],zoom_start=zoom)
                        folium.Marker(location=[raw_info['lat'],raw_info['lon']]).add_to(mprev)
                        tmpname = generateRandomName(30)
                        mprev.save("{}.html".format(tmpname))
                        tmpname2 = tmpname + ".html"
                        # send to log channel and get id and url
                        '''
                        files = {'fileToUpload': open(tmpname2,'rb')}
                        r = requests.post("http://xxxxxxxxxxxxxxxxx.000webhostapp.com/doupload.php", files=files,proxies=proxies)
                        print("FFFFFFFFFFF")
                        print(tmpname2)
                        docinfo = bot.sendDocument(tmpchannelid,open(tmpname2,'rb'))
                        file_id = docinfo['document']['file_id']
                        print("[VERBOSE] file_id : {}".format(file_id))
                        doc_link = "https://api.telegram.org/file/botxxxxxxxxxxxxxxxxxxxxxx/{}".format(bot.getFile(file_id)['file_path'])
                        print("[VERBOSE] doc_link : {}".format(doc_link))
                        '''

                        shutil.copy(tmpname2,"/home/xxxxxxxxxxx/tmpsite/media")

                        doc_link = "http://xxxxxxxxxxxxx.pythonanywhere.com/media/{}".format(tmpname2)
                        # generate png image
                        sshot = requests.get("https://api.screenshotmachine.com/?key=xxxxxxx&url={}&dimension=1024x768".format(doc_link),proxies=proxies).content
                        with open("{}.jpg".format(tmpname),"wb") as opw:
                            opw.write(sshot)
                        bot.sendMessage(chat_id,"[*] Generating map preview ..")
                        with open("{}.jpg".format(tmpname),"rb") as opread:
                            bot.sendPhoto(chat_id,("image.jpg",opread),caption="This preview was generated by @hackers_toolkit_bot\n~ ProjectSigma Team ~\n@ProjectSigmaTeam")
                        os.remove("{}.jpg".format(tmpname))
                        os.remove("/home/xxxxxxxxxxxxx/tmpsite/media/{}".format(tmpname2))
                    else:
                        bot.sendMessage(chat_id,"[-] Invalid ip format")
                else:
                    bot.sendMessage(chat_id,"[-] Invalid command format\nuse /iplocation [ip]")
            elif (command == '/help'):
                log(msg)
                bot.sendMessage(chat_id,"/host - get ip address of host or vice versa\n\n/iplocation - Get detailed information about ip address location and show on map\n\n/phone - Get information about phone number\n\n/help - show available commands\n\n\nDeveloper : @khalil_abbas\nProject Sigma Team\n@ProjectSigmaTeam",reply_to_message_id=msg['message_id'])
            elif (command == '/host'):
                log(msg)
                msgsplit = msg['text'].split(' ')
                if len(msgsplit) == 2:
                    #detect if it is a domain name or i
                    if (validate_ip(msgsplit[1])):
                        #try:
                        host_name = socket.gethostbyaddr(msgsplit[1])
                        tmpmsg = ''
                        for i in host_name:
                            tmpmsg = "{}{}\n".format(tmpmsg,str(i))
                        bot.sendMessage(chat_id, "[+] Host name of this ip address : {}".format(tmpmsg),reply_to_message_id=msg['message_id'])
                        #except:
                            #bot.sendMessage(chat_id, "[-] This ip address doesn't have a related domain name")
                    else:
                        try:
                            host_ip = socket.gethostbyname(str(msgsplit[1]))
                            bot.sendMessage(chat_id, "[+] ip adress of {} : {}".format(msgsplit[1],host_ip),reply_to_message_id=msg['message_id'])
                        except:
                            bot.sendMessage(chat_id, "[-] Invalid hostname",reply_to_message_id=msg['message_id'])
                else:
                    bot.sendMessage(chat_id, "[-] Invalid command format , use \n/host site.com",reply_to_message_id=msg['message_id'])
            elif(command == "/reboot"):
                log(msg)
                if(msg['from']['id'] == admin):
                    bot.sendMessage(chat_id, "Rebooting ...",reply_to_message_id=msg['message_id'])
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    bot.sendMessage(chat_id,"خراس 🙂  {}".format(msg['from']['id']),reply_to_message_id=msg['message_id'])
            elif(command == '/hack'):
                log(msg)
                msgsplit = msg['text'].split(' ')
                if (len(msgsplit) != 2):
                    bot.sendMessage(chat_id,"Invalid command format \nusage : /hack [site]",reply_to_message_id=msg['message_id'])
                else:
                    site = msgsplit[1]
                    bot.sendMessage(chat_id , "[*] Hacking {} ..".format(site),reply_to_message_id=msg['message_id'])
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[*] Testing connection to {} ..".format(site))
                    time.sleep(2)
                    bot.sendMessage(chat_id , "[+] Connected successfully !")
                    bot.sendMessage(chat_id , "[*] Method 1 : Trying to get stack trace via passive method ..")
                    time.sleep(5)
                    bot.sendMessage(chat_id , "[-] method 1 failed")
                    time.sleep(1)
                    bot.sendMessage(chat_id , "[*] Method 2 : Trying to get stack trace via active method ( less safe ) ..")
                    time.sleep(6)
                    bot.sendMessage(chat_id,"[+] Done ")
                    time.sleep(1)
                    bot.sendMessage(chat_id , "[*] Trying to trigger exploit by bruteforcing memory Return address ..")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] Trying 0xffc4b3c4 ..")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] Trying 0xffc4b3c5 ..")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] Trying 0xffc4b3c6 ..")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] Trying 0xffc4b3c7 ..")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] SUCCESS ! ")
                    time.sleep(1)
                    bot.sendMessage(chat_id , "[+] Spawning reverse shell ...")
                    time.sleep(3)
                    bot.sendMessage(chat_id , "Meterpreter session 1 opened {}:54835".format(socket.gethostbyname(site)))
                    time.sleep(3)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor ...")
                    time.sleep(4)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor (35%)")
                    time.sleep(2)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor (62%)")
                    time.sleep(2)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor (78%)")
                    time.sleep(2.5)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor (96%)")
                    time.sleep(3.7)
                    bot.sendMessage(chat_id , "[+] Uploading backdoor (100%)")
                    time.sleep(5)
                    bot.sendMessage(chat_id , "[+] Cleaning system logs ..")
                    time.sleep(4.4)
                    bot.sendMessage(chat_id , "[+] Done ! {} was hacked successfully ..".format(site))
            elif(command == "/phone"):
                if (len(msg['text'].split(' ')) == 2):
                    #try:
                    num = msg['text'].split(' ')[1]
                    number2 = phonenumbers.parse(num)
                    if (phonenumbers.is_valid_number(number2)):
                        bot.sendMessage(chat_id,get_pnone_info(msg))
                    else:
                        bot.sendMessage(chat_id,"[-] Invalid phone number")
                    #except:
                        #bot.sendMessage(chat_id,"[-] Invalid phone number")
                else:
                    bot.sendMessage(chat_id,"[-] Invalid command format\nuse /phone [number]")
            elif(command == "/gen_person"):
                bot.sendMessage(chat_id, "[+] generating fake person image ..",reply_to_message_id=msg['message_id'])
                pic = requests.get("https://thispersondoesnotexist.com/image",proxies=proxies).content
                bot.sendPhoto(chat_id, pic, caption="This image is not for a real person .. this person don't actually exist..\nthis is a fake picture generated with AI\n\ngenerated with @hackers_toolkit_bot\n@ProjectSigmaTeam")
bot.message_loop(handle)
print('listening ...')

while 1:
    time.sleep(10)
