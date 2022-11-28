import paramiko, time, os, re
device = 'ec2-3-13-93-157.us-east-2.compute.amazonaws.com'  # CSR1000v
Username = os.environ.get('csr_usr')
Password = os.environ.get('csr_pwd')
#ios_upgrade_commands = ['show version | in cisco', 'show ip int bri', 'verify /md5 bootflash:file.bin', 'verify /sha512 bootflash:file.bin']
ios_upgrade_commands = ['verify /md5 bootflash:file.bin',"dir flash: | in bytes"]
data = 3917647872

def convertByteToMB(data):
    if data:
        megabytes=data/1000000
        print (megabytes)
        return megabytes
    else:
        return False
convertByteToMB(data)

def freeflashMemory(data):
    output = re.findall(r'\s+\((\d+)\s+bytes free',data)
    if output:
        print (output)
        return output
    else:
        return None

def findMd5ValueDevice(image, data):
    #image = "bootflash:file.bin"
    output = re.findall(rf'\({image}\)\s+=\s(\w.+)',data)
    if output:
        print (output)
        return output
    else:
        return None

def Para_connection (server_ip, Username, Password):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server_ip, username=Username, password=Password,  look_for_keys=False)
    connection = client.invoke_shell()
    return connection

def Para_send_command (connection, command):
    out = []
    for command in ios_upgrade_commands:
        connection.send(command + '\n')
        if 'md5' in command or 'sha' in command:
            time.sleep(4)
            output=str(connection.recv(16096),'utf-8')
            result = {command:output}
            out.append(result)
        else:
            time.sleep(1)
            output=str(connection.recv(16096),'utf-8')
            result = {command:output}
            out.append(result)
    return out

#connection = Para_connection (device, Username, Password)
#out = Para_send_command(connection, ios_upgrade_commands)
#
out = [{'verify /md5 bootflash:file.bin': '\r\n\r\n\r\nCSR1#verify /md5 bootflash:file.bin\r\n....Done!\r\nverify /md5 (bootflash:file.bin) = 84e7972536e584a9d2902352a9aec042\r\n\r\n\r\nCSR1#'}, {'dir flash: | in by86213120 bytes total (3917647872 btes': 'dir flash: | in bytes\r\n6286213120 bytes total (3917647872 bytes free)\r\nCSR1#'}]
def loopandsearch(out):
    for key in out:
        for k in key:     
            if 'verify /md5' in k:
                findMd5ValueDevice(key[k])

            elif 'flash' in k:
                freeflashMemory(key[k])
