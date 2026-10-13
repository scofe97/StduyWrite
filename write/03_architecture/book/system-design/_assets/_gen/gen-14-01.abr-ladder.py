# 타입 스펙: type-process — 레인 셋(영상 화질 low·mid·hi, 오디오 전용 줄은 쓰지 않음)과 칸 여섯(조각 1~6)을 두고, 조각마다 측정한 처리량보다 BANDWIDTH 가 낮은 가장 높은 화질로 칸이 옮겨 간다.
# 사실 출처: BANDWIDTH 1,280,000·2,560,000·7,680,000 bps 와 low·mid·hi.m3u8 이름은 RFC 8216 §8.4 Master Playlist 예(draft-pantos-hls-rfc8216bis-22 §9.4 도 같은 값). BANDWIDTH 의 뜻(화질의 최대 조각 비트레이트)은 RFC 8216 §4.3.4.2,
#   화질 전환은 §2("Clients should switch between different Variant Streams to adapt to network conditions"). 조각별 측정 처리량 8.0 · 8.4 · 3.1 · 2.9 · 1.4 · 5.0 Mbps 와 "가장 높은 화질을 고른다"는 규칙은 설명용 예시이며 규격이 정한 값이 아니다.
#   화질 고르기: 8.0 ≥ 7.68 → hi · 8.4 → hi · 2.56 ≤ 3.1 < 7.68 → mid · 2.9 → mid · 1.28 ≤ 1.4 < 2.56 → low · 2.56 ≤ 5.0 < 7.68 → mid.
# Layout conventions: 노드 폭 100 · 높이 64, 레인 stride 80, 칸 stride 124, label_col 140 · right_pad 28, 처리량 줄 y=104. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, SOFT, RULE, KR, MONO

LCW, SLOT, NW, NH = 140, 124, 100, 64
NS = 6
W = LCW + NS * SLOT + 28
TP_Y, L_Y0, LS = 100, 144, 80
H = 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01 §4",
      "처리량이 떨어지면 그 조각부터 낮은 화질을 받는다",
      "Master Playlist 의 영상 화질은 1,280,000 · 2,560,000 · 7,680,000 bps 셋이다. 조각 다섯 번째에서 측정 처리량이 1.4 Mbps 로 떨어지자 플레이어는 mid 에서 low 로 내려간다.",
      "설명용 예시 처리량 · BANDWIDTH 는 RFC 8216 의 예")

LANES = (("hi", "7.68 Mbps", 7_680_000), ("mid", "2.56 Mbps", 2_560_000), ("low", "1.28 Mbps", 1_280_000))
THR = (8.0, 8.4, 3.1, 2.9, 1.4, 5.0)


def nx(j):
    return LCW + j * SLOT + 12


def pick(mbps):
    for k, (_, _, bw) in enumerate(LANES):
        if bw <= mbps * 1_000_000:
            return k
    return len(LANES) - 1


d.t(24, TP_Y + 20, "측정 처리량", 13, SOFT, KR, "start", 600)
for j, v in enumerate(THR):
    d.t(nx(j) + NW / 2, TP_Y + 20, f"{v} Mbps", 12, SOFT, MONO, "middle", 600)

for k, (name, label, _) in enumerate(LANES):
    y = L_Y0 + k * LS
    d.line(LCW - 8, y - 8, W - 24, y - 8, RULE, 0.8)
    d.t(24, y + 28, f"{name}.m3u8", 13, INK, MONO, "start", 600)
    d.t(24, y + 48, label, 12, MUTED, MONO, "start")

prev = None
for j, v in enumerate(THR):
    k = pick(v)
    name, label, _ = LANES[k]
    x, y = nx(j), L_Y0 + k * LS
    focal = j == 4
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        c = (OK, INFO, WARN)[k]
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, f"조각 {j + 1}", 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + NW / 2, y + 48, f"{name}.m3u8", 11, MUTED, MONO, "middle")
    if prev is not None:
        px, pk = prev
        py = L_Y0 + pk * LS + NH // 2
        cy = y + NH // 2
        if pk == k:
            d.arrow([(px + NW + 2, py), (x - 6, cy)], MUTED, "ar", 1.5)
        else:
            mx = px + NW + 12
            d.arrow([(px + NW + 2, py), (mx, py), (mx, cy), (x - 6, cy)], ACC if focal else MUTED, "acc" if focal else "ar", 1.5)
    prev = (x, k)

d.legend(H - 56, [("hi", OK), ("mid", INFO), ("low", WARN), ("화질이 내려간 조각", ACC)])
d.save("14-01.abr-ladder.svg")
