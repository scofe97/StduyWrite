# 타입 스펙: type-flowchart — 스캔 단계에서 이미지 속 파일의 지문을 떠 목록으로 만들고, 런타임에 새 실행 파일이 시작될 때마다 강제 도구가 그 목록과 대조한다. 같은 이름 productsearch 인 두 파일(이미지 속 파일 · 주입된 파일)이 한 대조 노드를 지나 실행 허용과 permission denied 로 갈린다(paired traces). focal 은 지문 대조.
# 사실 출처: 노트 L178~L180(불변 컨테이너 · 드리프트 방지), L184~L187(스캐너가 파일 지문을 뜬다 · 새 실행 파일 프로세스마다 대조 · 동일하지 않으면 실행 불가, permission denied), L189(이름만 대조했다면 productsearch 라는 이름으로 채굴기를 심어 우회).
# Layout conventions: 열 x=28·264·500·736(w=200), 스캔 행 y=132(h=56), 런타임 행 y=272·384(h=80), 대조 노드 h=192(두 행에 걸침). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE, PAPER


W, H = 960, 564


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#F5F5F305" stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')
    d.t(x + 16, y + 24, label, 12, MUTED, KR, "start", 600)


d = D(W, H, "CONTAINER SECURITY · 13-01 §4",
      "스캔 때 뜬 파일 지문이 런타임 실행의 허가증이 됩니다",
      "스캐너가 이미지 안 파일들의 지문을 떠 목록으로 남기고, 런타임에는 컨테이너가 새 실행 파일을 시작할 때마다 강제 도구가 그 지문과 대조한다. "
      "동일하면 실행하고, 동일하지 않으면 permission denied로 막는다. 이름이 같아도 지문이 다르면 거부된다.",
      "이름만 대조했다면 같은 이름을 붙인 주입 파일이 통과했을 것입니다.")

# 구역
zone(16, 92, 700, 112, "스캔 단계 · 배포 전")
zone(16, 228, 928, 252, "런타임 · 컨테이너 안")

# 스캔 행
SY, SH = 132, 56
d.arrow([(228, SY + 28), (260, SY + 28)], INFO, "info", 1.4)
d.arrow([(464, SY + 28), (496, SY + 28)], INFO, "info", 1.4)
d.tone(28, SY, 200, SH, INFO, 6, "14", 1.2)
d.t(44, SY + 24, "이미지 속 파일", 14, INK, KR, "start", 600)
d.t(44, SY + 44, "productsearch", 12, MUTED, MONO, "start")
d.tone(264, SY, 200, SH, INFO, 6, "14", 1.2)
d.t(280, SY + 24, "스캐너", 14, INK, KR, "start", 600)
d.t(280, SY + 44, "파일마다 지문 생성", 12, MUTED, KR, "start")
d.tone(500, SY, 200, SH, INFO, 6, "14", 1.2)
d.t(516, SY + 24, "지문 목록", 14, INK, KR, "start", 600)
d.t(516, SY + 44, "스캔의 산출물", 12, MUTED, KR, "start")

# 런타임 — 두 행과 한 대조 노드
RA, RB, RH = 272, 384, 80
CXN, CW = 500, 200
d.arrow([(600, SY + SH + 2), (600, RA - 4)], INFO, "info", 1.5)
d.tone(CXN, RA, CW, RB + RH - RA, ACC, 6, "1F", 1.4)
d.t(CXN + CW // 2, 352, "강제 도구", 14, ACC, KR, "middle", 600)
d.t(CXN + CW // 2, 376, "새 실행 파일마다", 12, MUTED, KR, "middle")
d.t(CXN + CW // 2, 400, "지문 대조", 14, INK, KR, "middle", 600)

FILES = [
    (RA, "이미지 속 실행 파일", "productsearch", "스캔 때 지문 기록", OK),
    (RB, "주입된 실행 파일", "productsearch", "이름 대조라면 통과", WARN),
]
for y, name, fname, note, nc in FILES:
    cy = y + RH // 2
    d.arrow([(340, cy), (CXN - 4, cy)], MUTED, "ar", 1.4)
    d.chip(420, cy, "exec", MUTED, 12)
    d.box(28, y, 312, RH, "#161B22", RULE, 1.0)
    d.t(44, y + 28, name, 14, INK, KR, "start", 600)
    d.t(44, y + 48, fname, 12, MUTED, MONO, "start")
    fit(note, 12, 312 - 32)
    d.t(44, y + 68, note, 12, nc, KR, "start", 600)

OUTS = [
    (RA, OK, "ok", "동일", "실행 허용", KR),
    (RB, BAD, "bad", "불일치", "permission denied", MONO),
]
for y, c, mk, t1, t2, f2 in OUTS:
    cy = y + RH // 2
    d.arrow([(CXN + CW + 2, cy), (732, cy)], c, mk, 1.5)
    d.tone(736, y, 196, RH, c, 6, "14", 1.2)
    d.t(752, y + 34, t1, 14, c, KR, "start", 600)
    d.t(752, y + 58, t2, 12, MUTED if c == OK else INK, f2, "start")

d.legend(504, [("스캔 단계", INFO), ("지문 대조", ACC), ("통과", OK), ("이름만 대조", WARN), ("거부", BAD)])
d.save(str(ASSETS / "13-01.drift-prevention.svg"))
print("ok 13-01 drift-prevention")
