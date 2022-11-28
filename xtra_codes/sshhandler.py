import paramiko, threading, time

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
            data = self.shell.send(command + "\n")
            time.sleep(timing)
            print (data)
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
    