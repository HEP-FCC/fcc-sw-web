---
layout: site
title: "FCC PS&C related publications and presentations"
id: documents
---

# FCC PS&C related publications and presentations

## Feasibility Study Report

[Future Circular Collider Feasibility Study Report Volume 1: Physics and Experiments](https://cds.cern.ch/record/2928193)
provides an overview of the physics case, experimental programme, and detector
concepts along with the description of the software and computing employed.


## Conceptual Design Report

The [summary volumes](https://fcc-cdr.web.cern.ch/) have been released, with
many physics and detector simulations carried out using the FCC Software. We
collaborated with CERN's [Re-usable Analysis](https://www.reanahub.io/) working
group to make the workflows used in the CDR reproducible and accessible for
future studies. [Here](https://github.com/reanahub/reana-demo-fcchh-fullsim) is
a first example of a full-simulation workflow.


## Publications

{% assign sorted_pubs_talks = site.pubs_talks | sort: 'date' | reverse %}
{% assign publications = sorted_pubs_talks | where: "type", "publication" %}
{% assign total_pubs = publications | size %}

<ul>
{% assign last_year="0000" %}
{% for pub_talk in publications %}
  {% if forloop.index == 21 and total_pubs > 20 %}
</ul>
<div class="collapse" id="more-publications">
<ul>
  {% endif %}
  {% assign pub_year = pub_talk.date | date: '%Y' %}
  {% if pub_year != last_year %}
    {% assign last_year = pub_year %}
    <h2 style="text-indent: -30px;"> {{pub_year}}: </h2>
  {% endif %}
  {% assign extra_mat_end = pub_talk.citation | prepend: "(" | append: ")" %}
  <li> {{ pub_talk.date | date: "%-d %B %Y"}}: <a href="{{pub_talk.link}}">{{pub_talk.name}}</a> {{extra_mat_end}} </li>
{% endfor %}
</ul>
{% if total_pubs > 20 %}
</div>
<a class="btn btn-link ps-0" data-bs-toggle="collapse" href="#more-publications" role="button" aria-expanded="false">
  Show all {{ total_pubs }} publications
</a>
{% endif %}

## Presentations

Besides the contributions included in the Feasibility Study report and
Conceptual Design report, there were numerous software sessions at FCC
conferences and related workshops. The following list is very incomplete, please
submit other contributions to be included here by creating an issue on
[Github](https://github.com/HEP-FCC/FCCSW).

{% assign presentations = sorted_pubs_talks | where_exp: "item", "item.type != 'publication'" %}
{% assign total_pres = 0 %}
{% assign split_after = 0 %}
{% assign running = 0 %}
{% for pub_talk in presentations %}
  {% if pub_talk.type == "event" %}
    {% assign n = pub_talk.sessions | size %}
  {% else %}
    {% assign n = 1 %}
  {% endif %}
  {% assign total_pres = total_pres | plus: n %}
  {% if running < 20 %}{% assign split_after = forloop.index %}{% endif %}
  {% assign running = running | plus: n %}
{% endfor %}
{% assign collapse_from = split_after | plus: 1 %}

<ul>
{% assign last_year="0000" %}
{% for pub_talk in presentations %}
  {% if forloop.index == collapse_from and total_pres > 20 %}
</ul>
<div class="collapse" id="more-presentations">
<ul>
  {% endif %}
  {% assign pub_year = pub_talk.date | date: '%Y' %}
  {% if pub_year != last_year %}
    {% assign last_year = pub_year %}
    <h2 style="text-indent: -30px;"> {{pub_year}}: </h2>
  {% endif %}
  {% assign extra_mat_begin = '' %}
  {% if pub_talk.type == "event" %}
    {% assign extra_mat_begin = "Contributions to the " %}
  {% endif %}
  <li> {{ pub_talk.date | date: "%-d %B %Y"}}: {{extra_mat_begin}} <a href="{{pub_talk.link}}">{{pub_talk.name}}</a> </li>
{% if pub_talk.type == "event" %}
<ul>
{%- for session in pub_talk.sessions -%}
    {%- assign session_author = session.name | split: ": " | first -%}
    {%- assign session_title = session.name | remove_first: session_author | remove_first: ": " -%}
    <li> {{session_author}}: <a href="{{session.link}}">{{session_title}}</a> </li>
{%- endfor -%}
</ul>
{% endif %}
{% endfor %}
</ul>
{% if total_pres > 20 %}
</div>
<a class="btn btn-link ps-0" data-bs-toggle="collapse" href="#more-presentations" role="button" aria-expanded="false">
  Show all {{ total_pres }} presentations
</a>
{% endif %}
