import json,difflib, time
from datetime import datetime
from django.shortcuts import render, redirect
from cisco.commands import ios_upgrade_commands
from cisco.device_connect import excecuteCommands
from cisco.thinkTank import *
from .forms import UpgradeDataForm
from .models import UpgradeData
from cisco.regex import *
from django.core.paginator import Paginator
from cisco.encryptDecrypt import encrypt_password, decrypt_password

def upgrade_input(request):
    form = UpgradeDataForm()
    if request.method =='GET':
        context = {'form':form}
        return render(request,'upgrade_input.html', context)

    elif request.method =='POST':
        form = UpgradeDataForm(request.POST) 
        device_Password = request.POST['device_Password']       
        enable_Password = request.POST['enable_Password']       
        tFTP_Password = request.POST['tFTP_Password']       
        
        if form.is_valid():
            formdata = form.save(commit=False)
            formdata.device_Password = encrypt_password(device_Password)
            formdata.enable_Password = encrypt_password(enable_Password)
            formdata.tFTP_Password = encrypt_password(tFTP_Password)
            formdata.save()
            return redirect('/')

    context = { 'form':form }
    return render(request,'upgrade_input.html',context)

def editUpgrade(request, id):
    obj =  UpgradeData.objects.get(id = id)  
    form = UpgradeDataForm(request.POST or None, instance= obj)
    if form.is_valid():
        obj.last_modified = datetime.now()
        device_Password = request.POST['device_Password']       
        enable_Password = request.POST['enable_Password']       
        tFTP_Password = request.POST['tFTP_Password']  
    
        formdata = form.save(commit=False)
        formdata.device_Password = encrypt_password(device_Password)
        formdata.enable_Password = encrypt_password(enable_Password)
        formdata.tFTP_Password = encrypt_password(tFTP_Password)
        formdata.save()
        return redirect('/')

    context = { 'form':form }
    return render(request,'editUpgrade.html',context)

def startUpgrade(request, id):
    obj =  UpgradeData.objects.get(pk = id)  
    device_Password = decrypt_password(obj.device_Password)
    print (device_Password)
    enable_Password = decrypt_password(obj.enable_Password)
    tFTP_Password = decrypt_password(obj.tFTP_Password)
    print (tFTP_Password)
    device_IP = obj.device_IP
    device_Username = obj.device_Username
    image_Name = obj.image_Name 
    tFTP_IP = obj.tFTP_IP
    tFTP_Username = obj.tFTP_Username
    mD5_Value = obj.mD5_Value
    device_current_image = ''
    device_free_space_pre=0
    tftp_image_available = ''
    tftp_md5_match = ''
    device_precheck_result = ''
    device_goahead = ''
    tftp_precheck_result = ''
    tftp_goahead = ''
    ############################## Device Section ###################################
    response = excecuteCommands(device_IP, device_Username, device_Password,ios_upgrade_commands)
    device_out = output_processor(response)

    device_status = device_out ['device_status']
    if device_status =='Yes':
        device_precheck_result = device_out ['result']
        device_goahead = device_out['goahead']
        device_cmd_result_data = device_out ['result_data']

        reg = regexProcessor(device_cmd_result_data)
        device_current_image = (reg[0])
        device_free_space_pre = (reg[1])
    
    ############################## TFTP Section #################################################
    
    find_image = ('ls -l --block-size=MB | grep '+image_Name)
    find_md5 = ('md5sum '+image_Name)
    tftp_commands = [{'cd /tftp/': .5, find_image:1, find_md5:4}]
    tftp_response = excecuteCommands(tFTP_IP, tFTP_Username, tFTP_Password,tftp_commands)
    tftp_out = output_processor(tftp_response)

    tftp_device_status = tftp_out ['device_status']

    if tftp_device_status =='Yes':
        tftp_goahead = tftp_out['goahead']
        tftp_precheck_result = tftp_out ['result'] 
        tftp_cmd_result = tftp_out ['result_data']

        reg = regexProcessor(tftp_cmd_result,image_Name)
        tftp_image_available = reg[0]
        tftp_md5_match = reg[1]

    ########################### Save Data to DB ############################
    dict ={
        'device_precheck_result':device_precheck_result,
        'device_status':device_status,
        'device_goahead':device_goahead,
        'device_current_image':device_current_image,
        'device_free_space_pre':device_free_space_pre,
        ############################### TFTP ######################################
        "tftp_precheck_result": tftp_precheck_result,
        "tftp_device_status": tftp_device_status,
        'tftp_goahead':tftp_goahead,
        'tftp_image_available':tftp_image_available,
        'tftp_md5_match':tftp_md5_match,
        }
    UpgradeData.objects.filter(id = id).update(**dict)
    ########################################################################################       
    validator = { 
        'device_goahead':device_goahead, 'tftp_goahead':tftp_goahead, 'tftp_image_available':tftp_image_available, 
        'tftp_md5_match':tftp_md5_match, 'device_free_space_pre':device_free_space_pre, 'image_Size_In_MB':obj.image_Size_In_MB,
        'device_current_image':device_current_image, 'image_Name':image_Name, 'mD5_Value':mD5_Value}

    validation_result = upgrade_Validation(validator)
    dict1 ={"validation_result": validation_result}
    UpgradeData.objects.filter(id = id).update(**dict1)

    ############################## Context Section ######################################
    obj =  UpgradeData.objects.get(pk = id) 
    context = {
        'result':utfdecoder(obj.device_precheck_result),
        'id':obj.id,
        'change_status':'Approved',
        'device_status':obj.device_status,
        'tftp_status':obj.tftp_device_status,
        'image_available':obj.tftp_image_available,
        'md5_match':obj.tftp_md5_match,
        'device_IP':obj.device_IP,
        'tFTP_IP':obj.tFTP_IP,
        'image_Name':obj.image_Name,
        'free_space':obj.device_free_space_pre,
        'current_image':obj.device_current_image,
        'upgrade_goahead':obj.validation_result,
        'tftp_status':obj.tftp_device_status,
        }
    return render(request,'startUpgrade.html', context)

