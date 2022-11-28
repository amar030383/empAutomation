from __future__ import print_function
import traceback, time, os
from paramiko_expect import SSHClientInteraction
import paramiko
device = '3.19.131.3'
Username = os.environ.get('csr_usr')
Password = os.environ.get('csr_pwd')
localPath = 'csr1000v-universalk9.17.02.03.SPA.bin'
remotePath = 'ec2-3-13-93-157.us-east-2.compute.amazonaws.com'
def Para_connect(ip, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname = ip, username = username, password=password, port=22)
    return (ssh_client)

def upload_image(ssh_client, localPath, remotePath ):
    print (localPath, remotePath)
    ftp_client=ssh_client.open_sftp()
    ftp_client.put(localPath, remotePath)
    ftp_client.close()

def Para_send_command (ssh_client, command):
    (stdin, stdout, stderr) = ssh_client.exec_command(command)
    time.sleep(1)
    output1= (stdout.read())
    output = (str(output1, 'utf-8'))
    #ssh_client.close()
    return (output)

def main():
    #https://github.com/fgimian/paramiko-expect/blob/master/examples/paramiko_expect-demo-helper.py
    PROMPT = 'amar@ip-172-31-48-228:~$\s+'
    try:
        PROMPT = 'amar@ip-172-31-48-228:~$\s+'
        PROMPT2 = 'amar@ip-172-31-48-228:/tftp$\s+'
        PROMPT3 = 'Password:\s+'
        cmd = 'scp csr1000v-universalk9.17.02.03.SPA.bin amar@3.13.93.157:csr1000vSCP.bin'
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=device, username=Username, password=Password)
        with SSHClientInteraction(client, timeout=300, display=True) as interact:
            interact.send('cd /tftp')
            interact.expect(PROMPT2)
            interact.send('cisco')
            interact.expect(PROMPT)

        print ('Script ended')
    except Exception:
        traceback.print_exc()
    finally:
        try:
            client.close()
        except Exception:
            pass
main()