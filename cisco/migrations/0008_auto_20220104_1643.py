# Generated by Django 3.2.8 on 2022-01-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cisco', '0007_auto_20220104_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgradedata',
            name='device_Password',
            field=models.CharField(default='cisco', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='upgradedata',
            name='enable_Password',
            field=models.CharField(default='cisco', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='upgradedata',
            name='tFTP_Password',
            field=models.CharField(default='cisco', max_length=250, null=True),
        ),
    ]
