import time, paramiko
class ssh:
    shell = None
    client = None

    def __init__(self, ip, username, password):
        print("Connecting to server on ip", str(ip) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(ip, username=username, password=password, look_for_keys=False)

    def open_shell(self):                   # Opens the shell
        self.shell = self.client.invoke_shell()

    def send_shell(self, command):          # Send commands to the shell
        if(self.shell):
            self.shell.send(command + "\n")
            time.sleep(1)
            output=str(self.shell.recv(4096),'utf-8')
            print (output)
            
        else:
            print("Shell not opened.")


def cisco_device_connect():
    username = "amar"
    password = "cisco"
    ip = '3.13.93.157'
    connection = ssh(ip, username, password)
    cmds = ['terminal len 0','dir | in bin', "show bootvar | in BOOT","dir flash: | in bytes"]
    connection.open_shell()
    for cmd in cmds:
        connection.send_shell(cmd)

cisco_device_connect()