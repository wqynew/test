#!/bin/bash
#SBATCH -n 20
#SBATCH -t 2:00

. ~/.profile
module load tensorflow
tensorflow test.py