# 02-01 §이미지 = 레이어 목록 — 실물은 해시 저장소에 한 벌씩
# 본문: "이미지는 레이어 실물을 통째로 담은 덩어리가 아니라, '어떤 해시의 레이어를 순서대로
#        쌓을지' 적은 목록(manifest)입니다. 레이어 실물은 해시로 식별되는 저장소에 딱 한 벌씩
#        있고, 여러 이미지의 manifest 가 같은 해시 레이어를 함께 가리킵니다."
#       "pull 할 때도 manifest 를 먼저 받고 거기 적힌 레이어 중 없는 것만 다운로드합니다."
# 타입 스펙: 목록이 실물을 *가리키는* 구조라 참조 매핑이다. 같은 해시를 둘이 가리키는 자리가
#           요점이므로 그 레이어에만 focal 을 걸고, 나머지는 고유 레이어로 묶어 화살표 수를 줄인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 688
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "manifest 는 해시 목록이고, 실물은 한 벌씩 있다",
      "두 이미지의 manifest 가 같은 해시를 적어 두면 그 레이어는 디스크에 한 벌만 있고 둘이 "
      "함께 가리킨다. 저장도 전송도 이미지가 아니라 레이어 단위로 이뤄진다.",
      lead="그래서 두 번째 pull 이 빠르다 — 이미 있는 레이어는 Already exists 로 건너뛴다")

NG, RD = (250, 260), (740, 260)
MW, MH = 400, 116
STORE = (56, 420, 888, 152)
BASE, NUQ, RUQ = (500, 496), (196, 496), (804, 496)

ddx.band(d, 104, 632, "manifest 가 같은 해시를 적었다는 것은 내용이 바이트 단위로 같다는 뜻이다")

def manifest(cx, cy, name, lines, c):
    d.box(cx - MW // 2, cy - MH // 2, MW, MH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 34, name, 13, c, MONO, "middle", 600)
    for i, (h, note) in enumerate(lines):
        y = cy - 8 + i * 22
        d.t(cx - MW // 2 + 20, y, f"↳ {h}", 11, ACC if i == 0 else MUTED, MONO, "start")
        d.t(cx + MW // 2 - 20, y, note, 10, SOFT, KR, "end")

manifest(*NG, "nginx:alpine", [("91d5cf66…", "alpine 베이스"), ("a1b2…", "nginx RUN"),
                               ("c3d4…", "nginx conf·CMD")], INFO)
manifest(*RD, "redis:alpine", [("91d5cf66…", "alpine 베이스"), ("e5f6…", "redis RUN"),
                               ("7a8b…", "redis conf·ENV")], OK)

sx, sy, sw, sh = STORE
d.o.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" '
           f'fill="{RULE}" fill-opacity="0.03" stroke="{RULE}" stroke-width="1.0"/>')
d.t(sx, sy - 12, "디스크의 레이어 저장소 — 해시가 곧 주소, 실물은 한 벌씩", 11, SOFT, KR, "start")

def layer(cx, cy, w, t, s, c, focal=False):
    x, y = cx - w // 2, cy - 38
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="76" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, 76, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(t, 12, w - 18, t), 12, ACC if focal else c, MONO, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, w - 14, t), 10, SOFT, KR)

layer(*NUQ, 220, "a1b2… · c3d4…", "nginx 고유 레이어", INFO)
layer(*BASE, 280, "91d5cf66… · 8.66MB", "둘이 함께 가리킨다 — 한 벌만", INFO, focal=True)
layer(*RUQ, 220, "e5f6… · 7a8b…", "redis 고유 레이어", OK)

d.path(f"M {NUQ[0]} {NG[1]+MH//2+6} L {NUQ[0]} {NUQ[1]-38-10}", INFO, 1.5, m="info")
d.path(f"M {RUQ[0]} {RD[1]+MH//2+6} L {RUQ[0]} {RUQ[1]-38-10}", OK, 1.5, m="ok")
d.path(f"M 320 {NG[1]+MH//2+6} L 320 380 L 430 380 L 430 {BASE[1]-38-10}", ACC, 1.8, m="acc")
d.path(f"M 670 {RD[1]+MH//2+6} L 670 380 L 570 380 L 570 {BASE[1]-38-10}", ACC, 1.8, m="acc")
d.chip(500, 380, "같은 해시 → 한 벌만", ACC, 11)

# 저장소 존이 420~572 를 쓴다 — 산문은 그 아래로 (616-80 은 계산 실수였다)
d.t(36, 604, "pull 하면 manifest 를 먼저 받고 거기 적힌 해시 중 없는 것만 내려받는다 — "
                  "이미 있으면 Already exists 로 건너뛴다.", 12, MUTED, KR, "start")
d.legend(648, [("nginx 쪽", INFO), ("redis 쪽", OK), ("둘이 함께 가리키는 레이어", ACC)])
d.save("02-01-image-manifest-layers.svg")
print("ok image-manifest-layers")
