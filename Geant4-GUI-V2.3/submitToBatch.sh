#!/bin/bash

#SBATCH -p htc
#SBATCH -n 1
#SBATCH --mem=4G
#SBATCH --time=04:00:00

module load singularity 
module load spack
#singularity exec -B /cvmfs:/cvmfs -B /hpc:/hpc /users/rnarayan/Public/geant4-10.6_latest.sif /users/rnarayan/Public/geant4-py/Geant4-GUI-V2.3/run.sh $SLURM_ARRAY_TASK_ID
singularity exec -B /cvmfs:/cvmfs -B /hpc:/hpc /users/rnarayan/Public/geant4-10.6_latest.sif $1 $SLURM_ARRAY_TASK_ID


