import argparse
import os

parser = argparse.ArgumentParser(description='Geant4 Python Based GUI Version 2.2')
parser.add_argument('--Batch', type = str, required=True, default = 'Off', help = 'On: Run Geant4 Simulator in Batch Mode\n Off: Run Geant4 GUI (default)')

parser.add_argument('--Setupfile', type = str, default = 'defaultsetup.yml', help = 'FileName of the Batch mode setup file (located inside the Batch Mode Setupfiles folder) Default: defaultsetup.yml')

parser.add_argument('--Seed', type = int, help = 'Random Seed For Geant4 Simulation')

args = parser.parse_args()

if args.Batch == 'On':
    temp = ["python Geant4-BatchV.py --Setupfile ", args.Setupfile]
    os_arg = ''.join(temp)
    os.system(os_arg)

elif args.Batch == 'Off':
    os.system("python Geant4-GUIV.py")

else: 
    print("Command Option Not Found, please use -h/--help to see more")
