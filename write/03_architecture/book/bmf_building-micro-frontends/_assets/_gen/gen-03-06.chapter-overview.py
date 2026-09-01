# 03-06 전체 지도 — iframe 이 만드는 격리의 겹. 바깥이 넓은 문맥이고 안으로 갈수록 권한이 좁아진다.
# 저자는 이 넷을 겹으로 세지 않는다. 겹으로 묶은 것은 노트의 읽기이며 각 겹의 문구는 원문 서술을 옮긴 것이다.
# 타입 스펙: type-nested — 바깥이 넓은 범위, 안으로 갈수록 구체. 포함 관계가 곧 권한의 범위다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, KR, MONO

W = 1000
rings = [
    (60, 100, 900, 352, "BROWSER TAB", "브라우저 탭", "사용자가 보는 하나의 화면", f"{INK}4D", 1.0, f"{INK}04"),
    (100, 160, 820, 268, "HOST PAGE", "호스트 페이지", "템플릿을 몇 개로 정해 두고 그 자리에 조각을 앉힌다", MUTED, 1.1, f"{INK}06"),
    (140, 220, 740, 184, "IFRAME", "인라인 프레임", "별도의 HTML 문서를 담는다 · postMessage 로만 바깥과 말한다", INK, 1.2, f"{INK}09"),
]
LEGEND_Y = 452 + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-06",
      "iframe 이 만드는 격리의 겹",
      "안으로 들어갈수록 실행할 수 있는 것이 줄어든다. 색이 붙은 가장 안쪽이 브라우저가 주는 가장 강한 격리다.",
      "안으로 들어갈수록 권한이 좁아집니다")

for x, y, w, h, eyebrow, name, desc, stroke, sw, fill in rings:
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    lw = len(eyebrow) * 6.4 + 16
    d.o.append(f'<rect x="{x + 24}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 24 + lw / 2, y + 3, eyebrow, 7.5, SOFT, MONO)
    d.t(x + 24, y + 30, name, 14, INK, KR, "start", 600)
    d.t(x + 24, y + 50, desc, 11, MUTED, KR, "start")

IX, IY, IW, IH = 180, 280, 660, 100
d.o.append(f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
lw = len("SANDBOX ATTRIBUTE") * 6.4 + 16
d.o.append(f'<rect x="{IX + 24}" y="{IY - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
d.t(IX + 24 + lw / 2, IY + 3, "SANDBOX ATTRIBUTE", 7.5, ACC, MONO)
d.t(IX + 24, IY + 32, "sandbox 속성", 15, ACC, KR, "start", 600)
d.t(IX + 24, IY + 58, "단독으로 두면 스크립트도 폼 제출도 막힌다", 11.5, MUTED, KR, "start")
d.t(IX + 24, IY + 80, "allow-scripts · allow-forms 로 하나씩 되돌린다", 11.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("브라우저가 주는 가장 강한 격리", ACC)])
d.save("03-06.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
