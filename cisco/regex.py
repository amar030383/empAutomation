import re

def convertByteToMB(data): # Device
    if data:
        megabytes=int(data)/1000000
        return int(megabytes)
    else:
        return False

def freeflashMemory(data):  # Device
    output = re.findall(r'\s+\((\d+)\s+bytes free',str(data))
    if output:
        data = convertByteToMB(output[0])
        return data
    else:
        return None

def findMd5ValueDevice(image, data):
    output = re.findall(rf'\({image}\)\s+=\s(\w.+)',str(data))
    if output:
        return output
    else:
        return None

def findimageuploadStatus(image_name, output):  # Device
    data = re.findall(rf'({image_name}\s+(\d+)%\s+\w+)\s+', str(output))
    last_match = str(data[-1])
    if '100%' in last_match:
        resp = {
            'status':'Pass',
            'msg': 'Image uploaded successfully',
            'log': last_match,
        }
        return resp
    else:
        resp = {
            'status':'Failed',
            'msg': 'Failed, please increase the timing',
            'log': last_match,
        }
        return resp
        
def showIPInterfaceBrief(data): # Device
    output = re.findall(r'(\w+.)\s+(\d+.\d+.\d+.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)',str(data))
    if output:
        return output
    else:
        return None

def showbootvar(data):  # Device
    output = re.findall(r'BOOT.+=\s(\w+.+.bin)',str(data))
    if output:
        single = getcurrentbootvar(output)
        return single[0]
    else:
        return None

def getcurrentbootvar(data):    # Device
    output = re.findall(r'bootflash:(\w.+.bin)',str(data))
    if output:
        return output
    else:
        return None

def tftpImageMD5(image, tftp_data):
    output = re.findall(rf'n(\w+)  {image}',str(tftp_data))

    if output:
        return output[0]
    else:
        return None

def tftpfindImage(image , tftp_data):
    print (image, tftp_data)
    output = re.findall(rf'{image}',str(tftp_data))
    if output:
        return output[0]
    else:
        return None

def regexProcessor(device_data, *argv):
    regexProcessedData = []
    for key in device_data:
        for k in key:     
            if 'dir flash' in k: 
                free_space = freeflashMemory(key[k])
                regexProcessedData.append(free_space)
            
            elif 'show bootvar' in k:
                current_boot = showbootvar(key[k])
                regexProcessedData.append(current_boot)

            elif 'ls -R ' in k: # Find Image
                for image in argv:
                    tftpimage = tftpfindImage(image ,key[k])
                    if tftpimage:
                        regexProcessedData.append(tftpimage)

            elif 'ls -l ' in k: # Find Image
                for image in argv:
                    tftpimage = tftpfindImage(image ,key[k])
                    if tftpimage:
                        regexProcessedData.append(tftpimage)
                        
            elif 'md5sum' in k: # Check MD5sum
                for image in argv:
                    tftpmd5 = tftpImageMD5(image ,str(key[k]))
                    if tftpmd5:
                        regexProcessedData.append(tftpmd5)

    return regexProcessedData

def deviceMD5Finer(data):
    output = re.findall(r'verify \/md5\s+\(\w.+\) = (\w+)',str(data))
    if output:
        return output[0]
    else:
        return None

    pass
# def checkTFTPimageSize(image, data):
#     data = re.findall(r'(\d+MB)\s+\w.+{image}',data)
#     print (data)
#     #data = re.findall(r'(\d+MB)\s+\w.+(csr1000v-universalk9.17.03.04a.SPA.bin)',data)
#     print (data[0])

# image = 'csr1000v-universalk9.17.03.04a.SPA.bin'
# data = '''
# amar@ip-172-31-48-228:/tftp$ ls -l --block-size=MB | grep csr1000v-universalk9.17.03.04a.SPA.bin
# -rw-rw-r-- 1 amar amar 519MB Nov 10 08:27 csr1000v-universalk9.17.03.04a.SPA.bin
# '''
# checkTFTPimageSize(image, data)