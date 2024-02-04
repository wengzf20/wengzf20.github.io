---
layout: post
title: An introduction to compressibleInterFoam
date: 2024-01-15 00:00:00
description: the connection between source code and governing equations were illustrated.
tags: OpenFOAM
categories: Solvers
thumbnail: assets/img/CFDfoundationLogo.png
toc:
  sidebar: left
---

<h2> Under development </h2>

CompressibleInterFoam is a default multiphase solver in OpenFOAM. It is capable of solving two compressible, non-isothermal immiscible fluids, with/without cavitation. The phase interface is captured using volume of fluid (VoF) approach.

<!-- \begin{equation} \label{eq:cauchy-schwarz} \left( \sum{k=1}^n a_k b_k \right)^2 \leq \left( \sum{k=1}^n ak^2 \right) \left( \sum{k=1}^n b_k^2 \right) \end{equation}
Eq. \ref{eq:cauchy-schwarz} is the Cauchy-Schwarz inequality. -->

<h2> Derivation from conservation law </h2>
The mass conservation for individual species are

$$
\frac{\partial\left(\rho_1 \alpha_1\right)}{\partial t}+\nabla \cdot\left(\rho_1 \boldsymbol{U} \alpha_1\right)=\dot{m} 
$$

$$
 \frac{\partial\left(\rho_2 \alpha_2\right)}{\partial t}+\nabla \cdot\left(\rho_2 \boldsymbol{U} \alpha_2\right)=-\dot{m}
$$

where $\alpha_{1}+\alpha_{2} = 1$; $\dot{m}$ is the source term from phase change. If there is no phase change, $\dot{m}$ is zero.

Consider only the volume fraction in the l.h.s., and move other parts to the r.h.s. to be the source term.

$$
\frac{\partial \alpha_1}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_1\right)=-\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t} + \frac{\dot{m}}{\rho_1}
$$

$$
\frac{\partial \alpha_2}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_2\right)=-\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t} - \frac{\dot{m}}{\rho_2}
$$

The sum of these two equations lead to

$$
\nabla \cdot\boldsymbol{U}=-\left(\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t}+\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t}\right)+\dot{m}\left(\frac{1}{\rho_1}-\frac{1}{\rho_2}\right)
$$

The 1st and 2nd term in the r.h.s. are the compressibility and phase change effects.

Insert it to the $\alpha_1$ equation by adding and substracting $\alpha_{1}\nabla \cdot\boldsymbol{U}$

$$
\frac{\partial \alpha_1}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_1\right)=\alpha_1 \alpha_2 \left(\frac{1}{\rho_1} \frac{D \rho_1}{D t}-\frac{1}{\rho_2} \frac{D \rho_2}{D t}\right)
$$

$$
+\alpha_1 \nabla \cdot \boldsymbol{U}+\dot{m}\left(\frac{\alpha_2}{\rho_1}+\frac{\alpha_1}{\rho_2}\right)
$$

The compressibility, $\alpha_1 \nabla \cdot \boldsymbol{U}$ and phase change are source terms for the alpha equation. They are separated into $S_{p}$ and $S_{u}$ in the MULES algorithm. $S_{p}$ is implicit source term, $S_{u}$ is explicit source term.

<h2> MULES method </h2>
In the $\alpha_{1}$ eqaution, it was defined

$$
\mathrm{dgdt}=-\alpha_1 \alpha_2 \left(\frac{1}{\rho_1} \frac{D \rho_1}{D t}-\frac{1}{\rho_2} \frac{D \rho_2}{D t}\right)
$$

dgdt was calculated in the pEqn, i.e.
```c++
dgdt =
(
    alpha1*(p_rghEqnComp2 & p_rgh)
    - alpha2*(p_rghEqnComp1 & p_rgh)
);
```

In solving the $\alpha$ equation, dgdt was calculated according to its sign

```
if (dgdt[celli] > 0.0)
{
    SpRef[celli] -= dgdt[celli]/max(1.0 - alpha1[celli], 1e-4);
    SuRef[celli] += dgdt[celli]/max(1.0 - alpha1[celli], 1e-4);
}
else if (dgdt[celli] < 0.0)
{
    SpRef[celli] += dgdt[celli]/max(alpha1[celli], 1e-4);
}
```

