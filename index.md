---
layout: landingpage
title: Sports Analytics Group @ BU
header_type: splash
header_img: "https://www.bu.edu/files/2025/04/frozen-four-feat.jpg"
subtitle: Est. 2024
---

<!-- Click [**Use this template**](https://github.com/dieghernan/chulapa-101/generate) button above for cloning this repo and get started with [Chulapa Jekyll theme](https://github.com/dieghernan/chulapa).

Contains basic configuration to get you a site with:

- Sample posts and [paginated blog index](./blog/).
- Sample collection with Markdown and kramdown cheatsheets and [collection index](./cheatsheets).
- Archive pages for posts grouped by year, category, and tag.
- Github Action for deploying the site.
- Demo page with the different Bootstrap components and how they look with the actual skin settings.
- Sample 404 page.
- Site search with Lunr.
- Sample `_config` with minimal configuration. `primary` color is set to <span class="text-primary">LightSkyBlue</span> and `autothemer` is enabled. [Learn how to customize your site](https://dieghernan.github.io/chulapa/docs/03-theming).
- Sample `algolia-search.yml` for using Algolia+GitHub Actions.
- Sample files for extending the theme with your own scripts and css.

On addition, `jekyll-sitemap` generates your sitemap on [./sitemap.xml](./sitemap.xml), and Chulapa generates an Atom feed on [./atom.xml](./atom.xml) and a RSS 2.0 feed on [./rss.xml](./rss.xml).

[Configure as necessary](https://dieghernan.github.io/chulapa/docs/02-config) and replace sample content with your own. -->


<main class="container-lg py-5">

  <!-- Latest Articles Section -->
  <div class="row text-center mb-5">
    <div class="col-12">
      <h2 class="display-4">Latest Articles</h2>
    </div>
  </div>
  <div class="row justify-content-center">
    <div class="col-12">
      {%- include_cached components/indexcards.html cacheddocs=site.posts cachedlimit=3 -%}
    </div>
  </div>
  <div class="row text-center mt-4">
    <div class="col-12">
      <a href="/blog/" class="btn btn-lg" style="background-color: #cc0000; color: white;">View All Articles</a>
    </div>
  </div>

  <!-- Divider -->
  <hr class="my-5" style="border-top: 1px solid #444;">

  <!-- Upcoming Events Section -->
  <div class="row text-center mb-5">
    <div class="col-12">
      <h2 class="display-4">Upcoming Events</h2>
    </div>
  </div>
  <div class="row g-4 justify-content-center">
    <!-- Splash Event Card -->
    <div class="col-md-6 col-lg-4">
      <div class="card text-white bg-dark h-100">
        <img src="https://www.bu.edu/files/2022/09/thumbnail-1.jpg" class="card-img-top" alt="BU Splash Event" style="object-fit: cover; width: 100%; height: 300px; border-bottom: 1px solid #444;">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title mb-1">Splash</h5>
          <h6 class="card-subtitle mb-2 text-muted" style="color: #bbb !important;">September 6th</h6>
          <p class="card-text mb-3">Meet us at Splash!</p>
        </div>
      </div>
    </div>
  </div>
  <div class="row text-center mt-4">
    <div class="col-12">
      <a href="/events/" class="btn btn-lg" style="background-color: #cc0000; color: white;">View All Events</a>
    </div>
  </div>

</main>