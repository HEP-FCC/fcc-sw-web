---
layout: site
id: documents
---

# Documents

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


## Past Publications and Presentations

Besides the contributions included in the Feasibility Study report and
Conceptual Design report, there were numerous software sessions at FCC
conferences and related workshops. The following list is very incomplete, please
submit other contributions to be included here by creating an issue on
[Github](https://github.com/HEP-FCC/FCCSW).

{% assign sorted_pubs_talks = site.pubs_talks | sort: 'date' | reverse %}

<ul>
{% assign last_year="0000" %}
{% for pub_talk in sorted_pubs_talks %}
  {% assign extra_mat_end = '' %}
  {% assign extra_mat_begin = '' %}
  {% assign pub_year = pub_talk.date | date: '%Y' %}
  {% if pub_year != last_year %}
    {% assign last_year = pub_year %}
    <h2 style="text-indent: -30px;"> {{pub_year}}: </h2>
  {% endif %}
  {% if pub_talk.type == "publication" %}
    {% assign extra_mat_end = pub_talk.citation | prepend: "(" | append: ")" %}
  {% endif %}
  {% if pub_talk.type == "event" %}
  {% assign extra_mat_begin = "Contributions to the " %}
  {% endif %}

  <li> {{ pub_talk.date  | date: "%-d %B %Y"}}: {{extra_mat_begin}} <a href="{{pub_talk.link}}">{{pub_talk.name}}</a> {{extra_mat_end}} </li>
{% if pub_talk.type == "event" %}
<ul>
{%- for session in pub_talk.sessions -%}
    <li> <a href="{{session.link}}">{{session.name}}</a> </li>
{%- endfor -%}
</ul>
{% endif %}
{% endfor %}
</ul>
