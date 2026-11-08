# 45-02 §5 — 같은 비밀로도 도전값마다 응답이 달라서, 지난 도전의 응답을 새 도전값에 다시 보내면 거부된다. 도전값과 응답은 암호화하지 않아도 된다.
# 본문 근거: 이 노트 §5 「비밀번호와 공개 키 밖의 인증」의 소절 「도전 응답은 매번 다른 도전값으로 재사용을 막는다」.
# 검증 근거: 2026-11-08 Python 3.14.4 로 응답 = HMAC-SHA256(비밀, 도전값)의 앞 16자리를 계산했다. 시연용 비밀은 bytes(range(32)) 로 고정했다(정답 5 의 실험은 매번 새 무작위 비밀을 쓴다).
#            도전값 7731 의 응답은 87d61ab60ff4273f, 도전값 9042 의 응답은 7e79121912351cb7 이고, 9042 에 87d61ab60ff4273f 를 보내면 REJECT 다.
# 타입 스펙: type-sequence — 참여자 둘(확인하는 쪽 · 증명하는 쪽)의 시간순 메시지. 틀로 지난 도전, 새 도전의 올바른 응답, 지난 응답 재사용을 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, BAD, KR, MONO

W, H = 880, 652
LW, LH, LY = 216, 44, 96
X_V, X_P = 156, 724
d = D(W, H, "OSTEP · 45-02 §5",
      "새 도전값에는 지난 응답이 통하지 않는다",
      "확인하는 쪽이 도전값 7731 을 보내면 증명하는 쪽이 비밀로 계산한 응답 87d61ab60ff4273f 를 돌려준다. 새 연결에서 도전값 9042 를 보내면 올바른 응답은 7e79121912351cb7 이고 확인하는 쪽이 같은 계산으로 비교해 ACCEPT 한다. "
      "도청한 쪽이 지난 응답 87d61ab60ff4273f 를 9042 에 다시 보내면 REJECT 된다. 응답은 비밀을 드러내지 않으므로 도전값과 응답을 암호화하지 않아도 된다.",
      "도전값과 응답은 암호화 없이 보내도 되고, 비밀은 미리 나눠 갖고 있어야 한다")


def msg(x1, x2, y, label, c=INK, mk="ar", dash=None, sub=None):
    sgn = 1 if x2 > x1 else -1
    d.arrow([(x1 + 10 * sgn, y), (x2 - 12 * sgn, y)], c, mk, 1.5, dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, KR if any("가" <= ch <= "힣" for ch in label) else MONO, "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 18, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def frame(y1, y2, name, w=96):
    d.o.append(f'<rect x="24" y="{y1}" width="832" height="{y2 - y1}" rx="4" fill="{INK}08" stroke="{SOFT}" stroke-width="0.9"/>')
    d.o.append(f'<rect x="24" y="{y1}" width="{w}" height="22" rx="2" fill="#0D1117" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(24 + w / 2, y1 + 16, name, 12, MUTED, KR, "middle", 600)


for x, name, sub in ((X_V, "확인하는 쪽", "비밀을 알고 있음"), (X_P, "증명하는 쪽", "같은 비밀을 가짐")):
    d.box(x - LW / 2, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x, LY + 20, name, 13, INK, KR, "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, KR)
    d.line(x, LY + LH + 6, x, H - 24, RULE, 1.0, "3 6")

# 지난 도전
frame(160, 304, "지난 도전")
msg(X_V, X_P, 208, "도전값 7731", INK, "ar", None)
msg(X_P, X_V, 268, "응답 87d61ab60ff4273f", MUTED, "ar", "5 4", "HMAC-SHA256(비밀, 7731) 의 앞 16자")

# 새 도전
frame(320, 500, "새 도전", 72)
msg(X_V, X_P, 368, "도전값 9042", INK, "ar", None)
msg(X_P, X_V, 428, "응답 7e79121912351cb7", OK, "ok", "5 4")
d.chip(X_V, 476, "같은 계산으로 비교 → ACCEPT", OK, 12, 8)

# 지난 응답 재사용
frame(516, 636, "재사용 시도", 108)
msg(X_P, X_V, 568, "9042 에 지난 응답 87d61ab60ff4273f", ACC, "acc", "5 4")
d.chip(X_V, 612, "REJECT", BAD, 12, 8)

d.save("45-02.challenge-response.svg")
