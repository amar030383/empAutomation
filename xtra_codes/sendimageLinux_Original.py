import threading, paramiko, time

strdata=''
fulldata=''

class ssh:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def close_connection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def open_shell(self):
        self.shell = self.client.invoke_shell()

    def send_shell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
            time.sleep(1)
        else:
            print("Shell not opened.")

    def process(self):
        global strdata, fulldata
        while True:
            if self.shell is not None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = strdata + str(alldata)
                fulldata = fulldata + str(alldata)
                strdata = self.print_lines(strdata) # print all received data except last line

    def print_lines(self, data):
        last_line = data
        if '\n' in data:
            lines = data.splitlines()
            for i in range(0, len(lines)-1):
                print(lines[i])
            last_line = lines[len(lines) - 1]
            if data.endswith('\n'):
                print(last_line)
                last_line = ''
        return last_line

sshUsername = "amar"
sshPassword = "cisco"
sshServer = '3.19.131.3'

connection = ssh(sshServer, sshUsername, sshPassword)
#cmd = 'scp csr1000v-universalk9.17.02.03.SPA.bin amar@3.13.93.157:csr1000v-universalk9.17.02.03.SPA.bin'
cmd = 'scp csr1000v.bin amar@3.13.93.157:csr1000v.bin'
connection.open_shell()
connection.send_shell('cd /tftp')

connection.send_shell(cmd)
connection.send_shell('cisco')
time.sleep(360)
print(fulldata)   # This contains the complete data received.
connection.close_connection()