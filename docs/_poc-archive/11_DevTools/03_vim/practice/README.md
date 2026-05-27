# Vim 핵심 명령어 빠른 참조

Vim 학습 프로젝트의 실습 파일 모음입니다.

---

## 모드 전환

```vim
i       " 커서 앞에서 Insert 모드
I       " 줄 시작에서 Insert 모드
a       " 커서 뒤에서 Insert 모드
A       " 줄 끝에서 Insert 모드
o       " 아래 새 줄에서 Insert 모드
O       " 위에 새 줄에서 Insert 모드
v       " Visual 모드 (문자 단위)
V       " Visual Line 모드 (줄 단위)
Ctrl+V  " Visual Block 모드 (블록 단위)
:       " Command 모드
Esc     " Normal 모드로 복귀
```

---

## 이동

### 기본 이동
```vim
h       " 왼쪽
j       " 아래
k       " 위
l       " 오른쪽
```

### 단어 이동
```vim
w       " 다음 단어 시작
b       " 이전 단어 시작
e       " 단어 끝
W/B/E   " 공백 기준 단어 이동
```

### 줄 이동
```vim
0       " 줄 시작 (공백 포함)
^       " 줄 첫 문자 (공백 제외)
$       " 줄 끝
```

### 파일 이동
```vim
gg      " 파일 처음
G       " 파일 끝
{n}G    " n번 줄로 이동
H       " 화면 상단
M       " 화면 중간
L       " 화면 하단
```

### 문자 점프
```vim
f{char} " 다음 {char}로 이동
t{char} " 다음 {char} 직전으로 이동
F{char} " 이전 {char}로 이동
T{char} " 이전 {char} 직후로 이동
;       " 마지막 f/t 반복
,       " 마지막 f/t 역방향 반복
```

### 화면 이동
```vim
Ctrl+D  " 반 페이지 아래
Ctrl+U  " 반 페이지 위
Ctrl+F  " 페이지 아래
Ctrl+B  " 페이지 위
zz      " 현재 줄을 화면 중앙으로
```

---

## 편집

### 삭제
```vim
x       " 문자 삭제
dd      " 줄 삭제
D       " 커서부터 줄 끝까지 삭제
dw      " 단어 삭제
d$      " 커서부터 줄 끝까지 삭제
d0      " 커서부터 줄 시작까지 삭제
```

### 변경 (삭제 + Insert 모드)
```vim
cw      " 단어 변경
ci"     " 따옴표 안 내용 변경
ci(     " 괄호 안 내용 변경
ci{     " 중괄호 안 내용 변경
ca"     " 따옴표 포함 변경
cc      " 줄 변경
C       " 커서부터 줄 끝까지 변경
```

### 복사 (yank)
```vim
yy      " 줄 복사
yw      " 단어 복사
yiw     " 단어 전체 복사 (커서 위치 무관)
yi"     " 따옴표 안 복사
yap     " 단락 복사
y$      " 커서부터 줄 끝까지 복사
```

### 붙여넣기
```vim
p       " 커서 뒤/아래에 붙여넣기
P       " 커서 앞/위에 붙여넣기
```

### 기타
```vim
u       " 되돌리기 (Undo)
Ctrl+R  " 다시 실행 (Redo)
.       " 마지막 명령 반복
~       " 대소문자 전환
J       " 다음 줄과 합치기
Ctrl+A  " 숫자 증가
Ctrl+X  " 숫자 감소
```

---

## 검색/치환

### 검색
```vim
/pattern    " 앞으로 검색
?pattern    " 뒤로 검색
n           " 다음 검색 결과
N           " 이전 검색 결과
*           " 커서 단어 앞으로 검색
#           " 커서 단어 뒤로 검색
:noh        " 검색 하이라이트 끄기
```

### 치환
```vim
:s/old/new/         " 현재 줄의 첫 매칭 치환
:s/old/new/g        " 현재 줄의 모든 매칭 치환
:%s/old/new/g       " 파일 전체 치환
:%s/old/new/gc      " 확인하며 치환
:%s/\<word\>/new/g  " 단어 경계 치환
```

### :g 명령
```vim
:g/pattern/d        " 패턴 매칭 줄 삭제
:g!/pattern/d       " 패턴 미매칭 줄 삭제
:g/pattern/s/old/new/g  " 매칭 줄에서만 치환
```

---

## 레지스터

### 레지스터 종류
```vim
"       " 무명 레지스터 (기본)
"0      " yank 레지스터 (마지막 yank 내용)
"a-"z   " 이름 있는 레지스터
"+      " 시스템 클립보드
"_      " 블랙홀 레지스터 (삭제 시 레지스터 오염 방지)
```

### 사용법
```vim
"ayy    " 레지스터 a에 줄 복사
"ap     " 레지스터 a에서 붙여넣기
"+y     " 시스템 클립보드로 복사
"+p     " 시스템 클립보드에서 붙여넣기
"0p     " 마지막 yank 내용 붙여넣기
"_dd    " 블랙홀 레지스터로 삭제 (레지스터 보존)
:reg    " 레지스터 내용 확인
```

---

## 윈도우/버퍼

### 윈도우 분할
```vim
:sp [file]      " 수평 분할
:vsp [file]     " 수직 분할
Ctrl+W s        " 수평 분할
Ctrl+W v        " 수직 분할
Ctrl+W q        " 윈도우 닫기
```

