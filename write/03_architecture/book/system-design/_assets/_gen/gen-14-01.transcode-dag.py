# 타입 스펙: type-flowchart — 원본 영상이 영상·오디오·메타데이터 세 갈래로 갈라지고, 영상 인코딩과 오디오 인코딩이 한 점에서 합쳐져 조립으로 끝난다. 타원은 시작·끝, 사각형은 작업, 채운 점은 갈래가 다시 만나는 자리다.
# 사실 출처: 추출본 v2.txt 4074~4093행(DAG 모델과 영상에 적용할 수 있는 검수·인코딩·썸네일·워터마크), PDF 230쪽 그림(원본 → 영상·오디오·메타데이터 → 작업 묶음·오디오 인코딩 → 조립),
#   영상 인코딩이 만드는 파일 360p·480p·720p·1080p·4k 다섯 개는 4089행 · PDF 231쪽 그림. 그림에서 조립으로 들어가는 선은 영상 인코딩과 오디오 인코딩 둘이고 메타데이터 갈래는 이어지지 않는다.
#   "원본 영상 300 MB" 의 300 MB 는 3934행의 평균 크기 가정이다.
# Layout conventions: 사각형 높이 56, 타원 높이 48, 영상 작업 묶음은 x 24~492·y 300~388, 열 중심 x=264(영상)·648(오디오)·852(메타데이터), 합류점 y=420. 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, RULE, KR, MONO

W, H = 960, 588
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01 §6",
      "원본 하나가 세 갈래로 갈라졌다가 조립에서 합쳐진다",
      "영상 갈래에서는 검수 · 영상 인코딩 · 썸네일 · 워터마크가 같은 단계에 놓이고, 영상 인코딩은 다섯 파일을 만든다. 오디오 인코딩과 함께 조립으로 합쳐진다.",
      "작업이 노드, 선이 순서 · 선이 없는 작업끼리는 동시에 돈다")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def rect(x, y, w, h, title, sub, c, focal=False, r=6):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, h, c, r, "12", 1.1)
    ty = y + h / 2 + (4 if not sub else -2)
    d.t(x + w / 2, ty, title, 13, ACC if focal else INK, fam(title), "middle", 600)
    if sub:
        d.t(x + w / 2, y + h / 2 + 16, sub, 13 if fam(sub) == KR else 11, MUTED, fam(sub))


# 시작 — 원본 영상
OX, OY, OW, OH = 440, 96, 200, 48
rect(OX, OY, OW, OH, "원본 영상", "", INFO, r=24)
d.t(OX + OW / 2, OY + OH / 2 + 18, "300 MB", 11, MUTED, MONO)

# 세 갈래 — 버스에서 갈라진다
BUS_Y = 176
d.line(OX + OW // 2, OY + OH, OX + OW // 2, BUS_Y, MUTED, 1.4)
d.line(264, BUS_Y, 852, BUS_Y, MUTED, 1.4)
TR_Y, TR_H = 208, 56
for cx, nm, c in ((264, "영상", INFO), (648, "오디오", INFO), (852, "메타데이터", INFO)):
    d.arrow([(cx, BUS_Y), (cx, TR_Y - 4)], MUTED, "ar", 1.4)
    rect(cx - 80, TR_Y, 160, TR_H, nm, "", c)

# 영상 작업 묶음 — 같은 단계에 네 작업
d.box(24, 300, 468, 88, "none", MUTED, 1.0, 6)
d.t(36, 296, "영상 작업(예)", 13, SOFT, KR, "start", 600)
d.arrow([(264, TR_Y + TR_H), (264, 296)], MUTED, "ar", 1.4)
TASKS = (("검수", "", OK, False), ("영상 인코딩", "5 개 파일", OK, False), ("썸네일", "", OK, False), ("워터마크", "", OK, False))
tx = 36
chip_x = {}
for nm, sub, c, _ in TASKS:
    rect(tx, 316, 104, 56, nm, sub, c)
    chip_x[nm] = tx + 52
    tx += 112

# 오디오 인코딩
rect(548, 316, 200, 56, "오디오 인코딩", "", OK)
d.arrow([(648, TR_Y + TR_H), (648, 312)], MUTED, "ar", 1.4)

# 합류 — 영상 인코딩과 오디오 인코딩이 한 점으로
MJ_X, MJ_Y = 424, 420
d.line(chip_x["영상 인코딩"], 372, chip_x["영상 인코딩"], MJ_Y, MUTED, 1.4)
d.line(chip_x["영상 인코딩"], MJ_Y, MJ_X, MJ_Y, MUTED, 1.4)
d.line(648, 372, 648, MJ_Y, MUTED, 1.4)
d.line(648, MJ_Y, MJ_X, MJ_Y, MUTED, 1.4)
d.o.append(f'<circle cx="{MJ_X}" cy="{MJ_Y}" r="4" fill="{INK}"/>')
d.arrow([(MJ_X, MJ_Y), (MJ_X, 448)], MUTED, "ar", 1.4)

# 끝 — 조립
rect(324, 452, 200, 48, "조립", "", ACC, focal=True, r=24)

# 영상 인코딩 결과 파일 — 묶음 아래 왼쪽 여백에 값으로 적는다
d.t(36, 412, "영상 인코딩 결과", 12, SOFT, KR, "start", 600)
d.t(36, 432, "360p.mp4 · 480p.mp4", 11, MUTED, MONO, "start")
d.t(36, 450, "720p.mp4 · 1080p.mp4", 11, MUTED, MONO, "start")
d.t(36, 468, "4k.mp4", 11, MUTED, MONO, "start")

d.legend(H - 56, [("트랙", INFO), ("작업", OK), ("합쳐지는 끝", ACC)])
d.save("14-01.transcode-dag.svg")
