from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('startUpgrade/<str:id>',views.startUpgrade, name = 'startUpgrade'),
    path('editUpgrade/<str:id>',views.editUpgrade, name = 'editUpgrade'),
    path('upgrade_input/',views.upgrade_input, name = 'upgrade_input'),
    path('upload_image/',views.upload_image, name = 'upload_image'),
    path('changeBootReload/',views.changeBootReload, name = 'changeBootReload'),
    path('multipage/',views.multipage, name = 'multipage'),
    path('upgrade_postcheck/',views.upgrade_postcheck, name = 'upgrade_postcheck'),
    path('compare_config/',views.compare_config, name = 'compare_config'),
    path('statusUpgrade/',views.statusUpgrade, name = 'statusUpgrade'),
    path('deleteUpgrade/<str:id>',views.deleteUpgrade, name = 'deleteUpgrade'),    
    path('displayUpgrade/<str:id>',views.displayUpgrade, name = 'displayUpgrade'),    
    ]