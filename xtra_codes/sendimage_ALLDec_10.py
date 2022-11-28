import threading, paramiko, time, re

fulldata=''

class sshHandler:
    shell = None
    client = None
    transport = None

    def __init__(self, ip, username, password):
        print("Connecting to server on ip", str(ip) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(ip, username=username, password=password, look_for_keys=False)
        self.shell = self.client.invoke_shell()
        self.transport = paramiko.Transport((ip, 22))
        self.transport.connect(username=username, password=password)
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def send_shell(self, command, timing):          # Send commands to the shell
        if(self.shell):
            self.shell.send(command + "\n")
            time.sleep(timing)
        else:
            print("Shell not opened.")
    
    def process(self):
        global strdata, fulldata
        while True:
            if self.shell is not None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                fulldata = fulldata + str(alldata)
    
             
def findimageuploadStatus(image_name, output):
    data = re.findall(rf'({image_name}\s+(\d+)%\s+\w+)\s+', output)
    last_match = str(data[-1])
    if '100%' in last_match:
        print ('Image uploaded successfully\n'+last_match)
    else:
        print ('Image uploaded failed, please increase the timing if the result if not 100%\n'+last_match)

def tftp_image_upload():
    tftp_ip = '3.19.131.3'
    tftp_username = "amar"
    tftp_password = "cisco"
    image_name = 'csr1000v.bin'
    #image_name = 'file.bin'
    device_ip = '3.13.93.157'
    device_username = 'amar'
    device_password = 'cisco'
    connection = sshHandler(tftp_ip, tftp_username, tftp_password)
    send_image = 'scp '+image_name+' '+device_username+'@'+device_ip+':'+image_name
    changeDir = 'cd /tftp'
    timing = 6*60
    commands = {changeDir:1, send_image:1, device_password:timing}
    for cmd in commands:
        connection.send_shell(cmd , commands[cmd])

    findimageuploadStatus(image_name, fulldata)

def cisco_device_connect():
    username = "amar"
    password = "cisco"
    ip = '3.13.93.157'
    connection = sshHandler(ip, username, password)
    cmds = ['terminal len 0','dir | in bin', "show bootvar | in BOOT","dir flash: | in bytes"]
    connection.open_shell()
    for cmd in cmds:
        connection.send_shell(cmd)
    print(type(fulldata))  # This contains the complete data received.

    #print(str(fulldata, 'utf-8'))   # This contains the complete data received.
    connection.close_connection()

tftp_image_upload()