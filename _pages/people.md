---
layout: default
title: People
permalink: /about/people/
---

<div class="page-header">
  <div class="container">
    <h1>People</h1>
    <p class="lead">연구센터 교수진 및 구성원</p>
  </div>
</div>

<div class="container py-5">

  {% assign all_faculty = site.data.members.professors
    | concat: site.data.members.associate_professors
    | concat: site.data.members.assistant_professors
    | sort: "name" %}

  <h2 class="section-title mb-4">Faculty</h2>
  <div class="faculty-table-wrap mb-5">
    <table class="table faculty-table">
      <thead>
        <tr>
          <th style="width:150px">Name</th>
          <th>Research Areas</th>
          <th style="width:200px">Email</th>
          <th style="width:60px">Homepage</th>
        </tr>
      </thead>
      <tbody>
        {% for member in all_faculty %}
        <tr>
          <td>
            {% if member.links.homepage and member.links.homepage != "" %}
              <a href="{{ member.links.homepage }}" target="_blank" class="faculty-name">{{ member.name }}</a>
            {% else %}
              <span class="faculty-name">{{ member.name }}</span>
            {% endif %}
            <br/><span class="text-muted small">{{ member.name_en }}</span>
          </td>
          <td>
            {% for interest in member.research_interests %}
            <span class="interest-tag">{{ interest }}</span>
            {% endfor %}
          </td>
          <td class="small font-monospace" style="white-space: nowrap;">
            {% if member.email %}
              {{ member.email | replace: "@", " (at) " | replace: ".", "." }}
            {% endif %}
          </td>
          <td class="text-center">
            {% if member.links.homepage and member.links.homepage != "" %}
            <a href="{{ member.links.homepage }}" target="_blank" class="icon-link" title="Homepage">
              <i class="fas fa-external-link-alt"></i>
            </a>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  {% if site.data.members.graduate_students and site.data.members.graduate_students.size > 0 %}
  <h2 class="section-title mb-4">Graduate Students</h2>
  <div class="faculty-table-wrap mb-5">
    <table class="table faculty-table">
      <thead>
        <tr>
          <th style="width:150px">Name</th>
          <th>Research Areas</th>
          <th style="width:200px">Email</th>
          <th style="width:60px">Links</th>
        </tr>
      </thead>
      <tbody>
        {% assign sorted_students = site.data.members.graduate_students | sort: "name" %}
        {% for member in sorted_students %}
        <tr>
          <td>
            {% if member.links.homepage and member.links.homepage != "" %}
              <a href="{{ member.links.homepage }}" target="_blank" class="faculty-name">{{ member.name }}</a>
            {% else %}
              <span class="faculty-name">{{ member.name }}</span>
            {% endif %}
            <br/><span class="text-muted small">{{ member.name_en }}</span>
          </td>
          <td>
            {% for interest in member.research_interests %}
            <span class="interest-tag">{{ interest }}</span>
            {% endfor %}
          </td>
          <td class="small font-monospace" style="white-space: nowrap;">
            {% if member.email %}
              {{ member.email | replace: "@", " (at) " | replace: ".", "." }}
            {% endif %}
          </td>
          <td class="text-center">
            {% if member.links.github and member.links.github != "" %}
            <a href="{{ member.links.github }}" target="_blank" class="icon-link" title="GitHub">
              <i class="fab fa-github"></i>
            </a>
            {% endif %}
            {% if member.links.google_scholar and member.links.google_scholar != "" %}
            <a href="{{ member.links.google_scholar }}" target="_blank" class="icon-link" title="Google Scholar">
              <i class="fas fa-graduation-cap"></i>
            </a>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}

</div>
