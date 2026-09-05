# 02-02 §1 — 네 개 창이 같은 캡처를 어느 범위로 보는가. 바깥에서 안으로 갈수록 범위가 좁아진다.
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 바깥이 넓고 안이 구체적이며,
#           focal 은 가장 안쪽 한 곳(Packet Bytes)에만 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 464
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-02 §1",
      "네 개 창의 범위",
      "캡처 파일에서 한 바이트까지 범위가 네 단계로 좁아진다. 필터 도구모음은 가장 바깥에서 목록 전체를 좁히고, 목록에서 고른 한 줄이 Details 를, Details 에서 고른 한 필드가 Bytes 를 정한다.",
      "안쪽 창이 무엇을 보여줄지는 바깥 창에서 무엇을 골랐는지가 정합니다")

# 안쪽으로 갈수록 좌우 32 · 위 48 · 아래 24 씩 들여쓴다. 레벨마다 같은 값이라 정렬이 유지되고,
# 위아래를 다르게 준 이유는 라벨이 링 상단에만 있어 대칭 여백이면 아래가 빈 채로 쌓이기 때문이다.
RINGS = [
    ("FILTER TOOLBAR", "필터 도구모음", "여기 건 필터가 안쪽 전체를 좁힙니다", 24, 104, 832, 272),
    ("PACKET LIST",    "Packet List",   "한 줄에 프레임 하나. 잡힌 것 전부",   56, 152, 768, 200),
    ("PACKET DETAILS", "Packet Details", "고른 프레임 하나의 계층 트리",        88, 200, 704, 128),
    ("PACKET BYTES",   "Packet Bytes",  "고른 필드의 16진수 덤프",             120, 248, 640, 56),
]

for i, (tag, name, sub, x, y, w, h) in enumerate(RINGS):
    last = (i == len(RINGS) - 1)
    if last:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        op = ["0.30", "0.45", "0.70"][i]
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                   f'fill="{PAPER2}" fill-opacity="{0.25 + i * 0.2}" '
                   f'stroke="{RULE}" stroke-opacity="{op}" stroke-width="1.1"/>')
    # 라벨은 링 상단 테두리 위 paper 마스크에 얹는다
    lab = f"{tag}"
    lw = len(lab) * 6 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y - 7}" width="{lw}" height="14" fill="{PAPER}"/>')
    d.t(x + 24, y + 4, lab, 8, ACC if last else SOFT, MONO, "start")
    d.t(x + 24, y + 30, name, 14, ACC if last else INK, KR, "start", 600)
    d.t(x + w - 24, y + 30, sub, 12, MUTED, KR, "end")

d.legend(408, [("가장 좁은 범위", ACC)])
d.save("02-02.four-panes.svg")
