# 06-01 §1 — 일반 모드와 monitor 모드가 각각 보는 범위. 안으로 갈수록 좁다.
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. focal 은 가장 안쪽 한 곳
#           (일반 모드가 보는 범위)이며, 바깥이 monitor 모드가 더 보는 것들이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 472
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 06-01 §1",
      "monitor 모드가 더 보는 것",
      "일반 모드는 자기 장비가 주고받는 데이터 프레임만 본다. monitor 모드를 켜면 그 채널에서 오가는 관리·제어 프레임과 남의 유니캐스트까지 어댑터가 올려 준다.",
      "안쪽이 일반 모드의 시야이고, 바깥 두 겹이 monitor 모드가 더해 주는 것입니다")

# 좌우 32 · 위 48 · 아래 24 씩 일정하게 들여쓴다 (라벨이 상단에만 있어 대칭이면 아래가 빈다)
RINGS = [
    ("CHANNEL", "채널 전체 트래픽", "monitor 모드가 어댑터에서 올려 줍니다", 24, 104, 832, 272),
    ("MGMT · CTRL", "관리·제어 프레임", "beacon · probe · auth · RTS/CTS · ACK", 56, 152, 768, 200),
    ("BROADCAST", "브로드캐스트·멀티캐스트", "AP 가 뿌리는 것", 88, 200, 704, 128),
    ("MY UNICAST", "내 유니캐스트 데이터", "일반 모드가 보는 전부", 120, 248, 640, 56),
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
    lw = len(tag) * 6 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y - 7}" width="{lw}" height="14" fill="{PAPER}"/>')
    d.t(x + 24, y + 4, tag, 8, ACC if last else SOFT, MONO, "start")
    d.t(x + 24, y + 30, name, 14, ACC if last else INK, KR, "start", 600)
    d.t(x + w - 24, y + 30, sub, 12, MUTED, KR, "end")

d.legend(408, [("일반 모드가 보는 범위", ACC)])
d.save("06-01.monitor-mode-scope.svg")
