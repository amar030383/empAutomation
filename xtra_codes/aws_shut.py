import boto.ec2, sys

auth = {"aws_access_key_id": "AKIAT4AZFG4CUSYBCEX6", "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}

def main():

    if len(sys.argv) < 2:
        print ("Usage: python aws.py {start|stop}\n")
        sys.exit(0)
    else:
        action = sys.argv[1] 
        
        if action == "start":
            startInstance()
        elif action == "stop":
            stopInstance()
        else:
            print ("Usage: python aws.py {start|stop}\n")

def startInstance():
    print ("Starting the instance...")
    try:
        ec2 = boto.ec2.connect_to_region("us-east-2", **auth)

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    try:
         ec2.start_instances(instance_ids="i-03537914873845c9d")

    except Exception as e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

def stopInstance():
    print ("Stopping the instance...")

    try:
        ec2 = boto.ec2.connect_to_region("us-east-2", **auth)

    except Exception as e1:
        error1 = "Error1: %s" % str(e1)
        print(error1)
        sys.exit(0)

    try:
         ec2.stop_instances(instance_ids="i-03537914873845c9d")

    except Exception as  e2:
        error2 = "Error2: %s" % str(e2)
        print(error2)
        sys.exit(0)

if __name__ == '__main__':
    main()