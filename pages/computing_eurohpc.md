---
layout: site
permalink: /computing_eurohpc.html
---

# EuroHPC

The [European High Performance Computing Joint Undertaking](https://eurohpc-ju.europa.eu/index_en)
(EuroHPC JU) operates a network of supercomputers across Europe and distributes time on
them through periodic access calls. FCC has been awarded GPU time on MareNostrum 5
through a Regular Access call, granted for **FCC reconstruction tasks**.

## MareNostrum 5

[MareNostrum 5](https://www.bsc.es/marenostrum/marenostrum-5) is hosted at the
Barcelona Supercomputing Center (BSC). It is divided into several partitions; our
allocation is on the accelerated (**ACC**) partition, whose nodes carry four NVIDIA
Hopper GPUs each.

The full user documentation is the
[BSC Support Knowledge Center](https://www.bsc.es/supportkc/docs/MareNostrum5/intro/);
the sections below cover only what is specific to our allocation.

## Getting access

If you work on FCC reconstruction tasks and would like to use the resources, please
contact [Lena Herrmann](mailto:lena.maria.herrmann@cern.ch). In your message, please
include:

- a one-sentence description of the project you plan to work on
- your full name
- your affiliation
- your nationality

BSC requires these details for the account application.

You will then receive an invitation email with a link to the user responsibility
agreement, which you need to sign electronically. Once the account is created, you will
receive further emails containing your user name and instructions on how to access and
run on the cluster.

## Call specifications

Our allocation is the EuroHPC Regular Access call **EHPC-REG-2026R01-012**

| | |
|---|---|
| Allocation | 20 750 node hours on MareNostrum 5 ACC |
| Node configuration | 4 NVIDIA Hopper GPUs, 64 GB HBM2 memory each |
| Period | 12 months, 10 August 2026 – 10 August 2027 |
| Account | `ehpc1013` |
| QoS | `acc_ehpc` |


## Network access

MareNostrum 5 has **no outbound internet access from any node inside the cluster**. You cannot download packages,
clone repositories, or transfer data from within a session on the cluster.

All data movement must be initiated from your local machine, connecting to the
dedicated transfer nodes `transfer1.bsc.es` – `transfer4.bsc.es`:

```bash
# run this on your local machine
scp -r myfile.tar.gz <username>@transfer1.bsc.es:/path/to/destination
```



## File structure

Our project directories on the two GPFS filesystems are:

| Path | Use |
|---|---|
| `/gpfs/projects/ehpc1013/` | data and software that should be shared within the project |
| `/gpfs/scratch/ehpc1013/` | temporary files, and the datasets used by running jobs |

Datasets belong on `scratch`.

EOS is not mounted on MareNostrum 5, so any data you need from CERN must be copied
across explicitly — see [Network access](#network-access) above for how to do this from
your local machine.

Details on quotas and filesystem behaviour are in the
[BSC filesystem documentation](https://www.bsc.es/supportkc/docs/MareNostrum5/storage/).


## Environment

Software provided by BSC is available through the `module` system, described under
[software environment](https://www.bsc.es/supportkc/docs/MareNostrum5/environment/).

We have a conda environment for MLPF training:

```bash
module load miniforge
source activate mlpf
```


If you need BSC to install or license software for you, contact
[Lena Herrmann](mailto:lena.maria.herrmann@cern.ch) to coordinate.

## Launching Slurm jobs

BSC uses Slurm as its batch system; the full reference is the
[BSC Slurm documentation](https://www.bsc.es/supportkc/docs/MareNostrum5/slurm/).

### Interactive sessions

A single node with all four GPUs:

```bash
salloc -A ehpc1013 -q acc_ehpc -J myjob -t 00:30:00 -n 1 -c 80 --gres=gpu:4
```

Two nodes, four GPUs each:

```bash
salloc -A ehpc1013 -q acc_ehpc -J myjob -t 00:10:00 --nodes 2 \
       --ntasks-per-node 1 --cpus-per-task 20 --gres=gpu:4
```

Adapt these to your needs; see the BSC documentation for the available options.


### Batch jobs

The example below is a single-node template that runs distributed training with
`torchrun` on all four GPUs of one node. Increase `--nodes` to scale it up.

```bash
#!/bin/bash
#SBATCH --job-name=myrecojob
#SBATCH --output=logs-torchrun/%j.out
#SBATCH --error=logs-torchrun/%j.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=80
#SBATCH --gres=gpu:4
#SBATCH --ntasks-per-node=1
#SBATCH --time=2:30:00
#SBATCH --qos=acc_ehpc
#SBATCH --account=ehpc1013

# modules
module load MINIFORGE/24.3.0-0
source "/gpfs/apps/MN5/ACC/MINIFORGE/24.3.0-0/etc/profile.d/conda.sh"
conda activate /gpfs/apps/MN5/ACC/MINIFORGE/24.3.0-0/envs/mlpf

# change to working directory
cd <your/working/directory>

# ---------------------------
# User-configurable variables
# ---------------------------
NODES=${NODES:-1}
GPUS_PER_NODE=${GPUS_PER_NODE:-4}
LOCAL_BATCH=${LOCAL_BATCH:-24}
MODEL_PREFIX=${MODEL_PREFIX:-/gpfs/scratch/ehpc1013/<username>/output/${NODES}nodes_${GPUS_PER_NODE}gpn}
WANDB_NAME=${WANDB_NAME:-run_${NODES}nodes_${GPUS_PER_NODE}gpn}

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export SLURM_CPU_BIND=none
export GPUS_PER_NODE=${GPUS_PER_NODE:-4}
export NODE_RANK=$SLURM_PROCID
export NUM_PROCS=$((SLURM_NNODES * GPUS_PER_NODE))
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500

echo "NODE_RANK: $NODE_RANK"
echo "NNODES: $SLURM_NNODES"
echo "NUM_PROCS: $NUM_PROCS"
echo "MASTER_ADDR: $MASTER_ADDR"
echo "MASTER_PORT: $MASTER_PORT"

srun --ntasks="$SLURM_NNODES" --ntasks-per-node=1 \
  torchrun \
    --nnodes="$SLURM_NNODES" \
    --nproc_per_node="$GPUS_PER_NODE" \
    --master_addr="$MASTER_ADDR" \
    --master_port="$MASTER_PORT" \
    --rdzv_backend=c10d \
    --rdzv_endpoint="$MASTER_ADDR:$MASTER_PORT" \
    --rdzv_id="$SLURM_JOB_ID" \
    --node_rank="$SLURM_PROCID" \
    -m src.train_lightning1 \
      --data-train /gpfs/scratch/ehpc1013/<username>/mydata \
      --data-config config_files/config_hits_track_v4.yaml \
      --network-config src/models/wrapper/example_mode_gatr_noise.py \
      --model-prefix "${MODEL_PREFIX}" \
      --num-workers 4 \
      --gpus "$GPUS_PER_NODE" \
      --batch-size "$LOCAL_BATCH" \
      --num-epochs 1 \
      --fetch-step 1 \
      --log-wandb \
      --wandb-displayname "${WANDB_NAME}" \
      --wandb-projectname <your-wandb-project> \
      --wandb-entity <your-wandb-entity> \
      --frac_cluster_loss 0 \
      --qmin 3 \
      --use-average-cc-pos 0.98 \
      --train-val-split 0.98 \
      --fetch-by-files \
      --train-batches 10000

echo "Training succeeded."
```

Submit it with `sbatch job.sh` and monitor with `squeue -u $USER`. 

## Weights & Biases logging

The cluster has no outbound internet access, so W&B cannot stream metrics live. Run it
in offline mode and sync the runs afterwards from a machine that does have network
access.

Mount the W&B run directory from the cluster onto your EOS space, via a transfer node:

```bash
# on lxplus
sshfs -o workaround=rename <username>@transfer1.bsc.es:/gpfs/projects/ehpc1013/HitPF/wandb /eos/user/<u>/<username>/wandbsync
```

Then sync the offline runs:

```bash
wandb sync --include-offline /eos/user/<u>/<username>/wandbsync/offline-run-<timestamp>-<id>/run-<id>.wandb
```


## Acknowledgements

Publications describing results obtained with EuroHPC JU resources must acknowledge
them, using the following wording:

*We acknowledge EuroHPC JU for awarding the project ID EHPC-REG-2026R01-012 access to
MareNostrum5 at BSC, Spain.*

Please also include the EuroHPC logo on presentation slides; the official versions are
available from the
[EuroHPC JU visual page](https://www.eurohpc-ju.europa.eu/media-events/media/visuals_en).