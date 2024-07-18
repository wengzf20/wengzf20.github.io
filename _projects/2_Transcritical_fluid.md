---
layout: page
title: Transcritical fluid
description: Chemical propulsion systems utilize high pressure to improve thermal efficency. The fluid under transcritical or supercritical states exhibits multi-scale physical behaviours and pose challenges to numerical simulation ...
img: assets/img/project_thumbnail/N2Jet.png
importance: 2
category: 
giscus_comments: false
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

<h2> Pressure-based supercritical flow solver </h2>

<p style="text-align: justify;">
Injection, mixing and combustion processes in rocket engines typically take place at trans- or super-critical conditions. Liquified fuel and oxidizer were injected at cryogenic and high pressure state. Accurate descriptions of real-fluid properties are essential for numerical simulation. A pressure-based solver was developed on open-source platform, DeepFlame [1], by connecting OpenFOAM and Cantera. The real fluid model in Cantera, including Peng-Robinson equation of state and corresponding thermodynamic functions, transport properties, was used to replace the ideal gas assumption in OpenFOAM. The pressure equation was revised according to Jarczyk and Pfitzner's work [2]. The performance of the solver was demonstrated using nitrogen convection and injection cases [2-3]. 
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-9 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/N2Convection2.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Nitrogen convection case proposed by Jarczyk and Pfitzner [2].
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-9 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/N2Convection1.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Periodical nitrogen convection case proposed by Ma et al. [3].
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-9 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/rho_field.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    LES simulation for case 4 in Mayer's experiment [4].
</div>

<a href="javascript:togglebibBlock('ref1')" class="textlink">References</a>
<div id="ref1" class="bibBlock noshow">
<pre>
[1] <img src="/assets/img/project_thumbnail/deepflame.jpg" style="height: 2em;vertical-align: middle;"> <a href="https://github.com/deepmodeling/deepflame-dev">https://github.com/deepmodeling/deepflame-dev</a>
[2] M.-M. Jarczyk, and M. Pfitzner, in 50th AIAA Aerospace Sciences Meeting Including the New Horizons Forum and Aerospace Exposition (American Institute of Aeronautics and Astronautics, 2012).
[3] P.C. Ma, Y. Lv, and M. Ihme, “An entropy-stable hybrid scheme for simulations of transcritical real-fluid flows,” Journal of Computational Physics 340, 330–357 (2017).
[4] W. Mayer, J. Telaar, R. Branam, G. Schneider, and J. Hussong, “Raman Measurements of Cryogenic Injection at Supercritical Pressure,” Heat and Mass Transfer 39(8), 709–719 (2003).
</pre>
</div>