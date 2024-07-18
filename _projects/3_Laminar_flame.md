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


<h2> Spontaneous ignition of hydrogen jet </h2>

<p style="text-align: justify;">
(More is coming)
</p>

<h2> Laminar flame speed </h2>

<p style="text-align: justify;">
Supercritical laminar flame speed was studied for syngas for sCO<sub>2</sub> application. (More is coming)
</p>

<h2> Extrapolation relation </h2>

<p style="text-align: justify;">
Relation between stretch rate and flame speed was derived via asymptotic analysis. The result obtained by Ronney and Sivashinsky [1] was extended from perfect gas to Noble-Abel gas.
</p>

\begin{equation} \label{eq:Evolution_S_R}
    \left(\frac{S}{1+b}\right)^{2}\ln\left(\frac{S}{1+b}\right)^{2} = -\frac{d}{dR}\left(\frac{S}{1+b}\right) + \frac{2}{R}\left(\frac{S}{1+b}\right) -\frac{d}{dR}\left(\frac{S}{1+b}\right) -l.
\end{equation}

The Markstein length (number) was given as

\begin{equation}
    L_{b} = -\frac{\delta_{ad}I\beta}{2}= -\frac{\delta_{ad}\beta}{2}\int_{\varepsilon}^{1} \frac{1+b}{T^{0}+b}\left[\left(\frac{T^{0}-\varepsilon}{1-\varepsilon}\right)^{\mathrm{Le}-1}-1\right] {\rm d} T^{0}.
\end{equation}

<p style="text-align: justify;">
The extrapolation relation was validated with spherical flame simulation based on recently developed solver for real gas laminar flame.
</p>

<div class="row justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/project_thumbnail/flame_sim_norm.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The variations of flame speed with the Karlovitz number simulated with IG and NA EoS. The fresh mixture was stoichiometric H2-air.
</div>

<a href="javascript:togglebibBlock('ref2')" class="textlink">Related publications</a>
<div id="ref2" class="bibBlock noshow">
<div class="publications" >
  {% bibliography --group_by none --query @*[key=SphericalFlame2024]* %}
</div>
</div>

<a href="javascript:togglebibBlock('ref1')" class="textlink">References</a>
<div id="ref1" class="bibBlock noshow">
<pre>
[1] P.D. Ronney, and G.I. Sivashinsky, “A Theoretical Study of Propagation and Extinction of Nonsteady Spherical Flame Fronts,” SIAM J. Appl. Math. 49(4), 1029–1046 (1989).
</pre>
</div>