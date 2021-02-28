import paramiko
import random
from configparser import SafeConfigParser

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
import Packages.logging.log_file as log

def execute_random_command(ssh, commandlist):
    lines = open(commandlist).read().splitlines()
    command = random.choice(lines)
    stdin, stdout, stderr = ssh.exec_command(command)
    return command



def choose_ssh_server(serverlist):

    parser = SafeConfigParser()
    parser.read(serverlist)

    server = random.choice(parser.sections())


    host = parser[server]["ip"]
    port = parser[server]["port"]
    username = parser[server]["username"]
    password = parser[server]["password"]

    return host, port, username, password



def main(serverlist, commandlist):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host, port, username, password = choose_ssh_server(serverlist)

    ssh.connect(host, int(port), username, password)
    log.log_event("SSH;Connection established;"+host)

    for i in range (1, random.randint(1,5)):
        command = execute_random_command(ssh,commandlist)
        log.log_event("SSH; Execute Command;"+command)

    
    ssh.close()
    log.log_event("SSH;Connection closed;"+host)






