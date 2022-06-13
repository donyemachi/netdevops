from getpass import getpass
from pprint import pprint
import datetime
import json
from napalm import get_network_driver
from netmiko import juniper
from netmiko import ConnectHandler,ssh_exception
from getpass import getpass
import openpyxl
from datetime import datetime
from time import gmtime, strftime
#import os
#import pprint
import argparse
import copy
from datetime import datetime
import time
import pandas as pd
from netmiko import Netmiko
from getpass import getpass
import re

vlan_id = [2,200,202,10,14,1901,1902,103,21,22,23,25,26,99,5,101,6,104,105,106,107,108,109,110,111,112,116,118,128,129,130,152,160,176,192,340,350,360,370,380,390,401,402,403,410,411,412,413,420,421,404,405,432,440,450,460,470,480,490,540]
vlan_name = ['ADLS','Security','QF-BMS','PABX/VoIP','NY Printers','RP4VM - Data (Dell - Internal VLANs)','RP4VM - Replication (Dell - Internal VLANs)','Load Balancer','Scientific Computing - Heart Beat','Scientific Computing - Public Mgmt','Scientific Computing - VPN','Scientific Computing - TSM Backup','Research - Backbone','Management WiFi','Management LAN','Cluster Management - Heatbeat','Management2','vSphere vMotion','vSan','Research Lab Patched Network','Racknet - SSID','Research-Lab-Network','Research Monitoring System','Printers','Open WiFi','Employees SSID','exam SSID','edls SSID','eduroam SSID','IoT','Extron VLAN for AV Team','Guest SSID','BYOD SSID - Students','BYOD SSID - Employees','Dual-Stack - IPv6','Private-Admin-1','Private-Admin-2','Private-Admin-4','Private-Student-1','Private-Student-2','Private-Admin-3','Trust (Inside)','DMZ - 1','DMZ - 2','Backbone 1','Backbone 2','Backbone 3','Backbone 4','Backbone 5',	'Backbone 6','DMZ - SC','DMZ-EXT','VPN','Admin 1','Admin 2','Admin 4','Student 1','Student 2','Admin 3','Audio Visual-1']

user_vlans = ['Admin 1', 'Admin 2', 'Admin 3', 'Admin 4', 'Private-Admin-1', 'Private-Admin-2', 'Private-Admin-3', 'Private-Admin-4']
parser = argparse.ArgumentParser(prog= 'switch_inventory.py', usage='%(prog)s device username',description="login credentials")

vlan_detail = {9: 'IDM-POC ', 1: 'default ', 124: 'Students ', 75: 'QFLink', 530:'Research', 115: 'Admin-3-Test', 2: 'ADLS', 200: 'Security', 202: 'QF-BMS', 10: 'PABX/VoIP', 14: 'NY Printers', 1901: 'RP4VM - Data (Dell - Internal VLANs)', 1902: 'RP4VM - Replication (Dell - Internal VLANs)', 103: 'Load Balancer', 21: 'Scientific Computing - Heart Beat', 22: 'Scientific Computing - Public Mgmt', 23: 'Scientific Computing - VPN', 25: 'Scientific Computing - TSM Backup', 26: 'Research - Backbone', 99: 'Management WiFi', 5: 'Management LAN', 101: 'Cluster Management - Heatbeat', 6: 'Management2', 104: 'vSphere vMotion', 105: 'vSan', 106: 'Research Lab Patched Network', 107: 'Racknet - SSID', 108: 'Research-Lab-Network', 109: 'Research Monitoring System', 110: 'Printers', 111: 'Open WiFi', 112: 'Employees SSID', 116: 'exam SSID', 118: 'edls SSID', 128: 'eduroam SSID', 129: 'IoT', 130: 'Extron VLAN for AV Team', 152: 'Guest SSID', 160: 'BYOD SSID - Students', 176: 'BYOD SSID - Employees', 192: 'Dual-Stack - IPv6', 340: 'Private-Admin-1', 350: 'Private-Admin-2', 360: 'Private-Admin-4', 370: 'Private-Student-1', 380: 'Private-Student-2', 390: 'Private-Admin-3', 401: 'Trust (Inside)', 402: 'DMZ - 1', 403: 'DMZ - 2', 410: 'Backbone 1', 411: 'Backbone 2', 412: 'Backbone 3', 413: 'Backbone 4', 420: 'Backbone 5', 421: 'Backbone 6', 404: 'DMZ - SC', 405: 'DMZ-EXT', 432: 'VPN', 440: 'Admin 1', 450: 'Admin 2', 460: 'Admin 4', 470: 'Student 1', 480: 'Student 2', 490: 'Admin 3', 540: 'Audio Visual-1', 888:' NYTVLAN'}
interface_status = {'True':'Interface_Up', 'False' : 'Interface_Down'}
speeds = {-1:'NA'}

