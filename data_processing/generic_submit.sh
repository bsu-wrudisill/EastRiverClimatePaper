#!/bin/bash
#SBATCH -J subset              # Job name
#SBATCH -o python%j            # Output and error file name (%j expands to jobID)
#SBATCH -n 1                   # Total number of mpi tasks requested
#SBATCH -N 1                   # Total number of nodes at 16 mpi tasks per-node requested
#SBATCH -p shortq                # Queue (partition) -- normal, development, etc.
#SBATCH -t 02:00:00            # Run time (hh:mm:ss) - 2.0 hours
#SBATCH --exclusive
####SBATCH --mem-per-cpu 15000     # mb of memory           

#~~~~~~~~ Source Module Files ~~~~~~~~~~~~~~~~~~~~~
echo -e "***** Sourcing (loading) default modules \n"
. /cm/shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate WRFDev
python subset_snow.py >> sub.log
exit
