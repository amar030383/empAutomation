import difflib

lines1 = ['CSR1#show bootvar | in BOOT\r\nBOOT variable = bootflash:csr1000v-universalk9.17.02.03.SPA.bin,12;\r\nBOOTLDR variable does not exist\r\nCSR1#', 'dir flash: | in bytes\r\n6286213120 bytes total (4423303168 bytes free)\r\nCSR1#']
lines2= ['CSR1#show bootvar | in BOOT\r\nBOOT variable = bootflash:csr1000v-universalk9.17.03.SPA.bin,12;\r\nBOOTLDR variable does not exist\r\nCSR1#', 'dir flash: | in bytes\r\n6286213120 bytes total (4423303168 bytes free)\r\nCSR1#']


for line in difflib.unified_diff(lines1, lines2):
    print (line)