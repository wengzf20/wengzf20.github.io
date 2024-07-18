---
layout: post
_styles: |
    .container {
    max-width: 950px; 
    }
title: Reactive flow solvers
date: 2024-07-18 00:00:00
description: 
tags: Code
categories: 
thumbnail: assets/img/5.jpg
pretty_table: true
---

`This page will receive periodic updates.`

<h3> Solvers implemented in OpenFOAM </h3>

| Solver | Features | Relevant Links |
| :---------- | :------------ |  :------------ |
|DLBFoam| Dynamic load balancing model for solving chemistry | [Repository](https://github.com/Aalto-CFD/DLBFoam.git) |
|hybridCentralSolvers| `to update` | [Repository](https://github.com/unicfdlab/hybridCentralSolvers.git)|
|EBIDNSFoam| `to update` | [Request](https://vbt.ebi.kit.edu/english/594.php) |
|blastFoam| `to update` | [Origin](https://github.com/synthetik-technologies/blastfoam.git)|
|CTreactingFoam| Reacting flow solver based on OpenFOAM and Cantera; Detailed transport; Strang splitting scheme and a well-balanced splitting scheme; Diagnostic methods: conservative chemical explosive mode analysis (CCEMA), and global pathway analysis (GPA) | [Origin](https://doi.org/10.3390/aerospace9020102) <br> [Repository](https://github.com/UMN-CRFEL/OpenFOAM-Cantera)|
| RSDFoam | Real gas shock and detonation simulation solver in OpenFOAM 9| [Origin](https://linkinghub.elsevier.com/retrieve/pii/S0045793023002372) <br> [Application 1](https://linkinghub.elsevier.com/retrieve/pii/S0010218024000713) |
| detonationFoam | Extension of rhoCentralFoam including HLLC-P, DLBFoam, 2D AMR; Flame and detonation simulation | [Origin](https://doi.org/10.17632/x45zh4nz28.1) <br> [Repository](https://github.com/JieSun-pku/detonationFoam) |
|reactingPimpleCentralFoam | OpenFOAM v2012; Pressure-based semi-implicit; Central-upwind (Kurganov and Tadmor); Detonation simulation with detailed chemistry, mixture of different stabilities, shock-attached and lab coordinates | [Origin](https://doi.org/10.51560/ofj.v4.125) <br> [Repository](https://github.com/Vigneshwaran-Sankar/reactingPimpleCentralFoam-for-detonations) |
|exaFoam| `to update` | `to update` |
|gpuFoam| Tools and extensions for GPU-accelerated OpenFOAM simulations |[Repository](https://github.com/vttresearch/gpuFoam.git)|


<br>
<h3> Solvers in other platforms </h3>

| Solver | Features | Relevant Links |
| :---------- | :------------ |  :------------ |
| PeleC |`to update` |`to update` |
| OpenCFD | `to update`| `to update`|


