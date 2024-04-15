#!/usr/bin/env python3
# -*- coding: utf-8 -*-
input_dir = "/directory/with/compressed/dicom/files"

#%% Do not modify beyound this point
__author__ = "Saul Pascual-Diaz"
__institution__ = "Universitat de Barcelona"
__date__ = "2024/04/15"
__version__ = "1"
__status__ = "Stable"

#%% System libraries
import os
import gdcm #Intallation command: conda install -c conda-forge gdcm
import sys
import pandas as pd

#%% Progress bar library
from tqdm import tqdm #Installation command: pip install tqdm

#%% Functions
def unzip_pair(file):
    reader = gdcm.ImageReader()
    reader.SetFileName( file )
    
    if not reader.Read():
        sys.exit(1)
    
    change = gdcm.ImageChangeTransferSyntax()
    change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
    change.SetInput( reader.GetImage() )
    if not change.Change():
        sys.exit(1)

    writer = gdcm.ImageWriter()
    writer.SetFileName( file )
    writer.SetFile( reader.GetFile() )
    writer.SetImage( change.GetOutput() )

    if not writer.Write():
        sys.exit(1)

def unzip_dcm(WD):
        filelist = []
        fileerrorlist = []
        for r, d, f in os.walk(WD):
        # r=root, d=directories, f = files
            for file in f:
                filelist.append(os.path.join(r, file))
        print('%i files detected.' % len(filelist))
        pbar = tqdm(total = len(filelist), mininterval=1,
                    maxinterval=5, unit=" dcm file")
        
        # carlos added problems with dicomdir
        filelist = [s for s in filelist if 'DICOMDIR' not in s]
        
        for file in filelist:
            # carlos added try y except
            try:
                unzip_pair(file)
            except: # carlos added try y except
                fileerrorlist.append(file)
                pass
            
            pbar.update(1)
        pbar.close()
        
        # carlos added write error list to csv
        fileerrorlist = pd.DataFrame(fileerrorlist)
        if not fileerrorlist.empty:
            fileerrorlist.to_csv(os.path.split(WD)[0]+"unzip_dcm_py3_ERRORLIST.csv")
            print('\n','***** ERROR WITH SOME FILES, CHECK unzip_dcm_py3_ERRORLIST.csv IN THE PARENT DIRECTORY *****')
    
#%% Running the script
unzip_dcm(input_dir)      