def upload_image(request):
    id = request.POST['id']
    upload_time = request.POST['upload_time']
    obj =  UpgradeData.objects.get(pk = id) 
    image = obj.image_Name
    device_Password = decrypt_password(obj.device_Password)
    tFTP_Password = decrypt_password(obj.tFTP_Password)
    tftp_image_upload_log = ''
    tftp_image_upload_status = ''
    send_image = 'scp '+image+' '+obj.device_Username+'@'+obj.device_IP+':'+image
    changeDir = 'cd /tftp'
    if 'csr1000v.light.image.bin' in image:
        timing = 4 
    else:
        timing =(int(upload_time)*60)
    commands = [{changeDir:1, send_image:1, device_Password:timing}]
    commands_output = excecuteCommands(obj.tFTP_IP, obj.tFTP_Username, tFTP_Password,commands)
    key = commands_output['result'] 
    conf = uploadconfirmation(key, obj)
    tftp_image_upload_status = conf[0]
    tftp_image_upload_log = conf[1]
    tftp_image_upload_msg = conf [2]

    md5commands = [{'verify /md5 '+image:timing}]
    md5check_output = excecuteCommands(obj.device_IP, obj.device_Username, device_Password,md5commands)    
    key = md5check_output['result'] 
    device_generated_md5 = md5checkDevice(key)    

    dict ={
        "tftp_image_upload_log": tftp_image_upload_log, 
        'tftp_image_upload_status':tftp_image_upload_status,
        'device_generated_md5':device_generated_md5,
        'tftp_image_upload_msg':tftp_image_upload_msg,
        }
    UpgradeData.objects.filter(id = id).update(**dict)

    obj =  UpgradeData.objects.get(pk = id)
    md5matched = 'False'
    tftp_upload_log = obj.tftp_image_upload_log
    if obj.tftp_md5_match ==obj.device_generated_md5:
        md5matched = True

    context = {
        'result':tftp_upload_log,
        'current_image':obj.device_current_image,
        'image_Name':obj.image_Name,
        'id':obj.id,
        'tftp_md5_match':obj.tftp_md5_match,
        'md5matched':md5matched,
        'tftp_image_upload_msg':obj.tftp_image_upload_msg,
        'device_generated_md5':obj.device_generated_md5,
        }
    return render(request,'upload_image.html', context)

