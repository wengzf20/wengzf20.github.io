---
layout: post
title: "CompressibleInterFoam: theory, implementation and examples"
date: 2024-01-15 00:00:00
description: this post is intended for a thorough introduction to compressibleInterFoam, including the governing equation, implementation in OpenFOAM and some demos.
tags: OpenFOAM
categories: Solvers
thumbnail: assets/img/CFDfoundationLogo.png
toc:
  sidebar: left
---
<!-- 
This theme supports rendering beautiful math in inline and display modes using [MathJax 3](https://www.mathjax.org/) engine. You just need to surround your math expression with `$$`, like `$$ E = mc^2 $$`. If you leave it inside a paragraph, it will produce an inline expression, just like $$ E = mc^2 $$.
 -->

`This page is under development`

CompressibleInterFoam is a default multiphase solver in OpenFOAM. It is capable of solving two compressible, non-isothermal immiscible fluids, with/without cavitation. The phase interface is captured using volume of fluid (VoF) approach.

<!-- \begin{equation} \label{eq:cauchy-schwarz} \left( \sum{k=1}^n a_k b_k \right)^2 \leq \left( \sum{k=1}^n ak^2 \right) \left( \sum{k=1}^n b_k^2 \right) \end{equation}
Eq. \ref{eq:cauchy-schwarz} is the Cauchy-Schwarz inequality. -->

<h2> Derivation from conservation law </h2>
The mass conservation for individual species are

\begin{equation} \label{eq:mass_alpha1}
\frac{\partial\left(\rho_1 \alpha_1\right)}{\partial t}+\nabla \cdot\left(\rho_1 \boldsymbol{U} \alpha_1\right)=\dot{m} 
\end{equation}

\begin{equation} \label{eq:mass_alpha2}
 \frac{\partial\left(\rho_2 \alpha_2\right)}{\partial t}+\nabla \cdot\left(\rho_2 \boldsymbol{U} \alpha_2\right)=-\dot{m}
\end{equation}

where $$ \alpha_{1}+\alpha_{2} = 1 $$; $$ \dot{m} $$ is the source term from phase change. If there is no phase change, $$ \dot{m} $$ is zero.

Consider only the volume fraction in the l.h.s., and move other parts to the r.h.s. to be the source term. Eq. \ref{eq:mass_alpha1} and \ref{eq:mass_alpha2} were re-written as

\begin{equation} \label{eq:mass_alpha1_comp}
\frac{\partial \alpha_1}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_1\right)=-\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t} + \frac{\dot{m}}{\rho_1}
\end{equation}

\begin{equation} \label{eq:mass_alpha2_comp}
\frac{\partial \alpha_2}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_2\right)=-\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t} - \frac{\dot{m}}{\rho_2}
\end{equation}

The sum of these two equations lead to

\begin{equation} \label{eq:divU}
\nabla \cdot\boldsymbol{U}=-\left(\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t}+\frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t}\right)+\dot{m}\left(\frac{1}{\rho_1}-\frac{1}{\rho_2}\right)
\end{equation}

The 1st and 2nd term in the r.h.s. are the compressibility and phase change effects.

Insert it to Eq. \ref{eq:mass_alpha1_comp} by adding and substracting $$ \alpha_{1}\nabla \cdot\boldsymbol{U} $$

\begin{equation} \label{eq:mass_alpha1_final}
\frac{\partial \alpha_1}{\partial t}+\nabla \cdot\left(\boldsymbol{U} \alpha_1\right)=\alpha_1 \alpha_2 \left(\frac{1}{\rho_1} \frac{D \rho_1}{D t}-\frac{1}{\rho_2} \frac{D \rho_2}{D t}\right) 
+\alpha_1 \nabla \cdot \boldsymbol{U}+\dot{m}\left(\frac{\alpha_2}{\rho_1}+\frac{\alpha_1}{\rho_2}\right)
\end{equation}

The compressibility, $$ \alpha_1 \nabla \cdot \boldsymbol{U} $$ and phase change are source terms for the alpha equation. They are separated into $$ S_{p} $$ and $$ S_{u} $$ in the MULES algorithm. $$ S_{p} $$ is implicit source term, $$ S_{u} $$ is explicit source term.

<h2> MULES method </h2>
In Eq. \ref{eq:mass_alpha1_final}, it was defined

\begin{equation} 
\mathrm{dgdt}=-\alpha_1 \alpha_2 \left(\frac{1}{\rho_1} \frac{D \rho_1}{D t}-\frac{1}{\rho_2} \frac{D \rho_2}{D t}\right)
\end{equation}

