# 영상정보신기술연구센터 홈페이지

전북대학교 영상정보신기술연구센터 공식 웹사이트 소스 저장소입니다.

**사이트 주소:** https://jbnu-ai.github.io

---

## 기술 스택

| 기술 | 용도 |
|------|------|
| [Jekyll 4.4](https://jekyllrb.com/) | 정적 사이트 생성기 |
| [jekyll-scholar](https://github.com/inukshuk/jekyll-scholar) | BibTeX 기반 논문 목록 자동 생성 |
| [Bootstrap 5](https://getbootstrap.com/) | 반응형 UI 프레임워크 |
| [GitHub Actions](https://github.com/features/actions) | 자동 빌드 및 배포 |

---

## 파일 구조

```
jbnu-ai.github.io/
├── _bibliography/
│   └── papers.bib           # 논문 BibTeX 목록
├── _data/
│   ├── members.yml          # 교수진 및 구성원 정보
│   └── news.yml             # 뉴스 및 이벤트 목록
├── _includes/
│   ├── header.html          # 상단 네비게이션
│   └── footer.html          # 하단 푸터
├── _layouts/
│   ├── default.html         # 기본 레이아웃
│   └── bib.html             # 논문 항목 렌더링 템플릿
├── _pages/
│   ├── about.md             # 센터 소개
│   ├── people.md            # 구성원 (/about/people/)
│   ├── research.md          # 연구 분야 (/research/)
│   ├── publications.md      # 논문 목록 (/research/publications/)
│   ├── news.md              # 뉴스 & 이벤트 (/news/)
│   ├── gallery.md           # 갤러리 (/gallery/)
│   └── contact.md           # 연락처 (/contact/)
├── assets/
│   ├── css/main.css         # 스타일시트
│   ├── js/main.js           # JavaScript
│   └── images/people/       # 구성원 사진
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions 배포 워크플로우
├── _config.yml              # Jekyll 설정
├── Gemfile                  # Ruby gem 의존성
├── index.html               # 메인 홈페이지
├── README.md                # 이 파일
└── INSTALL.md               # 로컬 개발 환경 설정 가이드
```

---

## 콘텐츠 편집 가이드

### 구성원 추가/수정

`_data/members.yml` 파일을 편집합니다. 섹션은 `professors`, `associate_professors`, `assistant_professors`, `graduate_students`로 구분됩니다.

```yaml
assistant_professors:
  - name: "홍길동"
    name_en: "Gildong Hong"
    title: "조교수"
    title_en: "Assistant Professor"
    email: "gdhong@jbnu.ac.kr"
    phone: "063-270-0000"
    office: "7호관 000"
    research_interests:
      - Deep Learning
      - Computer Vision
    links:
      homepage: "https://example.com"
      scholar_id: "XXXXXXXXX"   # Google Scholar 프로필 ID
```

### 논문 추가

`_bibliography/papers.bib` 파일에 BibTeX 형식으로 추가합니다.

```bibtex
@article{hong2025title,
  abbr        = {IEEE TIP},
  title       = {논문 제목},
  author      = {Hong, Gildong and Kim, Cheolsu},
  journal     = {IEEE Transactions on Image Processing},
  year        = {2025},
  selected    = {true},   % 메인 페이지 Selected Publications에 표시
  pdf         = {https://arxiv.org/abs/...},
  html        = {https://doi.org/...},
}
```

- `selected = {true}` 항목은 메인 페이지 **Selected Publications** 섹션(2025년 이후)에 자동 표시됩니다.
- `abbr` 필드: 학술대회/저널 약어 배지 표시 (journal은 파란색, conference는 초록색)

### 뉴스 추가

`_data/news.yml` 파일에 항목을 추가합니다.

```yaml
- date: "2025-03-01"
  category: paper        # paper / award / announcement / event
  title: "뉴스 제목"
  summary: "한 줄 요약"
  content: |
    상세 내용 (Markdown 사용 가능)
  link: "https://..."    # 외부 링크 (선택)
```

---

## 로컬 개발 환경 설정

자세한 내용은 [INSTALL.md](INSTALL.md)를 참고하세요.

```bash
# 빠른 시작 (rbenv + Ruby 3.2 설치 완료 후)
bundle install
bundle exec jekyll serve --livereload
```

---

## 배포

`main` 브랜치에 push하면 GitHub Actions가 자동으로 빌드 및 배포합니다.

```bash
git add .
git commit -m "커밋 메시지"
git push origin main
```

자세한 배포 절차는 [INSTALL.md](INSTALL.md#github-pages-배포)를 참고하세요.