### 윈도우 이동
```vim
Ctrl+W h        " 왼쪽 윈도우
Ctrl+W j        " 아래 윈도우
Ctrl+W k        " 위 윈도우
Ctrl+W l        " 오른쪽 윈도우
Ctrl+W w        " 다음 윈도우
```

### 윈도우 크기
```vim
Ctrl+W =        " 크기 균등하게
Ctrl+W _        " 높이 최대화
Ctrl+W |        " 너비 최대화
```

### 버퍼 관리
```vim
:e file         " 파일 열기
:bn             " 다음 버퍼
:bp             " 이전 버퍼
:bd             " 버퍼 닫기
:ls             " 버퍼 목록
:b {n}          " n번 버퍼로 이동
:b {name}       " 이름으로 버퍼 이동
```

---

## 비주얼 모드

### 선택
```vim
v       " Visual 모드 시작
V       " Visual Line 모드 시작
Ctrl+V  " Visual Block 모드 시작
o       " 선택 반대편 끝으로 커서 이동
gv      " 이전 선택 영역 재선택
```

### 블록 모드 편집
```vim
Ctrl+V → jjj → I → text → Esc   " 여러 줄 앞에 텍스트 삽입
Ctrl+V → jjj → $ → A → text → Esc   " 여러 줄 끝에 텍스트 추가
Ctrl+V → 선택 → c → text → Esc  " 블록 변경
Ctrl+V → 선택 → d               " 블록 삭제
```

---

## NeoVim 플러그인 (기본 키 매핑)

### Telescope (퍼지 파인더)
```vim
<leader>ff      " 파일 찾기
<leader>fg      " 텍스트 검색 (live grep)
<leader>fb      " 버퍼 목록
<leader>fr      " 최근 파일
<leader>fh      " 도움말 검색
<leader>fd      " 진단 목록
<leader>fs      " 심볼 검색
```

### Neo-tree (파일 탐색기)
```vim
<leader>e       " 파일 탐색기 토글
```

### LSP (Language Server Protocol)
```vim
gd              " 정의로 이동
gr              " 참조 찾기
gI              " 구현으로 이동
K               " 문서 보기 (Hover)
<leader>rn      " 이름 변경 (Rename)
<leader>ca      " 코드 액션
[d              " 이전 진단
]d              " 다음 진단
```

### 자동완성 (nvim-cmp)
```vim
Ctrl+N          " 다음 항목
Ctrl+P          " 이전 항목
Ctrl+Space      " 완성 트리거
Ctrl+E          " 완성 취소
Enter           " 선택 확인
Tab             " 다음 항목 / 스니펫 점프
Shift+Tab       " 이전 항목 / 스니펫 역점프
```

---

## 실습 파일 구조

```
practice/
├── README.md                       # 이 파일
├── configs/                        # 설정 파일
│   ├── minimal-init.lua            # 최소 NeoVim 설정
│   ├── full-init.lua               # 완전한 설정 (플러그인 포함)
│   ├── .ideavimrc                  # IdeaVim 설정
│   └── lazy-plugins/               # Lazy.nvim 플러그인 스펙
│       ├── telescope.lua
│       ├── treesitter.lua
│       ├── lsp.lua
│       ├── cmp.lua
│       └── ui.lua
└── exercises/                      # 연습 파일
    ├── 01-navigation.txt           # 내비게이션 연습
    ├── 02-operators.txt            # 연산자 + 모션 연습
    ├── 03-editing.txt              # 편집 연습
    ├── 04-registers.txt            # 레지스터 연습
    ├── 05-search-replace.txt       # 검색/치환 연습
    ├── 06-visual-block.txt         # 비주얼 블록 연습
    └── 07-multi-file/              # 다중 파일 연습
        ├── file-a.ts
        ├── file-b.ts
        └── file-c.ts
```

---

## 설정 파일 사용법

### 최소 설정 (플러그인 없음)
```bash
cp configs/minimal-init.lua ~/.config/nvim/init.lua
nvim
```

### 완전한 설정 (플러그인 포함)
```bash
# 1. full-init.lua를 init.lua로 복사
cp configs/full-init.lua ~/.config/nvim/init.lua

# 2. 플러그인 스펙 디렉토리 생성 및 복사
mkdir -p ~/.config/nvim/lua/plugins
cp configs/lazy-plugins/*.lua ~/.config/nvim/lua/plugins/

# 3. NeoVim 실행 (자동으로 플러그인 설치)
nvim
```

### IdeaVim 설정
```bash
cp configs/.ideavimrc ~/.ideavimrc
# IntelliJ IDEA 재시작
```

---

## 연습 순서 권장

1. **01-navigation.txt** - hjkl, w/b/e, f/t, 줄/파일 이동
2. **02-operators.txt** - d/c/y + 모션, 텍스트 객체
3. **03-editing.txt** - I/A/o/O, 삭제, 되돌리기, 반복
4. **04-registers.txt** - 이름 있는 레지스터, 클립보드, 블랙홀
5. **05-search-replace.txt** - 검색, 치환, :g 명령
6. **06-visual-block.txt** - 블록 선택, 열 편집
7. **07-multi-file/** - 버퍼/윈도우 관리, LSP 기능

각 파일에는 구체적인 미션이 포함되어 있습니다. 파일을 열고 주석/지시사항을 따라 연습하세요.
