---
layout: default
title: Blog
permalink: /Blog/
nav: true
nav_order: 5
description: A collection of research notes
---
<div class="blog-index">
  <header class="blog-heading"><h1>a collection of research notes</h1></header>
  <nav class="blog-topics" aria-label="Browse posts by topic">
    {% assign tags = site.tags | sort %}
    {% for tag in tags %}<a href="{{ tag[0] | slugify | prepend: '/blog/tag/' | append: '/' | relative_url }}"><span aria-hidden="true">#</span> {{ tag[0] }}</a>{% endfor %}
    {% assign categories = site.categories | sort %}
    {% for category in categories %}<a href="{{ category[0] | slugify | prepend: '/blog/category/' | append: '/' | relative_url }}"><span aria-hidden="true">◆</span> {{ category[0] }}</a>{% endfor %}
  </nav>
  {% include blog-list.liquid posts=site.posts %}
</div>
