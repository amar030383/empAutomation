import paramiko, time, os
device = 'ec2-3-13-93-157.us-east-2.compute.amazonaws.com'  # CSR1000v
Username = os.environ.get('csr_usr')
Password = os.environ.get('csr_pwd')
ios_cmd = ('show version | in cisco', 'show ip int bri')

def Para_connection (server_ip, Username, Password):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server_ip, username=Username, password=Password,  look_for_keys=False)
    connection = client.invoke_shell()
    return connection

def Para_send_command (connection, command):
    out = []
    for command in ios_cmd:
        connection.send(command + '\n')
        time.sleep(.8)
        ouput=str(connection.recv(4096),'utf-8')
        out.append(ouput)
    print (out)

    return ouput

connection = Para_connection (device, Username, Password)
Para_send_command(connection, ios_cmd)

