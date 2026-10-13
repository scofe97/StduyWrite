# 타입 스펙: type-flowchart — 같은 정책 판정 하나에 사건 셋(정책 안 · 정책 밖 · 예상된 오류 경로)이 들어가 서로 다른 끝으로 간다. focal 은 맥락이 붙은 보안 이벤트.
# 사실 출처: 추출본 src/ebpf9.txt 24~31행(/home/<username>/<filename> 은 관심 밖, /etc/passwd 는 알림 대상),
#   34~41행(디스크가 차서 보내는 네트워크 경보 메시지는 보안 이벤트가 아님), 42~48행(정책과 SIEM · 사람 경보), 51~57행(맥락: 무엇이·어느 구성 요소가·언제·누가).
#   맥락 칩 값(프로세스 · 컨테이너 · Pod)은 Kubernetes 환경의 구성 요소 예시다.
# Layout conventions: 행 중심 y=168·288·408(stride 120), 사건 상자 x=24 w=240, 마름모 중심 x=380 반폭 68·반높이 44, 결과 x=560. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 09-01 §1",
      "같은 정책 비교가 사건마다 다른 끝으로 간다",
      "앱의 쓰기가 /home 아래면 무시하고, /etc/passwd 면 맥락을 붙인 보안 이벤트로 SIEM 과 사람에게 보낸다. 디스크가 가득 차 나가는 경보 전송은 정책에 넣어 둔 오류 경로라 무시한다.",
      "정책 안은 무시, 정책 밖은 맥락을 붙여 올린다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def event(y, title, sub, c):
    d.tone(24, y - 32, 240, 64, c, 6, "12", 1.2)
    d.t(144, y - 4, title, 13, c, MONO, "middle", 600)
    d.t(144, y + 18, sub, 13, MUTED, kr(sub))


def diamond(cx, cy, label, c):
    pts = f"{cx-68},{cy} {cx},{cy-44} {cx+68},{cy} {cx},{cy+44}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 5, label, 13, INK, KR, "middle", 600)


def result(x, y, w, title, sub, c, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y - 32}" width="{w}" height="64" rx="6" fill="{c}1F" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.tone(x, y - 32, w, 64, c, 6, "12", 1.2)
    d.t(x + w / 2, y - 4, title, 13, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 18, sub, 13, MUTED, kr(sub))


ROWS = ((168, OK), (288, BAD), (408, INFO))
event(168, "write", "/home/<user>/<file>", OK)
event(288, "write", "/etc/passwd", BAD)
event(408, "경보 전송", "디스크 가득 → 네트워크", INFO)

for y, c in ROWS:
    mk = {OK: "ok", BAD: "bad", INFO: "info"}[c]
    d.arrow([(268, y), (306, y)], c, mk, 1.5)
    diamond(380, y, "정책 안?", c)

# 분기 라벨 — 마름모 오른쪽 꼭짓점에서 결과까지
d.arrow([(450, 168), (554, 168)], OK, "ok", 1.5)
d.chip(502, 150, "예", OK, 13)
d.arrow([(450, 288), (554, 288)], BAD, "bad", 1.5)
d.chip(502, 270, "아니오", BAD, 13)
d.arrow([(450, 408), (554, 408)], INFO, "info", 1.5)
d.chip(502, 390, "예", INFO, 13)

# 결과
result(560, 168, 192, "무시", "이벤트 없음", OK)
result(560, 288, 192, "보안 이벤트", "프로세스 · 컨테이너 · Pod", ACC, True)
result(560, 408, 192, "무시", "예상된 오류 경로", INFO)

# 이벤트 → SIEM · 사람
d.arrow([(756, 288), (782, 288)], ACC, "acc", 1.6)
d.tone(788, 256, 148, 64, BAD, 6, "12", 1.2)
d.t(862, 284, "SIEM", 13, BAD, MONO, "middle", 600)
d.t(862, 306, "사람 경보", 13, MUTED, KR)

d.legend(H - 56, [("정책 안", OK), ("정책 밖", BAD), ("오류 경로", INFO), ("맥락이 붙은 이벤트", ACC)])
d.save("09-01.policy-decision.svg")
