---
layout: page
title: Laminar flame
description: Researches on laminar flame are essential for the development of combustion chemistry, ignition problem, flame stability ...
img: assets/img/project_thumbnail/laminarflame.png
importance: 3
# category: work
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

<h2> Laminar flame speed </h2>

<p style="text-align: justify;">
Supercritical laminar flame speed was studied for syngas for sCO<sub>2</sub> application. (More is coming)
</p>

<h2> Extrapolation relation </h2>

<p style="text-align: justify;">
Relation between stretch rate and flame speed was derived via asymptotic analysis. The result obtained by Ronney and Sivashinsky [1] was extended from perfect gas to Noble-Abel gas. (More is coming)
</p>

<h2> Jet ignition </h2>

<p style="text-align: justify;">
(More is coming)
</p>



<a href="javascript:togglebibBlock('ref1')" class="textlink">References</a>
<div id="ref1" class="bibBlock noshow">
<pre>
[1] P.D. Ronney, and G.I. Sivashinsky, “A Theoretical Study of Propagation and Extinction of Nonsteady Spherical Flame Fronts,” SIAM J. Appl. Math. 49(4), 1029–1046 (1989).
</pre>
</div>