parser.add_argument('--device', help="hostname or IP",type=str,default=None  )
parser.add_argument('--username', help="login name", type=str, default=None)
#parser.add_argument('password', help="password",type=str, default=None )

args = parser.parse_args()

host = args.device
user = args.username


junos_driver = get_network_driver("junos")

junos_password = getpass(" SSH key password: ")

def convert1(seconds):
    return time.strftime("%H_%M_%S", time.gmtime(seconds))

def convert2(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d_%02d_%02d" % (hour, minutes, seconds)
    
def ConvertSectoDay(n):
 
    day = n // (24 * 3600)
 
    n = n % (24 * 3600)
    hour = n // 3600
 
    n %= 3600
    minutes = n // 60
 
    n %= 60
    seconds = n
    
    return "%02d_%02d_%02d" % (day, hour, seconds)

a = 86400
def period(n):
    days = n//a
    day = int(days)
    hrs = ((n/a) - (n//a)) * 24
    hr, mins = divmod(hrs, 1)
    hour = int(hr)
    minu = int(60 * mins)
    minn, sec = divmod(minu, 1)
    minute = int(minn)
    seconds = int(sec*60)
    second = int(seconds)
    #return "%02d_%02d_%02d" % (day, hour, minute, second)
    return (day, hour, minute)

a = 86400
def period1(n):
    days = n//a
    
    if n < 0:
        return "NA"
    
    elif days >= 7:
        week = days//7 # rem is days
        dayy = (days/7) - week # remainder above
        da, hr = divmod(dayy, 1)
        hour= int(hr)
        day = int(da)
        minu = 60 * hr
        minn, sec = divmod(minu, 1)
        minute = int(round(minu))
        return week, day, hour, minute
        
    else:
        week = 0
        hrs = ((n/a) - (n//a)) * 24
        hr, mins = divmod(hrs, 1)
        hour = int(hr)
        minu = 60 * mins
        minn, sec = divmod(minu, 1)
        minute = int(minn)
        seconds = round(sec*60)
        return week, days, hour, minute

def rep(txt):
  txt, n = re.subn(':', '', txt)
  return txt
  

def rep2(txt):
    return txt.replace(':', '')

def rep22(func):
    def inner(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        #str = args
        unwanted = ['ae0.0', 'ae1.0']
        #list1 = [ele for ele in str if ele not in unwanted]
        for txx in returned_value:
        #    del txt[unwanted]
            if txx in unwanted:
                returned_value.remove(txx)
        aaa = returned_value
        delim = ", "
        #listToStr = ' '.join([str(elem) for elem in aaa])
        temp = list(map(str, aaa))
        joined_string = delim.join(temp)
        return joined_string
        #return returned_value
        #    txt.remove(tx)
    return inner

@rep22  
def rep12(strr):
    unwanted = ['ae0.0', 'ae1.0']
    #list1 = [ele for ele in str if ele not in unwanted]
    for tx in strr:
    #    del txt[unwanted]
        if tx in unwanted:
            strr.remove(tx)
        #    txt.remove(tx)
    return strr
    
    
def rep3(txt):
    #return txt.replace(':', '')    
    char_to_replace = {'ae0.0': '', 'ae1.0': ''}
# Iterate over all key-value pairs in dictionary
    for key, value in char_to_replace.items():
    # Replace key character with value character in string
        sample_string = sample_string.replace(key, value)
    return txt    

with junos_driver(hostname=host, username=user, password=junos_password) as dev:
    dev.open()
    info = dev.get_interfaces()
    dev_info = {'interface': [entry1 for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            'mac-address': [entry2['mac_address'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            'status' : [entry2['is_up'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            'Flap(Weeks, Days, hour, minutes)' : [entry2['last_flapped'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
                  
            'Speed' : [entry2['speed'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            'MTU' : [entry2['mtu'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            'DESC' : [entry2['description'] for entry1, entry2 in info.items()if entry1 != 'ae0.0'],
            }
            
    mac_table = dev.get_mac_address_table()
    mac_data = {'mac':  [entry['mac'] for entry in mac_table if entry['interface'] != 'ae0.0'],
            'interface': [entry['interface'] for entry in mac_table if entry['interface'] != 'ae0.0'],
            'vlan': [entry['vlan'] for entry in mac_table if entry['interface'] != 'ae0.0']
#            'Last_flap': [entry['last_move'] for entry in mac_table if entry['interface'] != 'ae0.0']
            }
            
    vlan_infos =dev.get_vlans()
    #v_names = vlan_infos.value()
    vlan_info = { 'vl_name': [entry3 for entry3, entry4  in vlan_infos.items()],
                  'interfaces': [entry4['interfaces'] for entry3, entry4  in vlan_infos.items()]}
                
            
            
            

df21 = pd.read_excel('mac_raw.xlsx', sheet_name='All')
df22 = df21[df21.columns[~df21.columns.isin(['ActiveIPAddress','CWID','PrivateIPMigrationStatus', 'CanBeWired', 'CanBeWireless', 'WirelessConnected', 'WirelessConnectedPCName', 'DeviceStatus', 'Label', 'Migrate to Employees Wifi', 'Migrate to Private IP VLAN'])]]
df23 = copy.deepcopy(df22)
df24 = df23[df23.columns[~df23.columns.isin(['HostName','WifiMacAddress','DeviceTag', 'User', 'Department', 'DeviceModel', 'DeviceType', 'DeviceLocation'])]]
df25 = df24[["EthernetMacAddress","AddressName"]] 

user_det = df25.set_index('EthernetMacAddress').to_dict()['AddressName']

df36 = pd.DataFrame(vlan_info, columns=list(vlan_info.keys()))
df36['access_interfaces'] = df36.apply(lambda row: rep12(row['interfaces']), axis = 1)
df36['vlan name'] = df36['vl_name'].astype(int)
df36['vlan name'].replace(to_replace=vlan_detail, inplace=True)

df37 = df36[["vlan name","access_interfaces"]] 


#df['eq'] = df.apply(lambda row: row['coname1'] == row['coname2'], axis=1).astype(int)
df6 = pd.DataFrame(mac_data, columns=list(mac_data.keys()))
df = pd.DataFrame(dev_info, columns=list(dev_info.keys()))
#df6['user_mac'] = df6['mac'].replace(':', '')
df6['user_mac'] = df6.apply(lambda row: rep2(row['mac']), axis = 1)
df['speeds'] = df['Speed'].astype(int)
df['speeds'].replace(to_replace=speeds, inplace=True)
#['Speed'].replace(to_replace= {'-1': 'NA'}, inplace=True).astype(str)
#df['Flap'] = df.apply(lambda row: row['Flap'] == convert(int(row['Flap'])), axis = 1)
df['Flaps(Weeks, Day, hour, minutes)'] = df.apply(lambda row: period1(int(row['Flap(Weeks, Days, hour, minutes)'])), axis = 1)
df11 = copy.deepcopy(df)
#df11['Intf_status'] = df11.apply(lambda row: row['Intf_status'] == row['status'], axis=1).astype(int)



#df['status'].astype(str)
df['status'].astype(str).replace(to_replace=interface_status, inplace=True)

df11['port_status'] = df['status'].astype(str)
df11['port_status'].replace(to_replace=interface_status, inplace=True)
df12 = df11[df11.columns[~df11.columns.isin(['status', 'mac-address', 'MTU', 'Flap(Weeks, Days, hour, minutes)' ,'Speed'])]]
df0 = df11[df11.columns[~df11.columns.isin(['status', 'Flap(Weeks, Days, hour, minutes)', 'Speed'])]]
df9 = df.set_index('status')
 #df.sort_values("city08")
df13 = df12.set_index('interface').sort_values('port_status', ascending=False)
#df7 = df.groupby('status')[['interface', 'Flap']].rename({'Flap': 'Last_interface_Flap'},axis = 'columns')
df6['vlan name'] = df6['vlan']

df6['user detail'] = df6['user_mac']

df6['vlan name'].replace(to_replace=vlan_detail, inplace=True)

df6['user detail'].replace(to_replace=user_det, inplace=True)

#rslt_df = df6.loc[df6['vlan name'] in user_vlans ]
rslt_df = df6[df6['vlan name'].isin(user_vlans) ]

user_df = rslt_df[rslt_df.columns[~rslt_df.columns.isin(['user_mac'])]]


df2 = copy.deepcopy(df6)
#df3 = df2.groupby('vlan name')[['mac','interface']].count()
df4 = df2.groupby('vlan name')[['mac']].count().rename({'mac': 'users'},axis = 'columns')
#df13 = df.groupby('vlan name')[['mac','interface']].count()

current_datetime = datetime.now()
date_time = current_datetime.strftime("%m_%d_%Y - %H_%M_%S")
str_time = str(date_time)
filename = 'report' +' ' + str_time + '.xlsx'
file = str(filename)

with pd.ExcelWriter(file,  engine='xlsxwriter') as writer3:


    df4.to_excel(writer3, sheet_name="VLAN_counts", index=True)
    user_df.to_excel(writer3, sheet_name="end-user_counts", index=False)
    df6.to_excel(writer3, sheet_name="overall_user_Details", index=False)
    df25.to_excel(writer3, sheet_name="mac_Details", index=False)
    df37.to_excel(writer3, sheet_name="Port -to-Vlan_mapping", index=False)
    df13.to_excel(writer3, sheet_name="overall-port count", index=True)
    df0.to_excel(writer3, sheet_name="Raw_Interf_Data", index=False)
    
    
    
    #df4.to_excel(writer3, sheet_name="user_counts", index=True)
    
    #df12.to_excel(writer3, sheet_name="port_count", index=True)
    #df9.to_excel(writer3, sheet_name="active_port_count3", index=True)


#print(user_det)