#/bin/bash
#SBATCH -n 1
#SBATCH --mem 4096
#SBATCH -t 60

#
# GOOD EXAMPLE: python runs inside the container, /lustre, and GPU drivers bound to container
#

. ~/.profile
module load tensorflow
singularity shell \
	--bind /lustre \
	--bind /usr/local/nvidia/${NVIDIA_VERSION}:/usr/local/nvidia \
	$TFLOW_SING_IMAGEFILE <<EOF
python -c "import tensorflow"
EOF