dgdt was calculated in the pEqn, i.e.
```
dgdt =
(
    alpha1*(p_rghEqnComp2 & p_rgh)
    - alpha2*(p_rghEqnComp1 & p_rgh)
);
```

In solving Eq. \ref{eq:mass_alpha1_final}, dgdt was separated according to its sign in each cell

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

$$ S_p = \text{phaseChangeS}[1] -\frac{\mathrm{dgdt}}{\alpha_{2}}, S_u = \text{phaseChangeS}[0] + \frac{\mathrm{dgdt}}{\alpha_{2}} $$

if dgdt < 0

$$ S_p = \text{phaseChangeS}[1] + \frac{dgdt}{\alpha_{1}}, S_u = \text{phaseChangeS}[0] $$

$$ S_p $$, $$ S_u $$ together with other terms were sending to 

```c++
// In src/twoPhaseModels/twoPhaseMixture/VoF/alphaEqn.H
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

In MULES::explicitSolve, the time step was calculated, then limiter was applied, last another *explicitSolve* was called.
```c++
// In src/finiteVolume/fvMatrices/solvers/MULES/MULESTemplates.C
const scalar rDeltaT = 1.0/mesh.time().deltaTValue();
limit(rDeltaT, rho, psi, phi, phiPsi, Sp, Su, psiMax, psiMin, false);
explicitSolve(rDeltaT, rho, psi, phiPsi, Sp, Su); 
// rho - geometricOneField()
// psi - alpha1
// phiPsi - alphaPhi10
// Sp - SpRef
// Su - SuRef + alpha1*divU()
```

In the latter *explicitSolve* called, $$ \alpha_1 $$ for next time step was obtained via
```c++
// In src/finiteVolume/fvMatrices/solvers/MULES/MULESTemplates.C
psiIf =
(
    rho.oldTime().field()*psi0*rDeltaT
    + Su.field()
    - psiIf
)/(rho.field()*rDeltaT - Sp.field());
```

This means:

$$
\alpha_1(t+\Delta t)=\frac{\alpha_1(t)/\Delta t  + \mathrm{Su.field} - \frac{1}{V_P} \sum_f U\alpha_1 S_{f}}{1/\Delta t-\mathrm{Sp.field} }
$$

The corresponding equation was

$$
\frac{\partial \alpha_1}{\partial t}+\nabla \cdot(\boldsymbol{U} \alpha_1)=\alpha_1 S_{p} + S_{u} + \alpha_{1}\nabla\cdot\boldsymbol{U}
$$

(**Note**: Su.field() = $$ S_u+\alpha_{1}\nabla\cdot\boldsymbol{U} $$, $$ \alpha_1 S_{p} + S_{u} $$ is implemented in *alphaSuSp.H* in the solver)

<!-- - <span style="color: red;">**if dgdt > 0**</span>
    $$\alpha_1 S_{p} + S_{u} = \alpha_{1}\text{phaseChangeS}[1]  + \text{phaseChangeS}[0] + (1-\alpha_{1})\frac{\mathrm{dgdt}}{\alpha_{2}} $$
    $$= \alpha_{1}\text{phaseChangeS}[1]  + \text{phaseChangeS}[0] + \mathrm{dgdt} $$

- <span style="color: red;">**if dgdt < 0**</span>
    $$\alpha_1 S_{p} + S_{u} = \alpha_{1}\text{phaseChangeS}[1]  + \text{phaseChangeS}[0] + \mathrm{dgdt} $$

    <span style="color: red;">**These two cases indicate**</span>
    $$\alpha_{1}\text{phaseChangeS}[1]  + \text{phaseChangeS}[0]  = \dot{m}\left(\frac{\alpha_2}{\rho_1}+\frac{\alpha_1}{\rho_2}\right)$$ 
    according to the derivation in the last section. </span> -->

## Pressure-velocity coupling
The velocity field is firstly estimated from the momentum equation, then the velocity field is inserted to Eq. \ref{eq:divU}.

$$
\begin{equation}
\nabla \cdot (\mathbf{H}_{\boldsymbol{U}} - \frac{1}{a_p} \nabla p_{\mathrm{rgh}}) = -\left(\frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t} + \frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t}\right) + \dot{m}\left(\frac{1}{\rho_1} - \frac{1}{\rho_2}\right)
\end{equation}
$$

The source code for pressure-possion equation is

```
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

