from netmiko import ConnectHandler
import time

Device = { 'device_type': 'cisco_ios', 'ip' : 'ec2-3-13-93-157.us-east-2.compute.amazonaws.com', 'username' : 'amar','password' : 'cisco' }

netconnect = ConnectHandler(**Device)
output = netconnect.send_command('show int desc',use_textfsm=True)
time.sleep(2)
for x in output:
    print(x)
