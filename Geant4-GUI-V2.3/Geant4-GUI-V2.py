import argparse
import os

parser = argparse.ArgumentParser(description='Geant4 Python Based GUI Version 2.1')
parser.add_argument('--Batch', action='store_true', help = 'Run Geant4 Simulator in Batch Mode')
parser.add_argument('--Setupfile', type = str, default = 'defaultsetup.yml', help = 'FileName of the Batch mode setup file (located inside the Batch Mode Setupfiles folder) Default: defaultsetup.yml')
parser.add_argument('--Seed', type = int, help = 'Random Seed For Geant4 Simulation')

args = parser.parse_args()

if args.Batch:
    temp = ["python Geant4-BatchV.py --Setupfile %s --Seed %d "%(args.Setupfile,args.Seed)]
    os_arg = ''.join(temp)
    os.system(os_arg)
else:
    os.system("python Geant4-GUIV.py")
