import glob,sys,os
import subprocess

imagesPerDump=6

pub = "/public/avjoshi2/m87_v1/"
imLoc = "/home/avjoshi2/ipole-v1/out/"
models=sys.argv[1:]
for model in models:
	grmhdFiles = sorted(glob.glob(pub+model+"/*.h5"))
	imageFiles = sorted(glob.glob(imLoc+model+"/*.h5"))
	for grmhdFile in grmhdFiles:
		dumpNum = str(int(grmhdFile.split('.')[-2].split('_')[-1]))
		ims = [i for i in imageFiles if dumpNum in i]
		#print(dumpNum,len(ims),len(imageFiles),len(grmhdFiles))
		if(len(ims)==imagesPerDump):
			print('deleting '+grmhdFile)
			subprocess.call("rm {}".format(grmhdFile),shell=True)
