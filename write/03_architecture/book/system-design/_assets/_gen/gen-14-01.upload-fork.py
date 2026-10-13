# 타입 스펙: type-process — 업로드 한 건이 영상 갈래·완료 통지 갈래·메타데이터 갈래 세 줄로 흐르고, 변환 서버 뒤에서 변환본 저장과 완료 이벤트로 갈라진다. 번호가 순서를 나르고 칸마다 파일 이름·개수가 바뀐다.
# 사실 출처: 추출본 v2.txt 3976~3996행(부품)·4002~4015행(영상 갈래의 1·2·3a·3b·3a.1·3b.1 와 4)·4016~4019행(메타데이터 갈래), PDF 224쪽 · 226쪽 · 227쪽 그림(변환 서버에서 변환본 저장소와 완료 큐가 갈라진다).
#   변환본 5 개는 4089행 · PDF 231쪽 그림의 360p·480p·720p·1080p·4k 다섯 파일이고, funny.mov 와 300 MB 는 설명용 예시 값(300 MB 는 3934행의 평균 크기 가정, 이름은 4178행의 funny_720p.mp4 에서 따옴).
# Layout conventions: 노드 폭 156 · 높이 64, 열 stride 196(x=24 부터), 띠 stride 116(y=100 부터)·띠 머리 28, 노드 y=128·244·360. 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, RULE, KR, MONO

W, H = 988, 504
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01 §3",
      "변환 뒤에 변환본과 완료 이벤트로 갈라지고 메타데이터는 따로 흐른다",
      "클라이언트가 funny.mov 300 MB 를 원본 저장소에 올리는 동안 메타데이터 요청이 API 서버를 지나 DB 에 적힌다. 변환이 끝나면 변환본 5 개는 CDN 으로, 완료 이벤트는 큐와 처리기를 지나 DB 를 바꾼다.",
      "번호는 업로드 한 건이 지나는 순서 · a 는 메타데이터")

NW, NH, XS, XST = 156, 64, 24, 196
ROW = {"A": 128, "B": 244, "M": 360}
BAND = (("영상 갈래", 100), ("완료 통지 갈래", 216), ("메타데이터 갈래", 332))


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def X(c):
    return XS + XST * c


def node(c, row, title, sub, color, focal=False):
    x, y = X(c), ROW[row]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, NW, NH, color, 6, "12", 1.1)
    d.t(x + NW / 2, y + 28, title, 13, ACC if focal else INK, fam(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13 if fam(sub) == KR else 11, MUTED, fam(sub))


for lab, top in BAND:
    d.line(24, top, W - 24, top, RULE, 0.8)
    d.t(24, top + 18, lab, 13, SOFT, KR, "start", 600)

# 영상 갈래
node(0, "A", "클라이언트", "funny.mov · 300 MB", MUTED)
node(1, "A", "원본 저장소", "BLOB · 원본 1 개", INFO)
node(2, "A", "트랜스코딩 서버", "원본 1 → 파일 5", OK, focal=True)
node(3, "A", "변환본 저장소", "BLOB · 파일 5 개", INFO)
node(4, "A", "CDN", "엣지에 복제", INFO)
# 완료 통지 갈래
node(3, "B", "완료 큐", "완료 이벤트", WARN)
node(4, "B", "완료 처리기", "큐에서 꺼냄", OK)
# 메타데이터 갈래
node(1, "M", "API 서버", "파일명 · 크기 · 형식", OK)
node(4, "M", "메타 DB · 캐시", "변환 완료를 반영", INFO)

yA = ROW["A"] + NH // 2
# 1 올림 · 2 가져옴
d.arrow([(X(0) + NW + 2, yA), (X(1) - 6, yA)], MUTED, "ar", 1.5)
d.chip(X(0) + NW + 20, yA - 18, "1", MUTED, 11)
d.arrow([(X(1) + NW + 2, yA), (X(2) - 6, yA)], MUTED, "ar", 1.5)
d.chip(X(1) + NW + 20, yA - 18, "2", MUTED, 11)
# 3a 변환본 저장 — 수평
d.arrow([(X(2) + NW + 2, yA - 8), (X(3) - 6, yA - 8)], MUTED, "ar", 1.5)
d.chip(X(2) + NW + 20, yA - 26, "3a", MUTED, 11)
# 3b 완료 이벤트 — 같은 열에서 내려가 완료 큐 왼쪽으로
cx = X(2) + NW + 20
yB = ROW["B"] + NH // 2
d.arrow([(X(2) + NW + 2, yA + 12), (cx, yA + 12), (cx, yB), (X(3) - 6, yB)], WARN, "warn", 1.5)
d.chip(cx, yB - 36, "3b", WARN, 11)
# 4 배포
d.arrow([(X(3) + NW + 2, yA), (X(4) - 6, yA)], MUTED, "ar", 1.5)
d.chip(X(3) + NW + 20, yA - 18, "4", MUTED, 11)
# 5 꺼냄
d.arrow([(X(3) + NW + 2, yB), (X(4) - 6, yB)], MUTED, "ar", 1.5)
d.chip(X(3) + NW + 20, yB - 18, "5", MUTED, 11)
# 6 반영
cxd = X(4) + NW // 2
d.arrow([(cxd, ROW["B"] + NH + 2), (cxd, ROW["M"] - 6)], MUTED, "ar", 1.5)
d.chip(cxd, ROW["B"] + NH + 12, "6", MUTED, 11)

# a 메타데이터 — 클라이언트에서 내려가 API 서버로, 다시 메타 DB 로
yM = ROW["M"] + NH // 2
cxc = X(0) + NW - 32
d.arrow([(cxc, ROW["A"] + NH + 2), (cxc, yM), (X(1) - 6, yM)], INFO, "info", 1.5)
d.chip(cxc, 300, "a", INFO, 11)
d.arrow([(X(1) + NW + 2, yM), (X(4) - 6, yM)], INFO, "info", 1.5)
d.chip((X(1) + NW + X(4)) // 2, yM - 18, "a", INFO, 11)

d.legend(H - 56, [("클라이언트", MUTED), ("저장소 · CDN · DB", INFO), ("서버", OK), ("큐", WARN), ("갈라지는 지점", ACC)])
d.save("14-01.upload-fork.svg")
