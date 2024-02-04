---
layout: page
title: Detonation wave at elevated pressure
description: Focus on the initiation, structure and stability of gaseous detonation at high preassure where real gas effects are non-negligible.
img: assets/img/project_thumbnail/sootfoil.png
importance: 1
category: 
related_publications: false
# github: true
---
<!-- the script and style -->
<script>
function togglebibBlock(blockid) {
  var id = document.getElementById(blockid);
  if (id) {
    if(id.className.indexOf('bibBlock') != -1) {
        id.className.indexOf('noshow') == -1?id.className = 'bibBlock noshow':id.className = 'bibBlock';
    }
  } else {
    return;
  }
}
</script>

<style>
div.noshow { display: none; }
div.bibBlock {}
</style> 
<!-- the script and style -->

<p style="text-align: justify;">
The research on detonation can be seperated into several regimes using the pressure and density diagram of Schmitt and Bulter [1]. Gas phase detonation focus mainly on low pressure regime with perfect gas assumption while solid explosive or energetic materials lie on high pressure regime. Recently, the research on two-phase RDE partly falls in the regime of liquid phase detonation. However, the regime of gas with elevated pressure seems rarely explored in detonation research. It has been proved that the perfect gas based model fails to capture the detonation speed and cellular structure regularity at elevated pressure [1-2]. 
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/detonationregime.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Pressure and density diagram for different detonation research regime [1].
</div>

<h2> 1. Detonation initiation </h2>
<p style="text-align: justify;">
A critical decay rate model was derived to study the direct detonation initiation at elevated initial pressure. Compared to the perfect gas based model of Eckett et al. [3], the finite molecular volume results in easier initiation while the inter-molecular interaction results in more difficult initiation. 
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/RGeffect_Planar.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Comparison of the real gas effects on the critical decay time calculated with the quasi-unsteady model (symbol) and asymptotic solutions (line).
</div>


<h2> 2. Detonation structure </h2>
<p style="text-align: justify;">
The detonation speed, reaction zone structure of steady detonation wave were studied for both perfect gas and real gas models. Larger detonation speed was obtained for real gas model which agrees better with experimental data. The reaction zone structure depends on various aspects in the real gas model. In addition, uncertainty quantification was performed for parameters in real gas model. 
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/RGeffect_UQ.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The PDF of induction distance when sampling all parameters of the real gas model and the standard deviation of induction distance when sampling the reaction rate constants of R1, R13, R21 and R22.
</div>

<h2> 3. Detonation stability </h2>
<p style="text-align: justify;">
Linear and non-linear stability analysis was performed for 1D detonation for Noble-Abel gas. The finite molecular volume effect stabilizes detonation except for newtonian and weak heat release regimes. Linear stability solutions agree well with numerical simulations.
</p>
<div class="row justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/RGeffect_UQ.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The PDF of induction distance when sampling all parameters of the real gas model and the standard deviation of induction distance when sampling the reaction rate constants of R1, R13, R21 and R22.
</div>


<a href="javascript:togglebibBlock('ref1')" class="textlink">References</a>
<div id="ref1" class="bibBlock noshow">
<pre>
[1] R.G. Schmitt, and P.B. Butler, “Detonation Properties of Gases at Elevated Initial Pressures,” Combustion Science and Technology 106(1–3), 167–191 (1995).
[2] S. Taileb, J. Melguizo-Gavilanes, and A. Chinnayya, “Influence of the equation of state on the cellular structure of gaseous detonationsat elevated pressures.pdf,” (2020).
[3] C.A. Eckett, J.J. Quirk, and J.E. Shepherd, “The role of unsteadiness in direct initiation of gaseous detonations,” Journal of Fluid Mechanics 421, 147–183 (2000).
</pre>
</div>

<a href="javascript:togglebibBlock('ref2')" class="textlink">Related publications</a>
<div id="ref2" class="bibBlock noshow">
<div class="publications" >
  {% bibliography --group_by none --query @*[key=WENGPhys.Fluids2021 || key=WENGCombustionandFlame2023 || key=WENGCombustionandFlame2022 || key=WENGCombustionandFlame2023b || key=LSANA2023]* %}
</div>
</div>
