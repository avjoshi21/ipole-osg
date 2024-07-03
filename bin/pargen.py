#!/home/abhishek.joshi/miniconda3/bin/python

import glob
import sys,os
import re
import subprocess
import numpy as np

version = sys.argv[1]
if(version=='emhd'):
    ext="emhd"
elif(version=="ideal"):
    ext="ideal"

grmhdModel = sys.argv[2]
disk = 'mad' if grmhdModel[0]=='M' else 'sane'
tilt = sys.argv[3]
dumpStart = int(sys.argv[4])
dumpEnd = int(sys.argv[5])
r="/home/abhishek.joshi/sgra_emhd"

cadence=1
normBatchSize = 1000
bh='M87'

munitFilesStr=f"/home/abhishek.joshi/sgra_emhd/munits/windows/{ext}/MunitVals_{bh}_{tilt}_{grmhdModel}*.txt"
munitFiles = sorted(glob.glob(munitFilesStr))
md5file = f"/home/abhishek.joshi/sgra_emhd/md5/md5_{ext}_{grmhdModel}_{tilt}.txt"
# md5file = "/home/abhishek.joshi/sgra_emhd/md5/test.txt"
for munitFile in munitFiles:
    munitData = np.loadtxt(munitFile,skiprows=1,dtype=object)
    grmhdDirectoryStr=f"/home/abhishek.joshi/protected/{ext}/{disk}/{grmhdModel[1:]}/dumps/torus.*.h5"
    grmhdDirectory = sorted(glob.glob(grmhdDirectoryStr))
    for grmhdFile in grmhdDirectory[::cadence]:
        if("final" in grmhdFile):
            continue;
        #grmhdFile = grmhdFile.replace("/protected","osdf:///ospool/PROTECTED")
        dump = grmhdFile.split('/')[-1]
        dumpNum = int(re.search("(\d{5})",dump)[0])
        if (dumpNum < dumpStart or dumpNum > dumpEnd):
            continue
        windowStart = int(np.floor(dumpNum/1000)*1000)
        windowEnd = int(windowStart + normBatchSize)
        try:
            windowData = munitData[np.where((munitData[:,0]==str(windowStart)) & (munitData[:,1]==str(windowEnd))),:][0][0]
        except IndexError:
            continue    
        inc,rhigh,rlow,munit=windowData[-4:]
        if (eval(munit) > 1e50):
            continue
        #md5search = subprocess.run(f"grep {dump} {md5file}",shell=True,capture_output=True)
        #md5str=md5search.stdout.decode("utf-8")
        #md5 = md5str.split(' ')[0]

        print(f"{grmhdFile},0,{dumpNum:05d},{rhigh},{rlow},{inc},{munit}")
