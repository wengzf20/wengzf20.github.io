---
layout: post
title: A walkthrough of GPU-accelerated CFD
date: 2026-07-12 00:00:00
description: 
tags: GPU
categories: 
thumbnail: https://www.cyberpowersystem.co.uk/blog/w/wp-content/uploads/2025/09/amd-or-nvidia.jpg
pretty_table: true
toc:
  sidebar: right
---

## Running PeleC on AMD MI325X GPU

This section walks through getting PeleC running on **AMD Instinct MI325X** GPUs with
**ROCm 7.2.0 / HIP**, using the classic **Sedov blast-wave** test case, and reports the
CPU-vs-GPU speedup we measured.

### 1. Setup

Load the ROCm toolchain and point PeleC at its submodules:

```bash
module load rocm-7.2.0/ucx-1.18.0/ompi/5.0.9    # depends on the cluster
export HIP_PLATFORM=amd    # target AMD (use 'nvidia' for NVIDIA)
export PELE_HOME=/path/to/PeleC
export PELE_PHYSICS_HOME=${PELE_HOME}/Submodules/PelePhysics
export AMREX_HOME=${PELE_PHYSICS_HOME}/Submodules/amrex
```

Sanity-check the toolchain is visible via `hipcc --version` and `rocm-smi`.

Then configure PeleC's `GNUmakefile` to select the backend,

```make
USE_MPI = TRUE     # use TRUE, not True or true
USE_HIP = TRUE     # <-- AMD GPU backend
AMD_ARCH = gfx942  # specific to MI325X
USE_CUDA = FALSE
# Profiling
TINY_PROFILE = TRUE
```

Last compile the case, such as `Sedov` via

```bash
make TPLrealclean && make realclean    # clean previous config
make TPL    # third-party libs (SUNDIALS, etc.)
make -j
```

A correct GPU build produces an executable whose name carries the backend, e.g.
`PeleC3d.hip.TPROF.MPI.HIP.ex`. Run the executable via

```bash
mpirun -np 1 ./PeleC3d.hip.TPROF.MPI.HIP.ex example.inp > log.run 2>&1
```

By default AMReX pre-reserves a large device
memory pool at startup — **3/4 of total GPU memory** (192 GiB of the MI325X's 256 GiB) —
as a performance optimization to avoid repeated slow `hipMalloc` calls during the run.
On a **shared** GPU that reservation can't fit, limit the memory size (e.g. 2GB) via

```bash
mpirun -np 1 ./PeleC3d.hip.TPROF.MPI.HIP.ex example.inp \
       amrex.the_arena_init_size=2147483648 > log.run 2>&1
```

### 2. Performance comparison

Same case (Sedov blast, 64³ = 262,144 cells), 1000 timesteps, single rank each.

| Backend           | Clock time | Per timestep | Speedup |
|-------------------|------------------------|--------------|---------|
| CPU (AMD EPYC 9575F, 1 core)      | 373.9 s                | ~0.388 s     | 1×      |
| GPU (MI325X, 1 card)   | 1.85 s                 | ~0.0014 s    | **~200×** |

A single MI325X GPU completes the run **~200× faster** than a single EPYC 9575F CPU core
(~280× per steady-state timestep).