The code means, if dgdt > 0
$$S_p = phaseChangeS[1] -\frac{\mathrm{dgdt}}{\alpha_{2}}, S_u = phaseChangeS[0] + \frac{\mathrm{dgdt}}{\alpha_{2}}$$
if dgdt < 0
$$S_p = phaseChangeS[1] + \frac{dgdt}{\alpha_{1}}, S_u = phaseChangeS[0]$$

$S_p$, $S_u$ together with other terms were sending to 

```c++
if (divU.valid())
{
    MULES::explicitSolve
    (
        geometricOneField(), // 1
        alpha1,
        phiCN,  // phi for Euler ddt method, i.e. U
        alphaPhi10, // alpha*U
        Sp(),
        (Su() + divU()*min(alpha1(), scalar(1)))(),
        oneField(),
        zeroField()
    );
}
```
> src/twoPhaseModels/twoPhaseMixture/VoF/alphaEqn.H \

In MULES::explicitSolve, the time step was calculated, then limiter was applied, last another *explicitSolve* was called.
```c++
const scalar rDeltaT = 1.0/mesh.time().deltaTValue();
limit(rDeltaT, rho, psi, phi, phiPsi, Sp, Su, psiMax, psiMin, false);
explicitSolve(rDeltaT, rho, psi, phiPsi, Sp, Su); 
// rho - geometricOneField()
// psi - alpha1
// phiPsi - alphaPhi10
// Sp - SpRef
// Su - SuRef + alpha1*divU()
```
> src/finiteVolume/fvMatrices/solvers/MULES/MULESTemplates.C

The *explicitSolve* called, new $\alpha_1$ was obtained via
```c++
psiIf =
(
    rho.oldTime().field()*psi0*rDeltaT
    + Su.field()
    - psiIf
)/(rho.field()*rDeltaT - Sp.field());
```
> src/finiteVolume/fvMatrices/solvers/MULES/MULESTemplates.C


This means:


$$
\alpha_1(t+\Delta t)=\frac{\alpha_1(t)/\Delta t  + \mathrm{Su.field} - \frac{1}{V_P} \sum_f U\alpha_1 S_{f}}{1/\Delta t-\mathrm{Sp.field} }
$$

<span style="color: red;">**The corresponding equation was**</span>
$$\frac{\partial \alpha_1}{\partial t}+\nabla \cdot(\boldsymbol{U} \alpha_1)=\alpha_1 S_{p} + S_{u} + \alpha_{1}\nabla\cdot\boldsymbol{U}$$
(**Note**: Su.field() = $S_u+\alpha_{1}\nabla\cdot\boldsymbol{U}$)

- <span style="color: red;">**if dgdt > 0**</span>
    $$\alpha_1 S_{p} + S_{u} = \alpha_{1}phaseChangeS[1]  + phaseChangeS[0] + (1-\alpha_{1})\frac{\mathrm{dgdt}}{\alpha_{2}} $$
    $$= \alpha_{1}phaseChangeS[1]  + phaseChangeS[0] + \mathrm{dgdt} $$

- <span style="color: red;">**if dgdt < 0**</span>
    $$\alpha_1 S_{p} + S_{u} = \alpha_{1}phaseChangeS[1]  + phaseChangeS[0] + \mathrm{dgdt} $$

    <span style="color: red;">**These two cases indicate**</span>
    $$\alpha_{1}phaseChangeS[1]  + phaseChangeS[0]  = \dot{m}\left(\frac{\alpha_2}{\rho_1}+\frac{\alpha_1}{\rho_2}\right)$$ 
    according to the derivation in the last section. </span>


(**Note**: $\alpha_1 S_{p}$ + $S_{u}$ is implemented in *alphaSuSp.H* in the solver)

## Pressure-velocity coupling
The velocity field is firstly estimated from the momentum equation, then the velocity field is inserted to the Possion equation 

$$\nabla \cdot (\mathbf{H}_{\boldsymbol{U}} - \frac{1}{a_p} \nabla p_{\mathrm{rgh}})=-\left(\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t}+\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t}\right)+\dot{m}\left(\frac{1}{\rho_1}-\frac{1}{\rho_2}\right)$$

The source code for pressure-possion equation is

```bash
fvScalarMatrix p_rghEqnIncomp
(
    fvc::div(phiHbyA) - fvm::laplacian(rAUf, p_rgh)
    == Sp_rgh
);

solve
(
    p_rghEqnComp1() + p_rghEqnComp2() + p_rghEqnIncomp
);
```

where *p_rghEqnIncomp* means the incompressible part while *p_rghEqnComp1* and *p_rghEqnComp2* are compressible parts corresponding to the two phases.

