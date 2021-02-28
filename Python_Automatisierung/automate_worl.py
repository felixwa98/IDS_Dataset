"""
Title: automate_work.py
Author: Felix Waschke
Version: 0.01
Date: 24.12.2020

----------------------------------------------------------------
Funktionsweise: Das Programm soll einen realistischen Netzwerkverker eines kleineren Unternehmens simulieren.

----------------------------------------------------------------
To-Do:
- Uhrzeit / Datumcheck
- http / https Aufrufe  
- VoIP
    - Umsetzung über Discord
- Server, ... Konfigurations

"""
# Importieren der diversen Pakteten
import Packages.browsing.browsing_file as browsing
import Packages.ssh.ssh_file as ssh
import Packages.email.email_file as email
import Packages.voip.voip_file as voip
import Packages.ftp.ftp_file as ftp
import Packages.logging.log_file as log

# Importieren von Python Packteten
from configparser import SafeConfigParser
from datetime import datetime, date
import random
import time
import sys
import socket
import os

# Configuration Server
configfile = "init_config.txt"

main_config = "server"

# Initialize the lunch flag
# Is set to true at the start of the lunch break and reset at the start of each working day
hadLunchToday = False

def get_time():
    localtime = time.localtime(time.time())

    timestamp = time.asctime(localtime)

    return timestamp

def get_Date():
    localtime = time.localtime(time.time())

    year = localtime[0]
    month = localtime[1]
    day = localtime[2]

    hour = localtime[3]
    minute = localtime[4]

    datestamp = str(year) + str(month) + str(day)+ str(hour)+ str(minute)

    return datestamp

def get_day():
    localtime = time.localtime(time.time())

    day = localtime[6]

    # 0 is Monday, ... , 6 is Sunday
    return day


def getSubnetHostAndHostname():
	# Determine IP 
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com", 80))
	ip = (s.getsockname()[0])
	s.close()
	
	# Determine Subnet using IP AAAA.BBBB.CCCC.DDDD -> CCCC
	subnet = ip.split('.')[2]
	
	# Determine host part of the IP AAAA.BBBB.CCCC.DDDD -> DDDD
	host = ip.split('.')[3]
	
	# Determine host name 
	hostname = socket.gethostname()
	
	return subnet, host, hostname, ip

def get_configfile():
    # Collect Konfiguration Data
    global configfile

    init_config_parser = SafeConfigParser()
    init_config_parser.read(configfile)

    # Get FTP Server IP
    ftp_server = init_config_parser.get('FTP', 'Server-IP')
    ftp_username = init_config_parser.get('FTP', 'Username')
    ftp_password = init_config_parser.get('FTP', 'Password')
    ftp_file = getSubnetHostAndHostname()[3] + '.config'

    # Suchen nach der hinterlegten config dateiert
    check = ftp.download_file(ftp_server,ftp_file,ftp_file,ftp_username,ftp_password)

    # Datei neues erstellen

    if (not check):
        check = ftp.download_file(ftp_server,"master.config",ftp_file,ftp_username,ftp_password)

        if (check):
            # Erstellen der Einstellung der neuen Konfig Datei
            config_parser = SafeConfigParser()
            config_parser.read(ftp_file)

            host_information = getSubnetHostAndHostname()
            config_parser.set('DEFAULT','Hostname',host_information[2])
            config_parser.set('DEFAULT','Subnet',host_information[0])
            config_parser.set('DEFAULT','Hostid',host_information[1])
            config_parser.set('DEFAULT','IP-Addresse',host_information[3])
            log.log_event("System;New Configfile created")
            put_configfile()





        else:
            # Fehler, warscheinlich keine Verbindung zum FTP Server
            log.log_event("System;Connection to Configfile FTP refused.")

    
    # Update the inital configuration file
    # check = ftp.download_file(ftp_server,configfile,configfile,ftp_username,ftp_password)
    # log.log_event("System;Config Loaded")

    # Get Other Konfiguration Files 


def put_configfile():
    global configfile

    init_config_parser = SafeConfigParser()
    init_config_parser.read(configfile)

    # Get FTP Server IP
    ftp_server = init_config_parser.get('FTP', 'Server-IP')
    ftp_username = init_config_parser.get('FTP', 'Username')
    ftp_password = init_config_parser.get('FTP', 'Password')
    ftp_file = getSubnetHostAndHostname()[3] + '.config'

    check = ftp.upload_file(ftp_server,ftp_file, ftp_file, ftp_username, ftp_password)
    if (check):
        log.log_event("System;Upload of Configfile successfully")

