# 01-03.pmtu-blackhole — 크면 버리고 알려 준다, 그 알림이 막히면 조용히 사라진다
# 본문 요구: 헤더 필드 목록에 `Flags`(Do not Fragment)가 이름으로만 있고, 그 비트가 만드는
#           사건이 노트 어디에도 없었다(2026-09-02 전수 확인). 같은 왕복이 ICMP 회신 유무로
#           정상과 블랙홀로 갈리는 것이 요점이라, 결과 표가 아니라 두 왕복을 나란히 둔다.
# 타입 스펙: type-sequence.md — 세로가 시간, 가로가 주체. 위 묶음은 ICMP 가 돌아오고 아래 묶음은
#           같은 자리에 화살표가 없다. 그 빈자리가 이 그림의 논지다.
# 좌표: Layout conventions 타입이라 공식이 없다. 메시지 stride 52 하나, 묶음 사이만 +16.
# 이력: 2026-09-15 하단 해설 세 문장(본문 도식 뒤 세 문단과 같은 말)을 뺐다. Seq.state·selfmsg 가
#       한글 라벨을 mono 로 찍고 칩 폭을 글자당 7px 로 잡아 한글이 넘치던 것을 아래 kr_state 로 바꿨다.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 584
Y0, STRIDE, RAIL_BOT = 176, 52, 512

d = Seq(W, H, "PATH MTU DISCOVERY · AND ITS BLACK HOLE",
        "크면 버리고 크기를 알려 준다 — 그 알림이 막히면 조용히 사라진다",
        "DF 비트를 세운 패킷이 링크 MTU 를 넘었을 때의 두 갈래. 위는 라우터의 ICMP 가 돌아와 "
        "송신이 크기를 줄이는 정상 경로이고, 아래는 그 ICMP 가 차단돼 같은 크기로 재전송만 반복하는 경우다.",
        lead="두 묶음의 차이는 화살표 하나입니다 · 아래 묶음에는 돌아오는 알림이 없습니다")

d.lanes([("송신 호스트", "MTU 1500"), ("중간 라우터", "다음 링크 MTU 1450"), ("목적지", "웹 서버")])
A, R, B = "송신 호스트", "중간 라우터", "목적지"
d.rails(RAIL_BOT)


def kr_state(lane, txt, y, c):
    """Seq.state 와 같은 칩이되 한글은 한글 스택·1em 폭으로 잰다(계약 §프리미티브가 한글을 mono 로)."""
    x = d.LX[lane]
    w = sum(12 if "가" <= ch <= "힣" else 7 for ch in txt) + 20
    d.o.append(f'<rect x="{x-w/2}" y="{y-11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 12, c, KR)


y = Y0
d.msg(A, R, "1500B  DF=1", y, INFO, sub="쪼개지 말라는 표시(DF)")
y += STRIDE
kr_state(R, "1450 초과 → 폐기", y, WARN)
y += STRIDE
d.msg(R, A, "ICMP  Frag Needed  MTU=1450", y, OK, dash="4 4", sub="폐기 알림 + 줄일 크기")
y += STRIDE
d.msg(A, B, "1450B  DF=1", y, OK, sub="줄여서 재전송 · 통과")

y += STRIDE + 16
d.msg(A, R, "1500B  DF=1", y, INFO, sub="같은 패킷, 같은 표시")
y += STRIDE
kr_state(R, "폐기 · ICMP 차단됨", y, BAD)
y += STRIDE
x = d.LX[A]
d.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", BAD, 1.4, m="bad")
d.t(x + 68, y - 4, "같은 크기로 재전송 반복", 12, BAD, KR, "start")
d.t(x + 68, y + 13, "알림 없음 → 크기 그대로", 11, MUTED, KR, "start")

# 하단 해설 세 문장(라우터가 두 번 말함 · 블랙홀 · 큰 응답만 멈춤)은 도식 뒤 본문 세 문단이 말한다 — 뺐다
d.legend(RAIL_BOT + 32, [("알림이 돌아온다", OK), ("보낸 패킷", INFO),
                         ("버리는 판단", WARN), ("알림이 없다", BAD)])
d.save("01-03.pmtu-blackhole.svg")
print("ok pmtu-blackhole")
