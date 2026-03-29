---
layout: default
title: News
permalink: /news/
---

<div class="page-header">
  <div class="container">
    <h1>News</h1>
    <p class="lead">연구센터 소식 및 공지</p>
  </div>
</div>

<div class="container py-5">

  <div class="news-filter mb-4">
    <div class="btn-group flex-wrap" role="group">
      <button type="button" class="btn btn-outline-primary active news-filter-btn" data-category="all">All</button>
      <button type="button" class="btn btn-outline-primary news-filter-btn" data-category="paper">Paper</button>
      <button type="button" class="btn btn-outline-primary news-filter-btn" data-category="award">Award</button>
      <button type="button" class="btn btn-outline-primary news-filter-btn" data-category="announcement">Notice</button>
      <button type="button" class="btn btn-outline-primary news-filter-btn" data-category="event">Event</button>
    </div>
  </div>

  <div class="news-page-list">
    {% assign sorted_news = site.data.news | sort: "date" | reverse %}
    {% for item in sorted_news %}
    <article class="news-card" id="news-{{ item.date | date: '%Y%m%d' }}" data-category="{{ item.category }}">
      <div class="news-card-header">
        <div class="d-flex align-items-center gap-2 flex-wrap">
          <span class="news-category-badge cat-{{ item.category }}">
            {% case item.category %}
              {% when 'event' %}Event
              {% when 'paper' %}Paper
              {% when 'award' %}Award
              {% when 'announcement' %}Notice
              {% else %}{{ item.category }}
            {% endcase %}
          </span>
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
      <div class="news-card-body collapse" id="news-body-{{ forloop.index }}">
        <div class="news-body-content">
          {{ item.content | markdownify }}
        </div>
      </div>
      <button class="btn btn-sm btn-link news-toggle-btn ps-0"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#news-body-{{ forloop.index }}"
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
  </div>

</div>

<script>
// 앵커로 직접 접근 시 해당 뉴스 자동 펼침 + 하이라이트
const hash = window.location.hash;
if (hash) {
  const target = document.querySelector(hash);
  if (target) {
    const collapseEl = target.querySelector('.news-card-body');
    const toggleBtn = target.querySelector('.news-toggle-btn');
    if (collapseEl && toggleBtn) {
      new bootstrap.Collapse(collapseEl, { show: true });
      toggleBtn.querySelector('.toggle-text-more').classList.add('d-none');
      toggleBtn.querySelector('.toggle-text-less').classList.remove('d-none');
    }
    target.classList.add('news-highlight');
    setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 150);
  }
}

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

document.querySelectorAll('.news-filter-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.news-filter-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const cat = this.getAttribute('data-category');
    document.querySelectorAll('.news-card').forEach(card => {
      if (cat === 'all' || card.getAttribute('data-category') === cat) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
});
</script>
