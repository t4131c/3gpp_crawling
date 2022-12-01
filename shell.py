import os

filelist = os.listdir("./inputs")
path = os.getcwd()
out_path = path + "/out/"
if (not os.path.isdir(out_path)):
	os.mkdir(out_path)
input_path = path + "/inputs/"


for file in filelist:
	print("Searching : " + file)
	target = input_path + file
	output = file[:file.find(".")] + ".out"
	output = out_path + output
	command = "bash search.sh " + target + " > " + output
	print(command)
	os.system(command)

