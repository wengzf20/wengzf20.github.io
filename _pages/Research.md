---
layout: page
title: Research
permalink: /Research/
description: a collection of research topics
nav: true
nav_order: 2
display_categories: 
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">

<!-- Display projects without categories -->
{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->
  <div class="grid" >
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
</div>
