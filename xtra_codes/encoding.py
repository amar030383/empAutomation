
# data = b'CSR1#wr\r\nBuilding configuration...\r\n[OK]\r\nCSR1#'
# print ((data).decode("utf-8") )
# print ((b"abcde").decode("utf-8"))


string = ['Problem found!']

# string with encoding 'utf-8'
arr = bytes(string[0], 'utf-8')
arr2 = bytes(string[0], 'ascii')

print(arr,'\n')
print(arr2,'\n')

# actual bytes in the the string
# for byte in arr:
#     print(byte, end=' ')
# print("\n")
# for byte in arr2:
#     print(byte, end=' ')