#!/bin/bash

#SBATCH -p htc
#SBATCH -n 1
#SBATCH --mem=4G
#SBATCH --time=04:00:00

module load singularity 
module load spack
#singularity   shell -B /cvmfs:/cvmfs -B /hpc:/hpc /users/rnarayan/Public/geant4-10.6_latest.sif -b
#source /hpc/spack/opt/spack/linux-centos7-x86_64/gcc-6.3.0/geant4-10.04.p02-us2el5gppxoev2mzh62ytjwhylzw6cjj/share/Geant4-10.4.2/geant4make/geant4make.sh
#source /app/geant4/geant4-10.6.1-install/bin/geant4.sh

#python Geant4-BatchV.py --Batch --Setupfile BatchModeSetupFiles/defaultsetup.yml --Seed $SLURM_TASK_ID

singularity exec -B /cvmfs:/cvmfs -B /hpc:/hpc /users/rnarayan/Public/geant4-10.6_latest.sif /users/rnarayan/Public/geant4-py/Geant4-GUI-V2.3/run.sh $SLURM_ARRAY_TASK_ID