- fvc::div(phiHbyA): $$ \nabla \cdot \mathbf{H}_{\boldsymbol{U}} $$
- fvm::laplacian(rAUf, p_rgh): $$ \nabla \cdot ( \frac{1}{a_p} \nabla p_{\mathrm{rgh}}) $$
- Sp_rgh: source term from phase change, i.e. $$ \dot{m}\left(\frac{1}{\rho_1}-\frac{1}{\rho_2}\right) $$
- p_rghEqnComp1(): $$ \frac{\alpha_1}{\rho_1} \frac{D \rho_1}{D t} $$
- p_rghEqnComp2(): $$ \frac{\alpha_2}{\rho_2} \frac{D \rho_2}{D t} $$

### Consideration of the compressibility
`coming soon`
<!-- By assuming constant temperature, the pressure and density can be related with
$$d\rho_{i} = \left(\frac{\partial \rho_{i}}{\partial p}\right)_{T}dp = \psi_{i}dp\text{\quad or\quad}\rho_{i}^* = \rho_{i}^n + \psi_{i}(p^* - p^n)$$  
In the pimple loop, the pressure possion equation might be solved for several times in a single time step (for either *nOuterCorrectors* > 1 or *nCorrectors* > 1),  -->

<!-- first, the pressure effect on density was consider in the equation -->


## Phase change model

The phase change model was included in the $$ \ alpha$ equation via

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

### The Schnerr-Sauer model
#### Source term of alphaEqn

```c++
Foam::Pair<Foam::tmp<Foam::volScalarField::Internal>>
Foam::twoPhaseChangeModels::SchnerrSauer::mDotAlphal() const
{
    ...
    const volScalarField::Internal pCoeff(this->pCoeff(p));
    ...
    return Pair<tmp<volScalarField::Internal>>
    (
        Cc_*limitedAlpha1*pCoeff*max(p - pSat(), p0_),
        Cv_*(1.0 + alphaNuc() - limitedAlpha1)*pCoeff*min(p - pSat(), p0_)
    );
}
    // Note: 
    // pCoeff = (3*rho1()*rho2())*sqrt(2/(3*rho1()))
    //   *rRb(limitedAlpha1)/(rho*sqrt(mag(p - pSat()) + 0.01*pSat()));
```
$$
\dot{m}=\underbrace{\alpha_{v}\dot{m}_{c}}_{\text{condensation}}+\underbrace{\alpha_{l}\dot{m}_{v}}_{\text{vaporization}}
$$

$$
\begin{aligned}
& \dot{m}_{c} = C_{c}\alpha_{l}\frac{3\rho_{l}\rho_{v}}{\rho R_{b} \sqrt{|P-P_{s}|}}\sqrt{\frac{2}{3\rho_{l}}}max(P-P_{s},0) \geq 0 \\
&\dot{m}_{v} = C_{v}(1+\alpha_{Nuc}-\alpha_{l})\frac{3\rho_{l}\rho_{v}}{\rho R_{b} \sqrt{|P-P_{s}|}}\sqrt{\frac{2}{3\rho_{l}}}min(P-P_{s},0) \leq 0\\
&\text{pcoeff} = \frac{3\rho_{l}\rho_{v}}{\rho R_{b} \sqrt{|P-P_{s}|}}\sqrt{\frac{2}{3\rho_{l}}}
\end{aligned}
$$

```c
Foam::Pair<Foam::tmp<Foam::volScalarField::Internal>>
Foam::twoPhaseChangeModels::cavitationModel::Salpha
(
    volScalarField& alpha
) const
{
    ...
    const volScalarField::Internal vDotcAlphal(alphalCoeff*mDotAlphal[0]());
    const volScalarField::Internal vDotvAlphal(alphalCoeff*mDotAlphal[1]());
    return Pair<tmp<volScalarField::Internal>> // mdot =  \alpha_{l}S_{p} + S_{u}
    (
        1.0*vDotcAlphal, // Su
        vDotvAlphal - vDotcAlphal // Sp
    );
}
```

The source term in $\alpha_{l}$ equation, $S_{\alpha}$ was seperated as 

