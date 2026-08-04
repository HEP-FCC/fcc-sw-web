---
title: FCC Software and Computing
layout: main
---

The FCC Physics Software and Computing provides a set of software packages, tools, and standards to
enable different FCC physics efforts work together. The software ecosystem of the FCC
fully employs [Key4hep](https://key4hep.github.io/key4hep-doc/)
stack and is one of its main stakeholders.



<div class="container">
  <div class="row g-4">
    <div class="col-sm-6">
      <a href="{{ '/getting_started' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card">
          <div class="card-body d-flex flex-column align-items-center justify-content-center py-4">
            <img src="assets/img/getting-started.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Getting Started</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/documents' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card">
          <div class="card-body d-flex flex-column align-items-center justify-content-center py-4">
            <img src="assets/img/presentations.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Publications and Presentations</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/software' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card">
          <div class="card-body d-flex flex-column align-items-center justify-content-center py-4">
            <img src="assets/img/coding.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Software</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/computing' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card">
          <div class="card-body d-flex flex-column align-items-center justify-content-center py-4">
            <img src="assets/img/data-analysis.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Analysis and Computing</h4>
          </div>
        </div>
      </a>
    </div>
  </div>
</div>
<br>

<center><h3>Current organization</h3></center>

<div class="container-fluid px-0">
  <div class="row g-2">
    {% for group in site.data.psc_groups %}
      {% if group.split %}
        <div class="col-md-4 col-sm-6">
          <div class="row g-2 h-100">
            {% for sub in group.sub %}
            <div class="col-6 d-flex">
              <div class="card w-100 psc-group-card text-center">
                <div class="card-body d-flex flex-column align-items-center justify-content-center py-2 px-1">
                  <div class="fw-semibold small">{{ sub.subtitle }}</div>
                  {% if sub.gms_link %}
                  <a href="{{ sub.gms_link }}" class="small mt-1" target="_blank">Mailing list</a>
                  {% endif %}
                </div>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
      {% else %}
        <div class="col-md-4 col-sm-6">
          <div class="card h-100 psc-group-card text-center">
            <div class="card-body d-flex flex-column align-items-center justify-content-center py-2">
              <div class="fw-semibold small">
                {% if group.local_link %}
                  <a href="{{ group.local_link | relative_url }}" class="text-decoration-none text-body">{{ group.title }}</a>
                {% else %}
                  {{ group.title }}
                {% endif %}
              </div>
              {% if group.gms_link %}
              <a href="{{ group.gms_link }}" class="small mt-1" target="_blank">Mailing list</a>
              {% endif %}
            </div>
          </div>
        </div>
      {% endif %}
    {% endfor %}
  </div>
</div>


