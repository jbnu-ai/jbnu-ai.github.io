---
layout: default
title: Events
permalink: /events/
---

<div class="page-header">
  <div class="container">
    <h1>Events</h1>
    <p class="lead">세미나, 튜토리얼, 워크숍 일정</p>
  </div>
</div>

<div class="container py-5">

  <div class="news-page-list">
    {% assign sorted_events = site.data.news | where: "category", "event" | sort: "date" | reverse %}
    {% if sorted_events.size == 0 %}
    <p class="text-muted">등록된 이벤트가 없습니다.</p>
    {% else %}
    {% for item in sorted_events %}
    <article class="news-card" id="event-{{ item.date | date: '%Y%m%d' }}">
      <div class="news-card-header">
        <div class="d-flex align-items-center gap-2 flex-wrap">
          <span class="news-category-badge cat-event">Event</span>
          <span class="news-card-date">{{ item.date | date: "%Y.%m.%d" }}</span>
          {% if item.author %}
          <span class="text-muted small">— {{ item.author }}</span>
          {% endif %}
        </div>
        <h3 class="news-card-title mt-2 mb-0">{{ item.title }}</h3>
      </div>

      {% if item.summary %}
      <p class="news-card-summary">{{ item.summary }}</p>
      {% endif %}

      {% if item.content %}
      <div class="news-card-body collapse" id="event-body-{{ forloop.index }}">
        <div class="news-body-content">
          {{ item.content | markdownify }}
        </div>
      </div>
      <button class="btn btn-sm btn-link news-toggle-btn ps-0"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#event-body-{{ forloop.index }}"
              aria-expanded="false">
        <span class="toggle-text-more">자세히 보기 <i class="fas fa-chevron-down"></i></span>
        <span class="toggle-text-less d-none">접기 <i class="fas fa-chevron-up"></i></span>
      </button>
      {% endif %}

      {% if item.link %}
      <a href="{{ item.link }}" target="_blank" class="btn btn-sm btn-outline-primary mt-1">
        <i class="fas fa-external-link-alt me-1"></i>원문 보기
      </a>
      {% endif %}
    </article>
    {% endfor %}
    {% endif %}
  </div>

</div>

<script>
document.querySelectorAll('.news-toggle-btn').forEach(btn => {
  const target = document.querySelector(btn.getAttribute('data-bs-target'));
  if (!target) return;
  target.addEventListener('show.bs.collapse', () => {
    btn.querySelector('.toggle-text-more').classList.add('d-none');
    btn.querySelector('.toggle-text-less').classList.remove('d-none');
  });
  target.addEventListener('hide.bs.collapse', () => {
    btn.querySelector('.toggle-text-more').classList.remove('d-none');
    btn.querySelector('.toggle-text-less').classList.add('d-none');
  });
});
</script>
