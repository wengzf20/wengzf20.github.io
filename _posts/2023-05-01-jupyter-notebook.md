---
layout: post
title: Prepare figures for journal articles 
date: 2023-05-01 00:00:00-0000
description: an summary of codes for preparing figures based on python
tags: artworks
categories: Code 
giscus_comments: false
related_posts: false
thumbnail: assets/img/photo/IMG_2537.jpg
viewercount: true
---

{::nomarkdown}
{% assign jupyter_path = 'assets/jupyter/plotFig.ipynb' | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/plotFig.ipynb %}{% endcapture %}
{% if notebook_exists == 'true' %}
  {% jupyter_notebook jupyter_path %}
{% else %}
  <p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}