$$
\begin{aligned}
S_{\alpha} &= \alpha_{l,coeff}\dot{m} \\
&= \alpha_{l,coeff}(\alpha_{l}\dot{m}_{v} + \alpha_{v}\dot{m}_{c}) \\
&= \alpha_{l,coeff}[\alpha_{l}(\dot{m}_{v}-\dot{m}_{c}) + \dot{m}_{c}]\\
&= \underbrace{\alpha_{l}\alpha_{l,coeff}(\dot{m}_{v}-\dot{m}_{c})}_{\alpha_{l} \text{Sp} <0} + \underbrace{\alpha_{l,coeff}\dot{m}_{c}}_{\text{Su} >0} \\
&= \alpha_{l}\text{Sp} + \text{Su}
\end{aligned}
$$

$$
\alpha_{l,coeff} = \left(\frac{1}{\rho_l}-\alpha_{l}\left(\frac{1}{\rho_l}-\frac{1}{\rho_v}\right)\right) > 0
$$

In OpenFOAM, fvm::Sp handles negative source term. fvm::Sp makes the negative source term implicit so it contributes to the diagonal and increase the . This can help convergence when the source term is negative on the rhs (sink term). (ref.: OpenFOAM® Beginner training session)

#### Source term of pEqn
The mass transfer rate in pEqn, $\dot{m}_{p}$ was defined as

$$
\dot{m}_{p} = -\frac{\dot{m}}{P-P_{s}} = \underbrace{-\frac{\alpha_{l}\dot{m}_{v}}{P-P_{s}}}_{\dot{m}_{p,v} \leq 0 } - \underbrace{\frac{(1-\alpha_{l})\dot{m}_{c}}{P-P_{s}}}_{\dot{m}_{p,c} \geq 0 }  = 
\dot{m}_{p,v} - \dot{m}_{p,c}  
$$

```c++
Foam::Pair<Foam::tmp<Foam::volScalarField::Internal>>
Foam::twoPhaseChangeModels::SchnerrSauer::mDotP() const
{
    const volScalarField::Internal apCoeff(limitedAlpha1*pCoeff);

    return Pair<tmp<volScalarField::Internal>>
    (
        Cc_*(1.0 - limitedAlpha1)*pos0(p - pSat())*apCoeff,

        (-Cv_)*(1.0 + alphaNuc() - limitedAlpha1)*neg(p - pSat())*apCoeff
    );
}
```

$$
\begin{aligned}
& \dot{m}_{p,c} = C_{c}(1-\alpha_{l})*\underbrace{\alpha_{l}\text{pcoeff}}_{\text{apcoeff}}*\text{pos0}(P-P_{s}) =\frac{1-\alpha_{l}}{P-P_{s}}\dot{m}_{c} \geq 0 \\
&\dot{m}_{p,v} = -C_{v}(1+\alpha_{Nuc}-\alpha_{l})*\underbrace{\alpha_{l}\text{pcoeff}}_{\text{apcoeff}}*\text{neg}(P-P_{s}) = -\frac{\alpha_{l}}{P-P_{s}}\dot{m}_{v} \leq 0
\end{aligned}
$$

```
Foam::tmp<Foam::fvScalarMatrix>
Foam::twoPhaseChangeModels::cavitationModel::Sp_rgh
(
    const volScalarField& rho,
    const volScalarField& gh,
    volScalarField& p_rgh
) const
{
    const volScalarField::Internal pCoeff(1.0/rho1() - 1.0/rho2());
    const Pair<tmp<volScalarField::Internal>> mDotP = this->mDotP();

    const volScalarField::Internal vDotcP(pCoeff*mDotP[0]);
    const volScalarField::Internal vDotvP(pCoeff*mDotP[1]);

    return
        (vDotvP - vDotcP)*(pSat() - rho()*gh())
      - fvm::Sp(vDotvP - vDotcP, p_rgh);
}
```

$$
\begin{aligned}
S_{P}&= \left(\frac{1}{\rho_{l}}-\frac{1}{\rho_{v}}\right)\dot{m}\\
& = \left(\frac{1}{\rho_{l}}-\frac{1}{\rho_{v}}\right)(\dot{m}_{p,v} - \dot{m}_{p,c})(P_{s}-P)\\
& = \underbrace{\left(\frac{1}{\rho_{l}}-\frac{1}{\rho_{v}}\right)(\dot{m}_{p,v} - \dot{m}_{p,c})P_{s}}_{\text{Su}>0}\quad \underbrace{-\left(\frac{1}{\rho_{l}}-\frac{1}{\rho_{v}}\right)(\dot{m}_{p,v} - \dot{m}_{p,c})P}_{P*\text{Sp}<0}\\
\end{aligned}
$$

(Note: ${1}/{\rho_{l}}-{1}/{\rho_{v}} <0$)


## Temperature Equation
`coming soon`

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

