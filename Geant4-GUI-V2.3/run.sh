#!/bin/bash

#source /hpc/spack/opt/spack/linux-centos7-x86_64/gcc-6.3.0/geant4-10.04.p02-us2el5gppxoev2mzh62ytjwhylzw6cjj/share/Geant4-10.4.2/geant4make/geant4make.sh;
source /app/geant4/geant4-$G4VER-install/bin/geant4.sh 
source /app/root/root-$ROOTVER-build/bin/thisroot.sh 
echo $G4VER 
echo $ROOTVER
echo "seed $1"
#python3 -c 'from Geant4 import *'
python3 Geant4-GUI-V2.py --Batch --Setupfile BatchModeSetupFiles/defaultsetup.yml --Seed $1