- fvc::div(phiHbyA): $\nabla \cdot \mathbf{H}_{\boldsymbol{U}}$
- fvm::laplacian(rAUf, p_rgh): $\nabla \cdot ( \frac{1}{a_p} \nabla p_{\mathrm{rgh}})$
- Sp_rgh: source term from phase change, i.e. $\dot{m}\left(\frac{1}{\rho_1}-\frac{1}{\rho_2}\right)$
- p_rghEqnComp1(): $\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t}$
- p_rghEqnComp2(): $\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t}$

### Consideration of the compressibility

By assuming constant temperature, the pressure and density can be related with
$$d\rho_{i} = \left(\frac{\partial \rho_{i}}{\partial p}\right)_{T}dp = \psi_{i}dp\text{\quad or\quad}\rho_{i}^* = \rho_{i}^n + \psi_{i}(p^* - p^n)$$  
In the pimple loop, the pressure possion equation might be solved for several times in a single time step (for either *nOuterCorrectors* > 1 or *nCorrectors* > 1), 

- first, the pressure effect on density was consider in the equation

    $$\frac{\alpha_i}{\rho_i} \frac{D \rho_i}{D t} = \frac{\alpha_i}{\rho_i}\left(\frac{\partial \rho}{\partial t} + \boldsymbol{U}\cdot\nabla\rho\right) = \frac{\alpha_i}{\rho_i}\left(\frac{\partial \rho_i^n}{\partial t}  + \psi_{i}*correction(\frac{\partial p}{\partial t}) + \boldsymbol{U}\cdot\nabla\rho\right)$$

    The corresponding code was
    ```c++
    p_rghEqnComp1 =
        (
            (fvc::ddt(alpha1, rho1) + fvc::div(alphaPhi1*rho1f))/rho1
            - fvc::ddt(alpha1) - fvc::div(alphaPhi1)
            + (alpha1*psi1/rho1)*correction(fvm::ddt(p_rgh))
        );
    p_rghEqnComp1.ref() *= pos(alpha1); //pos(s) - return (s > 0) ? 1: 0;
    ```
    i.e.
    $$\frac{1}{\rho_1^*}\left(\frac{\partial\left(\alpha_1 \rho_1^*\right)}{\partial t}+\nabla \cdot\left(\alpha_1 \boldsymbol{U} \rho_1^*\right)\right) -\left(\frac{\partial \alpha_1}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_1\right)\right) +  \frac{\alpha_{1}\psi_{1}}{\rho_{1}}*correction(\frac{\partial p}{\partial t})$$

    **Note:** In the solver, p_rgh was used instead of p, this was correction for g = 0. Correction is needed if g might be considerred.

- second, the density was updated after solving the pressure equation
    ```c++
    mixture.thermo1().correctRho(psi1*(p_rgh - p_rgh_0));
    mixture.thermo2().correctRho(psi2*(p_rgh - p_rgh_0));
    ```


<!-- $$
d\rho_{i} = \psi_{i}dp \rightarrow \mathrm{dgdt}=\left(\frac{\psi_1}{\rho_1} -\frac{\psi_2}{\rho_2}\right) \frac{D P}{D t}
$$ -->

## Phase change model

The phase change model was included in the $\alpha$ equation via

```c++
Pair<tmp<volScalarField::Internal>> phaseChangeS
(
    phaseChange.Salpha(alpha1)
);

if (phaseChangeS[0].valid())
{
    Su = phaseChangeS[0];
    Sp = phaseChangeS[1];
}
```

and pressure equation via

```bash
fvScalarMatrix Sp_rgh(phaseChange.Sp_rgh(rho, gh, p_rgh));
```

## Temperature Equation
coming soon

