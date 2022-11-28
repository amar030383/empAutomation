with open('precheck.txt', 'r') as file1:
    with open('postcheck.txt', 'r') as file2:
        same = set(file1).intersection(file2)

same.discard('\n')

with open('output.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)