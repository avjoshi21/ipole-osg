import glob,sys,os
import subprocess
import click
import re

@click.command()
@click.option("--imagesperdump",type=float,help="number of GRRT parameters (images) per GRMHD dump")
@click.option("--outputdir",help="output directory where ipole images are stored")
@click.option("--grmhddir",help="directory where all grmhd snapshots are stored")
def clearFinishedGRMHD(imagesperdump,outputdir,grmhddir):
    grmhdFiles = sorted(glob.glob(os.path.join(grmhddir,"**/*.h5"),recursive=True))
    imageFiles = sorted(glob.glob(os.path.join(outputdir,"**/*.h5"),recursive=True))
    numDeleted=0
    for grmhdFile in grmhdFiles:
        #dumpNum = str(int(grmhdFile.split('.')[-2].split('_')[-1]))
        dumpNum=re.search("(\d{4,5}[_.])",grmhdFile)[0][:-1]
        ims = [i for i in imageFiles if dumpNum in i]
        if(len(ims)==imagesperdump):
            print('deleting '+grmhdFile)
            numDeleted+=1
            subprocess.call("rm {}".format(grmhdFile),shell=True)
    print(f"deleted {numDeleted} out of {len(grmhdFiles)} files")
if __name__ == "__main__":
    clearFinishedGRMHD()
