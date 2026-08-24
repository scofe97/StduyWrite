# 02-01 §Copy-on-Write — 수정하는 순간에만 복사한다
# 본문: "컨테이너의 파일시스템은 읽기 전용 레이어들과 그 위에 쌓인 읽기/쓰기 레이어로
#        이뤄집니다. 읽기 전용 레이어 안의 파일을 바꾸면 그 파일 전체가 컨테이너의
#        읽기/쓰기 레이어로 복사되고 그 사본에서 내용이 바뀝니다."
#       "파일을 삭제하면 읽기/쓰기 레이어에 '삭제됨' 으로만 표시될 뿐 아래 레이어에는 남아
#        있습니다 — 즉 이미지 크기는 줄지 않습니다."
# 타입 스펙: 위아래 층이 요점이라 층 그림. 공유 베이스가 두 컨테이너 밑에 하나로 깔리는
#           구조 자체가 답이므로, 베이스를 두 열에 걸치는 한 칸으로 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 604
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "베이스는 하나, 쓰기 레이어는 각자",
      "A 와 B 는 같은 읽기 전용 베이스를 공유하다가, A 가 그 안의 파일을 바꾸는 순간 그 파일만 "
      "A 의 쓰기 레이어로 복사된다. B 는 여전히 원본을 보므로 A 의 변경이 새어 나가지 않는다.",
      lead="공유로 얻는 효율과 격리를 동시에 얻는 장치다 — 건드릴 때만 복사한다")

AX, BX = 270, 720
CW, RW_Y, APP_Y = 400, 300, 218
BASE = (56, 400, 888, 96)

ddx.band(d, 104, 548, "삭제도 마찬가지다 — 쓰기 레이어에 표시만 남고 원본은 아래에 남아 이미지 크기는 줄지 않는다")

def box(cx, cy, w, h, t, s, c, dash=False):
    d.o.append(f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
               f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 8, ddx.fit(t, 12, w - 18, t), 12, c,
        MONO if all(ord(ch) < 128 or ch in '.' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 14, ddx.fit(s, 10, w - 14, t), 10, SOFT, KR)

d.t(AX, APP_Y, "컨테이너 A", 13, INK, KR, "middle", 600)
d.t(BX, APP_Y, "컨테이너 B", 13, INK, KR, "middle", 600)
box(AX, RW_Y, CW, 76, "config.txt (사본)", "A 의 쓰기 레이어 — 여기서 수정됐다", ACC)
box(BX, RW_Y, CW, 76, "비어 있다", "B 의 쓰기 레이어 — 건드리지 않았다", MUTED, dash=True)

bx, by, bw, bh = BASE
d.o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" '
           f'fill="{INFO}12" stroke="{INFO}" stroke-width="1.2"/>')
d.t(bx + bw // 2, by + 38, "공유 읽기 전용 베이스 레이어 — config.txt (원본, 그대로)",
     13, INFO, KR, "middle", 600)
d.t(bx + bw // 2, by + 62, "디스크에 한 벌만 있고 두 컨테이너가 함께 본다", 10, SOFT, KR)

d.path(f"M {AX} {by-6} L {AX} {RW_Y+38+10}", ACC, 1.8, m="acc")
d.chip(AX, 370, "수정하는 순간 그 파일만 복사", ACC, 11)
d.path(f"M {BX} {by-6} L {BX} {RW_Y+38+10}", MUTED, 1.4, dash="6 5")
d.chip(BX, 370, "읽기만 한다 — 복사 없음", MUTED, 11)

d.t(36, 524, "A 가 본 것은 자기 사본이고 B 가 본 것은 원본이다 — 같은 경로인데 서로 다른 파일을 본다.",
     12, MUTED, KR, "start")
d.legend(564, [("공유 베이스 (읽기 전용)", INFO), ("복사가 일어난 자리", ACC)])
d.save("02-01-copy-on-write.svg")
print("ok copy-on-write")
