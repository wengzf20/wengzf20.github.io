---
layout: page
title: Surrogate model
description: Neural network based surrogate models offer great potential for accelerating expensive combustion simulation with acceptable loss of accuracy ...
img: assets/img/project_thumbnail/pinn-feature.png
importance: 4
category: 
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

<h2> Neural network (NN) based regression on real fluid properties </h2>
<p style="text-align: justify;">
The update of real fluid properties takes about 50% (reactive case) [1] or 75% (non-reactive case) of the computation time in supercritical flow simulation. 

Fully connected (or multi-Layer perceptron) type NN was trained to predict the thermo-physical properties of pure nitrogen. The network was optimized to 69 parameters and with prediction error lower than 1% for most conditions.
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/ANN_pred.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Comparison between reference results (line) and prediction of NN (symbol). 
</div>

<p style="text-align: justify;">
The trained NN was coupled with an AI-empowered platform, DeepFlame, to accelerate CFD simulation. Several tests were done using nitrogen convection and supercritical nitrogen injection as examples. The NN significantly reduced the computation time by several folds.
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/ANN_N2Convection.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Simulation results obtained with explicit calculation and NN prediction. 
</div>


<a href="javascript:togglebibBlock('ref1')" class="textlink">References</a>
<div id="ref1" class="bibBlock noshow">
<pre>
[1] P.C. Ma, Y. Lv, and M. Ihme, “An entropy-stable hybrid scheme for simulations of transcritical real-fluid flows,” Journal of Computational Physics 340, 330–357 (2017).
[2] W. Mayer, J. Telaar, R. Branam, G. Schneider, and J. Hussong, “Raman Measurements of Cryogenic Injection at Supercritical Pressure,” Heat and Mass Transfer 39(8), 709–719 (2003).
[3] <img src="/assets/img/project_thumbnail/deepflame.jpg" style="height: 2em;vertical-align: middle;"> <a href="https://github.com/deepmodeling/deepflame-dev">https://github.com/deepmodeling/deepflame-dev</a>
</pre>
</div>