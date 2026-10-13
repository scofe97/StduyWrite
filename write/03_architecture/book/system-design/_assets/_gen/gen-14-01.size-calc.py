# 타입 스펙: type-process — 레인 둘(압축 안 한 영상 · 12 Mbps 로 압축한 영상)이 한 시간 분량의 바이트로 환산되고 칸마다 실제 값이 바뀐다(스펙 §2 공식의 label_col_w 140 · right_pad 28 을 따르고 step_slot_w 는 124 로 넓혔다).
# 사실 출처: "한 시간짜리 60 프레임 HD 영상이 수백 GB" 는 추출본 v2.txt 4058~4059행. 계산은 1920 × 1080 × 1.5 B(8 비트 4:2:0 가정) × 60 fps × 3,600 s.
#   12 Mbps 는 YouTube 도움말 "Recommended upload encoding settings"(https://support.google.com/youtube/answer/1722171) SDR 1080p 고프레임(48·50·60)의 권장 업로드 비트레이트이며 서비스가 내보내는 변환본의 비트레이트가 아니다.
#   계산: 1920 × 1080 = 2,073,600 · × 1.5 = 3,110,400 B · × 60 = 186,624,000 B/s · × 3,600 = 671,846,400,000 B ≈ 671.8 GB. 12,000,000 ÷ 8 = 1,500,000 B/s · × 3,600 = 5,400,000,000 B = 5.4 GB. 671.8 ÷ 5.4 ≈ 124.
# Layout conventions: 노드 폭 100 · 높이 64, 레인 stride 80, 칸 stride 124(스펙 112 에서 12 늘려 화살표 구간 24 확보). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, SOFT, INFO, RULE, KR, MONO

LCW, SLOT, NW, NH = 140, 124, 100, 64
NS = 5
W = LCW + NS * SLOT + 28
HDR_Y, L1_Y, L2_Y = 100, 136, 216
H = 404
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01 §5",
      "한 시간 분량이 671.8 GB 에서 5.4 GB 로 줄어든다",
      "1920 × 1080 픽셀에 1.5 B, 60 프레임으로 한 시간을 곱하면 671.8 GB 이고, 12 Mbps 로 압축하면 5.4 GB 라서 약 124 배 줄어든다.",
      "8 비트 4:2:0 가정 · 12 Mbps 는 1080p 고프레임 권장 업로드 값")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def nx(j):
    return LCW + j * SLOT + 12


def node(j, y, title, sub, c, focal=False):
    x = nx(j)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, title, 12, ACC if focal else INK, fam(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, fam(sub))


for j, lab in enumerate(["입력", "프레임", "초당", "한 시간", "결과"]):
    d.t(nx(j) + NW / 2, HDR_Y + 12, f"{j + 1} · {lab}", 12, SOFT, KR, "middle", 600)

d.line(LCW - 8, L1_Y - 12, W - 24, L1_Y - 12, RULE, 0.8)
d.line(LCW - 8, L2_Y - 12, W - 24, L2_Y - 12, RULE, 0.8)
d.t(24, L1_Y + 30, "압축 안 함", 13, INK, KR, "start", 600)
d.t(24, L2_Y + 30, "12 Mbps", 13, INK, MONO, "start", 600)

# 레인 1 — 압축하지 않은 영상
node(0, L1_Y, "1920 × 1080", "2,073,600 픽셀", INFO)
node(1, L1_Y, "3,110,400 B", "× 1.5 B", OK)
node(2, L1_Y, "186,624,000", "B/s · × 60", OK)
node(3, L1_Y, "× 3,600 s", "한 시간", OK)
node(4, L1_Y, "671.8 GB", "압축 전", WARN)
for j in range(4):
    d.arrow([(nx(j) + NW + 2, L1_Y + NH // 2), (nx(j + 1) - 6, L1_Y + NH // 2)], MUTED, "ar", 1.5)

# 레인 2 — 12 Mbps 로 압축한 영상
node(0, L2_Y, "12 Mbps", "비트 / 초", INFO)
node(2, L2_Y, "1,500,000", "B/s · ÷ 8", OK)
node(3, L2_Y, "× 3,600 s", "한 시간", OK)
node(4, L2_Y, "5.4 GB", "≈ 1/124", ACC, True)
d.arrow([(nx(0) + NW + 2, L2_Y + NH // 2), (nx(2) - 6, L2_Y + NH // 2)], MUTED, "ar", 1.5)
for j in (2, 3):
    d.arrow([(nx(j) + NW + 2, L2_Y + NH // 2), (nx(j + 1) - 6, L2_Y + NH // 2)], MUTED, "ar", 1.5)

d.legend(H - 56, [("입력 값", INFO), ("중간 값", OK), ("압축 전 크기", WARN), ("압축 후 크기", ACC)])
d.save("14-01.size-calc.svg")