def put_logfile():

    global configfile

    init_config_parser = SafeConfigParser()
    init_config_parser.read(configfile)

    # Get FTP Server IP
    ftp_server = init_config_parser.get('FTP', 'Server-IP')
    ftp_username = init_config_parser.get('FTP', 'Username')
    ftp_password = init_config_parser.get('FTP', 'Password')
    ftp_file =  "log/" + get_Date()  + getSubnetHostAndHostname()[3] + '.log'
    # Upload the log file to FTP Server
    check = ftp.upload_file(ftp_server,"C:\\log.csv", ftp_file , ftp_username, ftp_password)
    if (check):
        log.log_event("System;Upload of Logfile successfully")

def get_general_config():

    init_config_parser = SafeConfigParser()
    init_config_parser.read(configfile)

    # Get FTP Server IP
    ftp_server = init_config_parser.get('FTP', 'Server-IP')
    ftp_username = init_config_parser.get('FTP', 'Username')
    ftp_password = init_config_parser.get('FTP', 'Password')


    # Download the Browsing configuration
    ftp.download_bulk(ftp_server, "BROWSING/", "C:\\Config\\http\\", ftp_username, ftp_password)

    # Download the email configuration
    ftp.download_bulk(ftp_server, "EMAIL/", "C:\\Config\\smtp\\", ftp_username, ftp_password)

    # Download the ftp configuration
    ftp.download_bulk(ftp_server, "FTP/", "C:\\Config\\ftp\\", ftp_username, ftp_password)

    # Download the ssh configuration
    ftp.download_bulk(ftp_server, "SSH/", "C:\\Config\\ssh\\", ftp_username, ftp_password)

    # Download the voip configuration
    ftp.download_bulk(ftp_server, "VOIP/", "C:\\Config\\voip\\", ftp_username, ftp_password)




def check_for_break():
    global hadLunchToday
    curHour = 0
    time_for_lunch = False

    # Time for Lunch
    try:
	    curHour = int(datetime.now().strftime("%H"))
    except:
        curHour = 8
    
    if (curHour >= 11 and curHour <= 13 and not hadLunchToday):

        if random.randint(1, 10) >= 9:
            break_time = random.randint(20,40)
            
             
            hadLunchToday = True
        else:
            # Make a regular break
            break_time = random.randint(1,10)
    else:   
        # Make a regular break
            break_time = random.randint(1,10)
    
    # Take the break 
    log.log_event("Break;Took a Break;" + str(break_time))
    time.sleep(break_time * 60)




def main():
    try:
        get_configfile()
        put_configfile()
    except:
        log.log_event("System; Error with load config")

    try:
        get_general_config()
    except:
        log.log_event("System; Error with load general config")

    try:
        put_logfile()
    except:
        log.log_event("System; Error Upload the latest log")
    

    main_parser = SafeConfigParser()
    main_parser.read(getSubnetHostAndHostname()[3] + '.config')

    browsing_active = main_parser['WORKING']['browsing_active']
    email_active = main_parser['WORKING']['email_active']
    ftp_active = main_parser['WORKING']['ftp_active']
    ssh_active = main_parser['WORKING']['ssh_active']
    voip_active = main_parser['WORKING']['voip_active']
    break_active = main_parser['WORKING']['break_active']

    count_activity = int(browsing_active) + int(email_active) + int(ftp_active) + int(ssh_active) + int(voip_active) + int(break_active)

    activity = []
    for i in range(0,int(browsing_active)):
        activity.append("browsing")
    #for i in range(0,int(email_active)):
    #    activity.append("email")
    for i in range(0,int(ftp_active)):
        activity.append("ftp")
    for i in range(0,int(ssh_active)):
        activity.append("ssh")
    for i in range(0,int(voip_active)):
        activity.append("voip")
    for i in range(0,int(break_active)):
        activity.append("break")

    log.log_event("System;Starting Activities")

    while (True):
        try:
            random_activity = random.choice(activity)

            if (random_activity == "browsing"):
                browsing.main(main_parser["Browsing"]["videolist"], main_parser["Browsing"]["searchlist"], main_parser["Browsing"]["newslist"])
            elif (random_activity == "email"):
                email.main(main_parser["EMAIL"]["smtpserver"],main_parser["EMAIL"]["destinationaddresslist"],main_parser["EMAIL"]["bodylist"],main_parser["EMAIL"]["subjectlist"],main_parser["EMAIL"]["attachmentslist"])
            elif (random_activity == "ftp"):
                ftp.main(main_parser["FTP"]["server_list"],main_parser["FTP"]["file_list"])
            elif (random_activity == "ssh"):
                ssh.main(main_parser["SSH"]["server_list"], (main_parser["SSH"]["command_list"]))
            elif (random_activity == "voip"):
                voip.main(main_parser["Voip"]["music_list"])
            elif (random_activity == "break"):
                check_for_break()
            else:
                log.log_event("System;The activity is not valid" + random_activity)

            # Waits between two actions a bit, it wait between 0s and 2min
            time.sleep(random.randint(0,120))

        except:
            log.log_event("System;Error while Activities")
            
main()
        


    






    
            



        
        

    
    

