---
title: FCC Software and Computing
layout: main
---

The FCC Physics Software and Computing provides a set of software packages, tools, and standards to
enable different FCC physics efforts work together. The software ecosystem of the FCC
fully employs [Key4hep](https://key4hep.github.io/key4hep-doc/)
stack and is one of its main stakeholders.



<div class="container">
  <div class="row g-4 justify-content-start" style="max-width: 85%; margin: 0 auto;">
    <div class="col-sm-6">
      <a href="{{ '/getting_started' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card" style="border-top: 4px solid #198754;">
          <div class="card-body d-flex flex-column align-items-center justify-content-start py-4">
            <img src="assets/img/getting-started.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Getting Started</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/documents' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card" style="border-top: 4px solid #6f42c1;">
          <div class="card-body d-flex flex-column align-items-center justify-content-start py-4">
            <img src="assets/img/presentations.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Publications and Presentations</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/software' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card" style="border-top: 4px solid #0d6efd;">
          <div class="card-body d-flex flex-column align-items-center justify-content-start py-4">
            <img src="assets/img/coding.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">Software</h4>
          </div>
        </div>
      </a>
    </div>
    <div class="col-sm-6">
      <a href="{{ '/analysis.html' | relative_url }}" class="text-decoration-none">
        <div class="card h-100 text-center fcc-nav-card" style="border-top: 4px solid #dc3545;">
          <div class="card-body d-flex flex-column align-items-center justify-content-start py-4">
            <img src="assets/img/data-analysis.png" width="100px" class="mb-3">
            <h4 class="card-title mb-0">FCC Analysis</h4>
          </div>
        </div>
      </a>
    </div>
  </div>
</div>
<br>

<div style="border-top: 4px solid #0d6efd; margin-top: 2rem; margin-bottom: 0.75rem;"></div>
<center><h3 class="mb-3">Current organization</h3></center>

<div class="container-fluid px-0">
  <div class="row g-2 psc-org-grid">
    {% for group in site.data.psc_groups %}
      {% if group.split %}
        {% assign sub0 = group.sub[0] %}
        {% assign sub1 = group.sub[1] %}
        <div class="col-md-4 col-sm-6">
          <div class="card h-100 psc-group-card text-center" style="border-top: 3px solid; border-image: linear-gradient(to right, {{ sub0.color }} 50%, {{ sub1.color }} 50%) 1;">
            <div class="card-body d-flex flex-row justify-content-start py-2 px-0">
              <div class="d-flex flex-column align-items-center justify-content-start py-0 px-2 w-50">
                <div class="fw-semibold small">
                  {% if group.local_link %}<a href="{{ group.local_link | relative_url }}" class="text-decoration-none text-body">{{ sub0.subtitle }}</a>{% else %}{{ sub0.subtitle }}{% endif %}
                </div>
                {% if sub0.gms_link %}<a href="{{ sub0.gms_link }}" class="small mt-1" target="_blank">Mailing list</a>{% endif %}
              </div>
              <div style="width: 3px; background-color: var(--bs-border-color); align-self: stretch;"></div>
              <div class="d-flex flex-column align-items-center justify-content-start py-0 px-2 w-50">
                <div class="fw-semibold small">{{ sub1.subtitle }}</div>
                {% if sub1.gms_link %}<a href="{{ sub1.gms_link }}" class="small mt-1" target="_blank">Mailing list</a>{% endif %}
                {% if sub1.shared_with_physics %}<div><span class="badge text-bg-secondary mt-1" style="font-size:0.6em; font-weight:normal;">Shared with Physics</span></div>{% endif %}
              </div>
            </div>
          </div>
        </div>
      {% else %}
        <div class="col-md-4 col-sm-6">
          <div class="card h-100 psc-group-card text-center" {% if group.color %}style="border-top: 3px solid {{ group.color }};"{% endif %}>
            <div class="card-body d-flex flex-column align-items-center justify-content-start py-2">
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
              {% if group.shared_with_physics %}<div><span class="badge text-bg-secondary mt-1" style="font-size:0.6em; font-weight:normal;">Shared with Physics</span></div>{% endif %}
            </div>
          </div>
        </div>
      {% endif %}
    {% endfor %}
  </div>
</div>


