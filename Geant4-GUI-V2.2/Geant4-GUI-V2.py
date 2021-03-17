import argparse
import os

parser = argparse.ArgumentParser(description='Geant4 Python Based GUI Version 2.1')
parser.add_argument('--Batch', type = str, required=True, default = 'Off', help = 'On: Run Geant4 Simulator in Batch Mode\n Off: Run Geant4 GUI (default)')


args = parser.parse_args()

if args.Batch == 'On':
    os.system("python Geant4-BatchV.py")

elif args.Batch == 'Off':
    os.system("python Geant4-GUIV.py")

else: 
    print("Command Option Not Found, please use -h/--help to see more")
