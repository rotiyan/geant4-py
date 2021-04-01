#!/bin/bash

source /hpc/spack/opt/spack/linux-centos7-x86_64/gcc-6.3.0/geant4-10.04.p02-us2el5gppxoev2mzh62ytjwhylzw6cjj/share/Geant4-10.4.2/geant4make/geant4make.sh;
source /app/geant4/geant4-10.6.1-install/bin/geant4.sh; 
echo "seed $1"
python Geant4-GUI-V2.py --Batch --Setupfile BatchModeSetupFiles/defaultsetup.yml --Seed $1
