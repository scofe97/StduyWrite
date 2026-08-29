# 19-01 §랩 — amicontained 없이 /proc 으로 직접 잽니다
# 본문이 이 도식의 규격을 준다 — "두 출력을 나란히 놓으면" 이고, 초점을 CapEff 줄이라 못 박는다.
# 그러니 before/after 를 두 카드로 떼어 놓으면 안 되고 *같은 행에 붙여* 놓아야 한다.
# 행이 맞아야 "CapBnd 는 거의 안 변했는데 CapEff 만 무너졌다" 가 눈으로 잡힌다 —
# 그게 이 절 전체의 논지이고, 책의 도구가 가려 버린 것이다.
# 마지막 열에 변화를 적는 이유도 같다. 두 값만 보면 16진수라 차이가 안 읽힌다.
# 타입 스펙: type-dp-security-matrix.md — 열 넷(항목 · 기본 · 강화 · 무엇이 달라졌나) × 행 아홉의
#           격자이고 연결선이 없다. 본문이 "두 출력을 나란히 놓으면" 이라고 규격을 적어 두었고,
#           행이 맞아야 "CapBnd 는 그대로인데 CapEff 만 무너졌다" 가 눈으로 잡힌다.
#           어긋나는 지점: 정본이 초점 칸을 하나로 제한하는데 여기는 두 행(CapEff · CapPrm)이 초점이다.
#           둘을 함께 짚지 않으면 "상한은 남았으니 되찾을 수 있다" 로 잘못 읽히므로, 신호가
#           흐려지는 비용을 알고 감수한 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 828
d = D(W, H, "KUBERNETES UP AND RUNNING · 19-01",
      "무너진 것은 상한이 아니라 손에 쥔 것이다",
      "책의 amicontained 는 bounding 집합만 찍는다. 그것만 보면 capability 는 14 개에서 "
      "14 개로 거의 그대로다. 실제로 0 이 된 것은 effective 집합이다.",
      "kind 로컬 클러스터 실측 — alpine:3.20 · /proc/self/status · 서버 v1.35.0")

COLS = [("항목", 24, 196), ("기본 — 아무것도 걸지 않음", 228, 372),
        ("강화 — 책의 SecurityContext", 608, 372), ("무엇이 달라졌나", 988, 228)]
HDR_Y, Y0, RH, GAP = 130, 150, 56, 8

for name, x, w in COLS:
    d.t(x, HDR_Y, name, 9, SOFT, KR, "start")

ROWS = [
    ("CapBnd", "00000000a80425fb", "14개", "00000000aa0421fb", "14개",
     "net_bind_service 빠지고\nsys_time 더해짐", MUTED, False),
    ("CapEff", "00000000a80425fb", "14개", "0000000000000000", "0개",
     "전부 사라짐", ACC, True),
    # CapPrm 을 빼면 bounding 을 '상한' 이라 부른 것이 오해를 남긴다 —
    # 되찾을 밑천(CapPrm)이 0 이고 NoNewPrivs 가 1 이면 그 상한은 회수 불가다.
    ("CapPrm", "00000000a80425fb", "14개", "0000000000000000", "0개",
     "되찾을 밑천도 없음", ACC, True),
    ("NoNewPrivs", "0", "", "1", "", "권한 상승이 봉인됨", OK, False),
    ("Seccomp", "0", "필터 없음", "2", "필터링", "RuntimeDefault 가 걸림", OK, False),
    ("uid / gid", "0 / 0", "root", "1000 / 3000", "비root", "root 를 벗어남", OK, False),
    ("보조 그룹", "없음", "", "2000", "fsGroup", "fsGroup 이 들어옴", MUTED, False),
    ("루트 FS", "writable", "", "read-only", "", "쓰기가 막힘", MUTED, False),
]

for i, (label, b, bs, a, as_, delta, c, focal) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    d.t(COLS[0][1] + 8, y + RH / 2 + 5, label, 12, INK if focal else MUTED,
        MONO, "start", 600 if focal else 400)
    for (cell, sub, cc), (_, cx, cw) in zip(
            ((b, bs, MUTED), (a, as_, c)), (COLS[1], COLS[2])):
        if focal:
            d.tone(cx, y, cw, RH, cc, 6, "12", 1.4)
        else:
            d.box(cx, y, cw, RH, PAPER2, RULE, 0.9, 6)
        d.t(cx + 16, y + (26 if sub else RH / 2 + 5), cell, 12,
            cc if focal else INK, MONO, "start", 600 if focal else 400)
        if sub:
            d.t(cx + cw - 16, y + 26, sub, 10, cc if focal else SOFT, KR, "end")
    _, dx, dw = COLS[3]
    lines = delta.split("\n")
    for j, ln in enumerate(lines):
        # 변화 열은 항상 그 행의 색을 쓴다 — 범례의 색이 도식 어디에도 없으면 오해를 부른다
        d.t(dx, y + RH / 2 + 5 - (len(lines) - 1) * 7 + j * 14,
            ddx.fit(ln, 10, dw, ln), 10, c, KR, "start", 600 if focal else 400)

BY = Y0 + len(ROWS) * (RH + GAP) + 10
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.o.append(f'<rect x="24" y="{BY+20}" width="{W-72}" height="62" rx="6" '
           f'fill="{ACC}0C" stroke="{ACC}" stroke-width="1.2"/>')
d.t(44, BY + 44, "bounding 은 앞으로 가질 수 있는 상한이고 effective 는 지금 행사하는 권한이다",
    12, ACC, KR, "start", 600)
d.t(44, BY + 66, "runAsUser 만 빼고 나머지를 그대로 두면 CapEff 가 다시 14 개로 돌아온다 — 절제로 확인했다. "
                 "값한 조치는 capability 가감이 아니라 비root 전환이다",
    10, MUTED, KR, "start")

d.legend(BY + 96, [("이 절의 초점", ACC), ("확실히 좋아진 것", OK), ("상한은 그대로", MUTED)])
d.save("19-01.securitycontext-measured.svg")
print("필요 h:", BY + 96 + 48, "· 실제:", H)
