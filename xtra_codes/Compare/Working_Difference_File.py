precheck = "precheck.txt"
postcheck = "postcheck.txt"
f1 = open(precheck, "r")
f2 = open(postcheck, "r")
i = 0
new = []
for line1 in f1:
	i += 1
	for line2 in f2:
		if line1 == line2:
			pass
		else:
			file1 = {i: line1}
			file2 = {i : line2}
			diff = [file1,file2]
			new.append(diff)
		break
for x in new:
	for y in x:
		print (y)
