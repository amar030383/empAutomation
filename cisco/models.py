from django.utils import timezone
from django.db import models
#from django.db.models.base import Model
class UpgradeData(models.Model):

    CATEGORY = (("IOS","IOS"),('NXOS', 'NXOS'),('IOSXR', 'IOSXR'))
    UPGRADE_STATUS = (("Successful","Successful"),('Pending', 'Pending'),('Cancelled', 'Cancelled'),('Failed', 'Failed'), ('Completed with Issues','Completed with Issues'))
    CHANGE_STATUS = (("Approved","Approved"),('Not Approved', 'Not Approved'), ('Rejected','Rejected'), ('Incorrect Change Window','Incorrect Change Window'))

    id = models.AutoField(primary_key=True)
    change_No = models.CharField(max_length=25, null=True, default='CHG0000036')
    change_status = models.CharField(max_length=25, null=True, choices =CHANGE_STATUS, default='Approved',  editable=False)
    device_Type = models.CharField( max_length=25, null=True, choices=CATEGORY, default='IOS')
    device_IP = models.GenericIPAddressField(null=True, default='3.13.93.157')
    device_Username = models.CharField( max_length=25, null=True, default='amar')
    device_Password = models.CharField( max_length=250, null=True, default='cisco')
    enable_Password = models.CharField( max_length=250, null=True, default='cisco')
    tFTP_IP = models.GenericIPAddressField(null=True, default='3.19.131.3')
    tFTP_Username = models.CharField(max_length=25, null=True,default='amar')
    tFTP_Password = models.CharField(max_length=250, null=True, default='cisco')
    image_Size_In_MB = models.IntegerField(null=False, default=1024)
    ##################################### Real Image ############################################################
    #image_Name = models.CharField(max_length=50, null=True, default='csr1000v-universalk9.17.03.04a.SPA.bin')
    #mD5_Value = models.CharField(max_length=50, null=True, default='5042bd9e602b03d5522c0cefe3b395a3')
    
    ##################################### Test Image ############################################################
    image_Name = models.CharField(max_length=40, null=True, default='csr1000v.light.image.bin')
    mD5_Value = models.CharField(max_length=40, null=True, default='c94df39614e265a4a3b7e7ad49db9607')

    upgrade_status = models.CharField(max_length=25, null=True, choices=UPGRADE_STATUS, default='Pending', editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    last_modified = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    device_status = models.CharField(max_length=100, null=True, editable=False) # Reachable/ or problem
    device_goahead = models.CharField(max_length=50, null=True, editable=False) # Yes or No
    device_free_space_pre = models.IntegerField(null=True, editable=False) # Store in Int(MB)
    device_precheck_result = models.CharField(max_length=10000, null=True, editable=False)
    device_upgrade_cmds = models.CharField(max_length=10000, null=True, editable=False)
    device_postcheck_result = models.CharField(max_length=10000, null=True, editable=False)
    device_current_image = models.CharField(max_length=50, null=True,editable=False)    
    device_generated_md5 = models.CharField(max_length=50, null=True,editable=False)
    tftp_goahead = models.CharField(max_length=50, null=True, editable=False) # Yes or No
    tftp_precheck_result = models.CharField(max_length=5000, null=True, editable=False) # TFTP command outputs for auditing
    tftp_device_status = models.CharField(max_length=100, null=True, editable=False) # Yes or No
    tftp_image_upload_status = models.CharField(max_length=50, null=True, editable=False) # Image upload Status, Success or failed 
    tftp_image_upload_log = models.CharField(max_length=500, null=True, editable=False) # Image upload logs
    tftp_image_upload_msg = models.CharField(max_length=50, null=True, editable=False) # Image upload logs
    tftp_image_available = models.CharField(max_length=50, null=True, editable=False) # Image available on TFTP server
    validation_result = models.CharField(max_length=50, null=True, editable=False) # Result after gathering info
    tftp_md5_match = models.CharField(max_length=50, null=True, editable=False) # MD5 match on TFTP Server
    comparediff =  models.CharField(max_length=10000, null=True, editable=False)

    def __str__(self): 
        return self.id