<!-- ```bash
fvScalarMatrix TEqn
(
    fvm::ddt(rho, T) + fvm::div(rhoPhi, T) - fvm::Sp(contErr, T)
    - fvm::laplacian(turbulence.alphaEff(), T)
    + (
        fvc::div(fvc::absolute(phi, U), p)()() // - contErr/rho*p
        + (fvc::ddt(rho, K) + fvc::div(rhoPhi, K))()()
        - (U()&(fvModels.source(rho, U)&U)()) - contErr*K
    )
    *(
        alpha1()/mixture.thermo1().Cv()()
        + alpha2()/mixture.thermo2().Cv()()
    )
    ==
    fvModels.source(rho, T)
);
```
 $$\frac{\partial \rho T}{\partial t} + \nabla\cdot(\rho \boldsymbol{U} T) - err*T - \nabla\cdot(\alpha_{eff}\nabla T) $$ 
 $$+ (\frac{\alpha_{1}}{C_{v,1}} + \frac{\alpha_{2}}{C_{v,2}})$$
 $$*[\nabla\cdot(U p) + \frac{\partial \rho K}{\partial t} + \nabla\cdot(\rho\boldsymbol{U} K) $$
 
 $$- U\otimes(fvSource(\rho U)\otimes U) - err*K]$$ 
 $$== fvSource(\rho T)$$

  $$\frac{\partial \rho T}{\partial t} + \nabla\cdot(\rho \boldsymbol{U} T) - \nabla\cdot(\alpha_{eff}\nabla T) $$ 
 $$+ (\frac{\alpha_{1}}{C_{v,1}} + \frac{\alpha_{2}}{C_{v,2}})*[\nabla\cdot(U p) + \frac{\partial \rho K}{\partial t} + \nabla\cdot(\rho\boldsymbol{U} K)]== 0$$

## Counter-gradient transport (interfaceCompression scheme)
In the VoF treatment, a common closure used for counter-gradient transport has the form
> D.A.P. Solis, “Development of a compressible VOF solver for cavitating flows,” (n.d.).

$$
\begin{aligned}
& \alpha_1 \rho \frac{\mathrm{D} T}{\mathrm{D} t}+\frac{\alpha_{\mathrm{l}}}{c_{p, 1}} \rho \frac{\mathrm{D} K}{\mathrm{D} t}=\left(\frac{\partial p}{\partial t}+\nabla \cdot\left(k_{\mathrm{l}} \nabla T\right)\right) \frac{\alpha_{\mathrm{l}}}{c_{p, 1}}+\frac{\alpha_{\mathrm{l}}}{c_{p, 1}} \dot{m}_1 h_{\mathrm{g}}-\frac{\rho}{\rho_{\mathrm{l}} c_{p, 1}} \dot{m}_1 h_1 \\
& \alpha_{\mathrm{g}} \rho \frac{\mathrm{D} T}{\mathrm{D} t}+\frac{\alpha_{\mathrm{g}}}{c_{p, \mathrm{~g}}} \rho \frac{\mathrm{D} K}{\mathrm{D} t}=\left(\frac{\partial p}{\partial t}+\nabla \cdot\left(k_{\mathrm{g}} \nabla T\right)\right) \frac{\alpha_{\mathrm{g}}}{c_{p, \mathrm{~g}}}-\frac{\alpha_{\mathrm{g}}}{c_{p, \mathrm{~g}}} \dot{m}_{\mathrm{g}} h_{\mathrm{g}}
\end{aligned}
$$

$$
\begin{array}{r}
\rho \frac{\mathrm{D} T}{\mathrm{D} t}+\left(\frac{\alpha_1}{c_{p, 1}}+\frac{\alpha_{\mathrm{g}}}{c_{p, \mathrm{~g}}}\right)\left(\rho \frac{\mathrm{D} K}{\mathrm{D} t}-\frac{\partial p}{\partial t}\right)-\left(\alpha_1 \nabla \cdot(\right. \\
\left.\cdot\left(\alpha_{\mathrm{Eff}, 1} \nabla T\right)+\alpha_{\mathrm{g}} \nabla \cdot\left(\alpha_{\mathrm{Eff}, \mathrm{g}} \nabla T\right)\right)= \\
\dot{m}_1 h_{\mathrm{g}}\left(\frac{\alpha_1}{c_{p, 1}}+\frac{\alpha_{\mathrm{g}}}{c_{p, \mathrm{~g}}}\right)-\frac{\rho}{\rho_1 c_{p, 1}} \dot{m}_1 h_1,
\end{array}
$$

## Reference
> 1. $\alpha$ equation: Shi, X., Zheng, K., & Yin, B. (2023). Numerical method for gas-liquid two-phase flow with phase change heat transfer considering compressibility using OpenFOAM. International Journal of Thermal Sciences, 188, 108195. 
> 2. momentum equation and coupling: S.T. Miller, H. Jasak, D.A. Boger, E.G. Paterson, and A. Nedungadi, “A pressure-based, compressible, two-phase flow finite volume method for underwater explosions,” Computers & Fluids 87, 132–143 (2013).  -->
