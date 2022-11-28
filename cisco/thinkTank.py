import json, re, ast
from cisco.encryptDecrypt import decrypt_password
from cisco.regex import *

def resultProcessor(device_data):
    result = []
    if device_data:
        for key in device_data:
            for k in key:
                result.append((key[k]).strip()) 
        return result
    else:
        return ('Could not gather information from the device')

def upgrade_Validation(validator):    
#    print (json.dumps(validator, indent=4, sort_keys=True))
    # status = []
    # if validator['device_goahead']=='Yes':
    #     result = {'device_goahead': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'device_goahead': 'Failed', 'Message':"Could not get into the device"}

    # if validator['tftp_goahead']=='Yes': 
    #     result = {'tftp_goahead': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'tftp_goahead': 'Failed', 'Message':'Could not get into the device'}

    # if validator['tftp_image_available']== validator['image_Name']:
    #     result = {'tftp_image_available': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'tftp_image_available': 'Failed', 'Message':'Image not found on TFTP Server'}

    # if validator['tftp_md5_match']==validator['mD5_Value']:
    #     result = {'tftp_md5_match': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'tftp_md5_match': 'Failed', 'Message':'MD5 does not match'}

    # if validator['tftp_image_available']!=validator['device_current_image']:
    #     result = {'Image Validation': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'Image Validation': 'Failed', 'Message':'New image and device image matches'}

    # if validator['image_Size_In_MB']<validator['device_free_space_pre']:
    #     result = {'image_Size_In_MB': 'Pass', 'Message':'Successful'}
    # else:
    #     result = {'image_Size_In_MB': 'Failed', 'Message':'Insuffient space on Device'}
    

    if validator['device_goahead']=='Yes' and validator['tftp_goahead']=='Yes' and validator['tftp_image_available']== validator['image_Name']\
    and validator['tftp_md5_match']==validator['mD5_Value'] and validator['tftp_image_available']!=validator['device_current_image']\
    and validator['image_Size_In_MB']<validator['device_free_space_pre']:
        return ('Yes')
    else:
        return('No')

def output_processor(response):
    device_status = ''
    result = ''
    goahead = ''
    result_data = ''
    device_status = response['status'][0]['Reachable']  # Working Fine

    if device_status != 'Yes':
        result =  ['Problem found!']
        goahead = 'No'
    else:
        goahead = 'Yes'
        result_data = response['result']                    #   
        result = resultProcessor(result_data) 
    output = {
        'device_status':device_status,
        'goahead':goahead,
        'result':result,
        'result_data':result_data,
    }  
    return output


def utfdecoder(data):
    try:
        list1 = ast.literal_eval(data) 
        output = []
        for c in list1:
            solved = ((c).decode("utf-8"))
            output.append(solved)
        return output
    except:
        return None

def uploadconfirmation(key, obj):
    tftp_image_upload_status = ''
    tftp_image_upload_log=''
    tftp_image_upload_msg =''
    for k in key:
        for key, value in k.items():
            if decrypt_password(obj.device_Password) in key: # Find Image
                tftp_image_upload= findimageuploadStatus(obj.image_Name, value)

                tftp_image_upload_log =  (tftp_image_upload['log'])
                tftp_image_upload_msg =  (tftp_image_upload['msg'])
                if 'Pass' == tftp_image_upload['status']:
                    tftp_image_upload_status = 'Pass'
                else:
                    tftp_image_upload_status = 'Failed'

    return [tftp_image_upload_status, tftp_image_upload_log, tftp_image_upload_msg]

def md5checkDevice(key):
    for k in key:
        for key, value in k.items():
            md5 = deviceMD5Finer(value)
            if md5:
                return md5
            else:
                return None
