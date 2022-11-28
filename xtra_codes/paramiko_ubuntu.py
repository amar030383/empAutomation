import paramiko, os, time
device = '3.19.131.3'
Username = os.environ.get('csr_usr')
Password = os.environ.get('csr_pwd')
'''
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conn = ssh_client.connect(hostname = device, username =Username, password=Password, port=22)
changeDIR = 'cd /tftp/'
#command = 'scp csr1000v-universalk9.17.02.03.SPA.bin amarjeet:cisco@ec2-3-13-93-157.us-east-2.compute.amazonaws.com:csr1000v-universalk9.17.02.03.SPA.bin'
cmd = ['pwd', 'cd /tftp','pwd' ,'ls -lrt']
for x in cmd:
    (stdin, stdout, stderr) = ssh_client.exec_command(x)
    output = (str(stdout.read(), 'utf-8'))
    print (x,output)
'''
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(device, username=Username, password=Password)

channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')
stdin.write('cd /tftp')
stdin.write('scp csr1000v.bin amar@3.13.93.157:csr1000vNew.bin')
stdin.write('yes')
stdin.write('cisco')
time.sleep(360)
output = (str(stdout.read(), 'utf-8'))
print (output)
