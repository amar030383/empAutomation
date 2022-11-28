import paramiko, time, socket, json

Timeout_Error = 'Timeout Error'
AuthenticationException = 'Authentication failed.'
UnableToConnect = 'Unable to connect'

def para_connection (server_ip, Username, Password):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server_ip, username=Username, password=Password, look_for_keys=False)
        connection = client.invoke_shell()
        return connection
    except (socket.error) as ex:
        return ex
    except paramiko.AuthenticationException as auth:
        return auth
    except Exception as ex:
        return ex

def para_send_command (connection, cmds):
    out = []
    for commands in cmds:
        for command in commands:
            connection.send(command + '\n')
            time.sleep(commands[command])
            output= connection.recv(64096)
            result = {command:output}
            out.append(result)
    #print (json.dumps(out, indent=4, sort_keys=True))
    return out

def excecuteCommands( ip, username, password,commands): # show commands will be executed to gather importand information
    print ('In excecuteCommands')
    connection = para_connection(ip, username, password)
    if 'connection failed' in str(connection):
        print ('In IF Connection failed')
        result = {'output': Timeout_Error}
        status = [{'Reachable':'No, check device connectivity'}]
        return {'result':result, 'status':status}

    elif AuthenticationException in str(connection):
        print ('In IF Authentication failed')
        result = {'output': AuthenticationException}
        status = [{'Reachable':'Yes, but check username and password'}]
        return {'result':result, 'status':status}


    elif UnableToConnect in str(connection):
        print ('In elif Unable to connect')
        result = {'output': UnableToConnect}
        status = [{'Reachable':'No, check device connectivity'}]
        return {'result':result, 'status':status}

    else:
        print ('In ELIF Paramiko')
        result = para_send_command(connection, commands)    
        status = [{'Reachable':'Yes'}]
        return {'result':result, 'status':status}
