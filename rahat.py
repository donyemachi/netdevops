import napalm
import sys
import os

import argparse
from napalm import get_network_driver
from getpass import getpass
import json
from netmiko import Netmiko
from pprint import pprint as pp
import json


parser = argparse.ArgumentParser(prog= 'rahat.py', usage='%(prog)s device os username',description="login credentials & device type")
parser.add_argument('--device', help="hostname or IP",type=str,default=None  )
parser.add_argument('--device_type', help="device type", type=str, default=None)
parser.add_argument('--username', help="login name", type=str, default=None)
#parser.add_argument('password', help="password",type=str, default=None )

args = parser.parse_args()

host = args.device
driver = args.device_type
user = args.username

device_password = getpass(" SSH key password: ")
priv = getpass(" priviledge password: ")

optional_args = {'secret': priv}
device_driver = get_network_driver(driver)

commands = ['show ipv6 route']
#device = driver(
#        hostname=host,
#        username=user,
#        password=device_password,
     #   optional_args={"port": 12443},
#  )
    

with device_driver(hostname=host, username=user, password= device_password, optional_args=optional_args) as dev:
    dev.open()
    cmd = dev.cli(commands)
    info = dev. get_facts()
    info2 = dev.get_network_instances()
    info_json = json.dumps(info, sort_keys=True, indent=4)
    info2_json = json.dumps(info2, sort_keys=True, indent=4)
    info3_json = json.dumbs(cmd, sort_keys=True, indent=4)
    


print(info_json)  

print('get_network_instances' + '#######################################################')
print(info2_json) 

print('cmd' + '#######################################################')
print(info3_json) 
#print(info)
#pp(type(cmd))