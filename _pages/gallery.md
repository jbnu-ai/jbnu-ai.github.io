---
layout: default
title: Gallery
permalink: /gallery/
---

<div class="page-header">
  <div class="container">
    <h1>Gallery</h1>
    <p class="lead">연구실 활동 사진</p>
  </div>
</div>

<div class="container py-5">

  <!-- Category Tabs -->
  <ul class="nav nav-tabs mb-4" id="galleryTab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="all-tab" data-bs-toggle="tab" data-bs-target="#all"
              type="button" role="tab">All</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="lab-tab" data-bs-toggle="tab" data-bs-target="#lab"
              type="button" role="tab">Lab Life</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="conf-tab" data-bs-toggle="tab" data-bs-target="#conf"
              type="button" role="tab">Conferences</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="award-tab" data-bs-toggle="tab" data-bs-target="#award"
              type="button" role="tab">Awards</button>
    </li>
  </ul>

  <div class="tab-content" id="galleryTabContent">
    <div class="tab-pane fade show active" id="all" role="tabpanel">
      <div class="gallery-grid">
        <!-- Placeholder gallery items -->
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>2024 연말 연구실 모임</p>
          </div>
        </div>
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>CVPR 2024 발표</p>
          </div>
        </div>
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>우수논문상 수상</p>
          </div>
        </div>
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>2024 세미나</p>
          </div>
        </div>
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>MT 활동</p>
          </div>
        </div>
        <div class="gallery-item">
          <div class="gallery-placeholder">
            <i class="fas fa-image fa-3x"></i>
            <p>ICCV 2023 발표</p>
          </div>
        </div>
      </div>
    </div>
    <div class="tab-pane fade" id="lab" role="tabpanel">
      <p class="text-muted text-center py-5">Lab life photos coming soon.</p>
    </div>
    <div class="tab-pane fade" id="conf" role="tabpanel">
      <p class="text-muted text-center py-5">Conference photos coming soon.</p>
    </div>
    <div class="tab-pane fade" id="award" role="tabpanel">
      <p class="text-muted text-center py-5">Award photos coming soon.</p>
    </div>
  </div>

  <div class="text-center mt-4 text-muted">
    <p>사진을 추가하려면 <code>assets/images/gallery/</code> 폴더에 이미지를 추가하고 <code>_data/gallery.yml</code>을 편집하세요.</p>
  </div>

</div>