def changeBootReload(request):
    id = request.POST['id']
    obj =  UpgradeData.objects.get(pk = id) 
    device_Password = decrypt_password(obj.device_Password)
    enable_Password = decrypt_password(obj.enable_Password)
    image = obj.image_Name
    device_IP = obj.device_IP
    device_Username = obj.device_Username
    device_Password = device_Password
    changeBootvar = 'boot system bootflash:'+image
    show_boot = 'do show boot'
    changeBoot_Reload_commands = [{'conf t':1, enable_Password:1, 'no boot system':2, changeBootvar:1,  "do wr": 1, show_boot: 1}]
    #changeBoot_Reload_commands = [{"wr": 1, "show boot": 1, enable_Password:1}]
    #changeBoot_Reload_commands = [{'conf t':1, enable_Password:1,'no boot system':2, changeBootvar:1,  "do wr": 1, "show_boot": 1, 'do reload':1, 'yes':1}]

    response = excecuteCommands(device_IP, device_Username, device_Password,changeBoot_Reload_commands)
    result_data = response['result']                       
    device_upgrade_cmds = resultProcessor(result_data)  
    if device_upgrade_cmds:
        dict ={"device_upgrade_cmds": device_upgrade_cmds,"upgrade_status": "Done"}
        UpgradeData.objects.filter(id = id).update(**dict)

    context = {
        'image_Name':image,
        'current_image':obj.device_current_image,
        'id':id,
        }
    return render (request, 'changeBootReload.html',context)

def upgrade_postcheck(request):
    print ('In upgrade_postcheck')
    id = request.POST['id']
    obj =  UpgradeData.objects.get(pk = id) 
    device_Password = decrypt_password(obj.device_Password)
    device_IP = obj.device_IP
    device_Username = obj.device_Username
    response = excecuteCommands(device_IP, device_Username, device_Password,ios_upgrade_commands)
    result_data = response['result']                       
    result = resultProcessor(result_data)  
    if result:
        edit = UpgradeData.objects.get(id = id)
        edit.device_postcheck_result = result
        edit.save() 
    obj =  UpgradeData.objects.get(pk = id) 
    post_result = utfdecoder(obj.device_postcheck_result)
    context = {
        'result':post_result,
        'image_Name':obj.image_Name,
        'current_image':obj.device_current_image,
        'id':id,
        }
    return render (request, 'changeBootReload.html',context)

def compare_config(request):
    id = request.POST['id']
    obj =  UpgradeData.objects.get(pk = id) 
    precheck = utfdecoder(obj.device_precheck_result)
    postcheck = utfdecoder(obj.device_postcheck_result)    
    result3 = []
    for line in difflib.unified_diff(precheck, postcheck):
        result3.append(line)
    dict1 ={"comparediff": result3}
    UpgradeData.objects.filter(id = id).update(**dict1)

    context = { 'result':precheck, 'result2':postcheck, 'result3': result3, 'id':id }
    return render (request, 'compare_config.html',context)

def statusUpgrade(request):
    id = request.POST['id']
    status = ['Successful', 'Failed', 'Completed_with_Issues']
    result = []
    for sta in status:
        try:
            output = request.POST[sta]
            result.append(output)
        except:
            pass    
    edit = UpgradeData.objects.get(id = id)
    edit.upgrade_status = result[0]
    edit.save() 
    return redirect('/')

def home(request):
    p = Paginator(UpgradeData.objects.order_by('-date_created'),5)
    page = request.GET.get('page')
    paged_data = p.get_page(page)

    upgrade_orders = UpgradeData.objects.all()
    total_orders = upgrade_orders.count()
    
    orders = UpgradeData.objects.all().filter(upgrade_status = 'Successful')
    executed_orders = orders.count()
    unexecuted_upgrades = total_orders-executed_orders

    context = {
        'paged_data':paged_data,
        'total_orders':total_orders, 
        'executed_upgrades':executed_orders, 
        'unexecuted_upgrades':unexecuted_upgrades
        }
    return render(request, 'dashboard.html', context)

def login(request):
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
        print (email, password)
    return render (request,'login.html')

def multipage(request):
    return render (request,'multipage.html')

def deleteUpgrade(request, id):
    UpgradeData.objects.get(id = id).delete()
    return redirect('/')


def displayUpgrade(request, id):
    fl = []
    for field in UpgradeData._meta.fields:
        f = (field.name)
        fl.append(f)

    for data in fl:
        print (data)

    return render(request,'displayUpgrade.html')
