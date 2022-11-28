import difflib
import sys

file1 = open("precheck.txt").readlines()
file2 = open("postcheck.txt").readlines()
file1 = ['CSR1#show bootvar | in BOOT\r\nBOOT variable = bootflash:csr1000v-universalk9.17.02.03.SPA.bin,12;\r\nBOOTLDR variable does not exist\r\nCSR1#', 'dir flash: | in bytes\r\n6286213120 bytes total (4423303168 bytes free)\r\nCSR1#']
file2= ['CSR1#show bootvar | in BOOT\r\nBOOT variable = bootflash:csr1000v-universalk9.17.02.03.SPA.bin,12;\r\nBOOTLDR variable does not exist\r\nCSR1#', 'dir flash: | in bytes\r\n6286213120 bytes total (4423303168 bytes free)\r\nCSR1#']
delta = difflib.unified_diff(file1, file2)
sys.stdout.writelines(delta)