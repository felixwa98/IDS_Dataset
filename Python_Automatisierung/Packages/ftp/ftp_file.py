import ftplib
from subprocess import Popen, check_output
from configparser import SafeConfigParser
from datetime import datetime, date
from queue import Queue
from uuid import getnode
import random
import threading
import time
import platform
import sys
import socket
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
import Packages.logging.log_file as log


def download_file(server, filename, download_path, username, password):

    # Connect to FTP Server
    try:
        f = ftplib.FTP(server)
        f.login(username, password)

        local_file = open(download_path, 'wb')
        f.retrbinary('RETR ' + filename, local_file.write, 1024)
        local_file.close()

        f.quit()
        log.log_event("FTP;Down File;"+ filename+ ";" + server)

        return True
    except:
        # Connection Error
        log.log_event("FTP;Connection Error")
        return False

    
def download_bulk(server, directory, download_path, username, password):

        # Connect to FTP Server
    try:
        f = ftplib.FTP(server)
        f.login(username, password)

        filenames = f.nlst(directory)

        for filename in filenames:
            local_filename = os.path.join(download_path, filename.split('/')[-1])
            file = open(local_filename, 'wb')
            f.retrbinary('RETR '+ filename, file.write)

            file.close()


        f.quit()
        log.log_event("FTP;Download Dir;"+ directory+ ";" + server)

        return True
    except:
        # Connection Error
        log.log_event("FTP;Connection Error")
        return False

    


def upload_file(server, filename, upload_path, username, password):
    # Connect to FTP Server
    try:
        f = ftplib.FTP(server)
        f.login(username, password)

        f.storbinary('STOR '+ upload_path, open(filename, 'rb'))

        f.quit()
        log.log_event("FTP;Upload File;"+ filename + ";" + server)
        return True
    except:
        # Connection Error
        log.log_event("FTP;Connection Error")
        return False


def choose_server(serverlist):
    parser = SafeConfigParser()
    parser.read(serverlist)

    server = random.choice(parser.sections())


    host = parser[server]["ip"]
    username = parser[server]["username"]
    password = parser[server]["password"]

    return host, username, password

def choose_file(filelist):
    lines = open(filelist).read().splitlines()
    file_name = random.choice(lines)
    return file_name


def main(serverlist, filename):

    host, username, password = choose_server(serverlist)

    for i in range (1, random.randint(1,5)):
        if (1 == random.randint(0,2)):
            # Upload Files
            datei = choose_file(filename)
            upload_file(host, datei, datei, username, password)
        else:
            # Download Files
            datei = choose_file(filename)
            download_file(host, datei, datei, username, password)

 