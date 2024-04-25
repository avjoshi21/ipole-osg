import sys,os,glob
import click
import re
@click.command()
@click.option("--inputfile",default='par/BATCH.ALL',help='BATCH.ALL file used to submit jobs to osg')
@click.option("--outputdir",default="./",help="output directory where all ipole images are stored")
def removeFinishedFiles(inputfile,outputdir):
    with open(inputfile,'r') as fp:
        lines=fp.readlines()
    with open(inputfile,'w') as fp:
        for line in lines[:]:
            outputImage = imageNamer(lineParser(line))
            if(len(glob.glob(os.path.join(outputdir,outputImage)))==0):
                fp.write(line)

                
                
        

def lineParser(line):
    vals = line.split(',')
    returnDict={}
    returnDict['rhigh']=vals[-3]
    returnDict['theta']=vals[-2]
    grmhdDump=vals[0]
    returnDict['dumpNum']=re.search("(\d{4,5}[_.])",grmhdDump)[0][:-1]
    if re.search("(sane)",grmhdDump,flags=re.I)==None:
        returnDict['model']="M"
    else:
        returnDict['model']="S"
    returnDict['spin']=re.search("(a[+-]\d.\d{1,4})|(a\d.\d{1,4})|(a.\d{1,4})",grmhdDump,flags=re.I)[0]
    return returnDict

def imageNamer(modelDict):
    return f"img_{modelDict['model']}{modelDict['spin']}_s{modelDict['dumpNum']}_Rh{modelDict['rhigh']}_i{modelDict['theta']}.h5"

if __name__=="__main__":
    removeFinishedFiles()
