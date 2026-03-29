# 로컬 개발 환경 설정 및 배포 가이드

운영체제에 맞는 섹션을 참고하세요.

- [macOS](#macos)
- [Windows](#windows)
- [공통: 프로젝트 설치 및 실행](#공통-프로젝트-설치-및-실행)
- [GitHub Pages 배포](#github-pages-배포)
- [문제 해결](#문제-해결)

---

## macOS

### 사전 요구사항

- macOS (Apple Silicon / Intel)
- [Homebrew](https://brew.sh/) 패키지 매니저
- Git

### 1단계: Ruby 설치 (rbenv 사용)

macOS 기본 Ruby(2.6)는 시스템 전용이라 gem 설치가 제한됩니다.
rbenv로 독립된 Ruby 환경을 구성합니다.

```bash
# rbenv 및 ruby-build 설치
brew install rbenv ruby-build

# Shell 초기화 설정 추가 (zsh 기준)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Ruby 3.2.3 설치 (수 분 소요)
rbenv install 3.2.3
rbenv global 3.2.3

# 설치 확인
ruby --version
# ruby 3.2.3 (2024-01-18 revision ...) [arm64-darwin] 출력되면 성공
```

---

## Windows

### 사전 요구사항

- Windows 10 / 11 (64-bit)
- Git for Windows ([git-scm.com](https://git-scm.com/download/win))

### 방법 A: RubyInstaller 사용 (권장)

Jekyll 공식 권장 방식입니다.

**1. RubyInstaller 다운로드 및 설치**

[rubyinstaller.org/downloads](https://rubyinstaller.org/downloads/) 에서
**Ruby+Devkit 3.2.x (x64)** 를 다운로드합니다.

설치 마지막 단계에서 **"Run 'ridk install'"** 체크박스를 유지한 채 Finish를 클릭합니다.
터미널 창이 열리면 `1` (MSYS2 base) 또는 `3` (MSYS2 and MINGW)을 입력하고 Enter합니다.

**2. 설치 확인**

```cmd
ruby --version
gem --version
```

**3. Bundler 설치**

```cmd
gem install bundler
```

### 방법 B: WSL2 사용 (Linux 환경 선호 시)

WSL2(Ubuntu)를 이용하면 macOS와 동일한 명령어를 사용할 수 있습니다.

```powershell
# PowerShell (관리자 권한)
wsl --install
# 재시작 후 Ubuntu 터미널 실행
```

Ubuntu 터미널에서:

```bash
# 의존성 설치
sudo apt update && sudo apt install -y rbenv ruby-build git curl

# Shell 초기화
echo 'eval "$(rbenv init - bash)"' >> ~/.bashrc
source ~/.bashrc

# Ruby 3.2.3 설치
rbenv install 3.2.3
rbenv global 3.2.3

# 설치 확인
ruby --version
gem install bundler
```

> WSL2 내에서 프로젝트를 클론하면 파일 시스템 성능이 더 좋습니다.
> Windows 탐색기에서 `\\wsl$\Ubuntu\home\<사용자명>` 경로로 파일에 접근할 수 있습니다.

---

## 공통: 프로젝트 설치 및 실행

운영체제 무관하게 아래 단계를 따릅니다.

### 저장소 클론

```bash
git clone https://github.com/jbnu-ai/jbnu-ai.github.io.git
cd jbnu-ai.github.io
```

### 의존성 설치

```bash
bundle install
```

설치되는 주요 gem:

| gem | 설명 |
|-----|------|
| `jekyll 4.4` | 정적 사이트 생성기 |
| `jekyll-scholar 7.x` | BibTeX 논문 목록 자동 생성 |
| `jekyll-feed` | RSS 피드 생성 |
| `jekyll-seo-tag` | SEO 메타태그 |
| `jekyll-sitemap` | sitemap.xml 자동 생성 |

### 로컬 서버 실행

```bash
bundle exec jekyll serve --livereload
```

브라우저에서 **http://localhost:4000** 접속

유용한 옵션:

| 옵션 | 설명 |
|------|------|
| `--livereload` | 파일 수정 시 브라우저 자동 새로고침 |
| `--drafts` | `_drafts/` 임시 글 포함 미리보기 |
| `--incremental` | 변경된 파일만 재빌드 (빠름) |
| `--port 4001` | 포트 변경 (기본 4000이 사용 중일 때) |

서버 종료: `Ctrl + C`

### 빌드 확인

배포 전 로컬에서 빌드 결과를 확인합니다.

```bash
bundle exec jekyll build
```

결과물은 `_site/` 폴더에 생성됩니다. (`_site/`는 `.gitignore`에 포함되어 있으며 커밋하지 않습니다.)

### 자주 쓰는 명령어

| 명령어 | 설명 |
|--------|------|
| `bundle exec jekyll serve --livereload` | 로컬 서버 실행 + 자동 새로고침 |
| `bundle exec jekyll build` | 정적 파일 빌드 |
| `bundle exec jekyll clean` | `_site/`, 캐시 삭제 |
| `bundle update` | gem 최신 버전으로 업데이트 |

---

## GitHub Pages 배포

### 최초 1회 설정

GitHub 저장소 → **Settings** → **Pages** → Source를 **GitHub Actions**로 변경합니다.

### 배포 방법

`main` 브랜치에 push하면 `.github/workflows/deploy.yml`의 GitHub Actions가 자동으로 빌드 및 배포합니다.

```bash
git add .
git commit -m "커밋 메시지"
git push origin main
```

### 배포 흐름

```
git push origin main
       │
       ▼
GitHub Actions (ubuntu-latest)
  1. actions/checkout@v4               — 소스 체크아웃
  2. ruby/setup-ruby@v1 (3.2)          — Ruby + bundle 캐시
  3. actions/configure-pages@v4        — Pages baseurl 설정
  4. bundle exec jekyll build          — 정적 사이트 빌드
  5. actions/upload-pages-artifact@v3  — 빌드 결과 업로드
  6. actions/deploy-pages@v4           — GitHub Pages 배포
       │
       ▼
https://jbnu-ai.github.io  (보통 1~2분 이내)
```

### 배포 상태 확인

GitHub 저장소 → **Actions** 탭에서 워크플로우 실행 상태를 확인할 수 있습니다.
빌드 실패 시 로그에서 에러 내용을 확인하고 로컬에서 `bundle exec jekyll build`로 재현합니다.

### 수동 배포 트리거

push 없이 즉시 배포하려면 Actions 탭 → **Build and Deploy Jekyll Site** → **Run workflow** 버튼을 클릭합니다.

---

## 문제 해결

### [macOS] rbenv 환경이 적용되지 않는 경우

새 터미널을 열거나:

```bash
eval "$(rbenv init - zsh)"
```

### [Windows] `ridk install` 이후에도 gem 설치가 안 되는 경우

명령 프롬프트(cmd) 또는 PowerShell을 **관리자 권한**으로 실행한 뒤 다시 시도합니다.

```cmd
ridk install
gem install bundler
```

### [Windows] `bundle install` 중 `Encoding::UndefinedConversionError`

콘솔 인코딩을 UTF-8로 변경합니다:

```cmd
chcp 65001
bundle install
```

### `cannot load such file` 에러

```bash
bundle install  # gem 재설치
```

### 포트 충돌 (`Address already in use`)

```bash
bundle exec jekyll serve --port 4001
```

### BibTeX 파싱 에러

`_bibliography/papers.bib` 파일 첫 두 줄에 Jekyll Front Matter 헤더가 있어야 합니다:

```
---
---
@article{...}
```

### GitHub Actions 빌드 실패

로컬에서 동일 명령으로 재현합니다:

```bash
bundle exec jekyll build
```

에러 메시지를 확인하고 `_bibliography/papers.bib` BibTeX 문법, `_data/` YAML 들여쓰기 등을 점검합니다.
