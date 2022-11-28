import paramiko, time, os
device = 'ec2-3-13-93-157.us-east-2.compute.amazonaws.com'  # CSR1000v
#device = 'ec2-3-19-131-3.us-east-2.compute.amazonaws.com'   # FTP Server
#device = 'ec2-3-14-220-80.us-east-2.compute.amazonaws.com'  # Automation App
#device = '3.19.131.3'
Username = os.environ.get('csr_usr')
Password = os.environ.get('csr_pwd')
ios_cmd = ('show version | in cisco')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname = device, username = Username, password=Password, port=22, look_for_keys=False)
cmds =["show ip interface brief", "show ver | in cisco"] 
data = []
for ios_cmd in cmds:
    (stdin, stdout, stderr) = ssh_client.exec_command(ios_cmd)
    data.append(str(stdout.read(), 'utf-8'))
    #output = (str(stdout.read(), 'utf-8'))
    #print (output)
print (data)