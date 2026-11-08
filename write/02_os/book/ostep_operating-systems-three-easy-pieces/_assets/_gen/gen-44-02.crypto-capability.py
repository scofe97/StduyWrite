# 44-02 §4 — 서명한 capability 를 자원 쪽이 공개 키로 검증한다. 권한 칸을 read 에서 write 로 고치면 같은 서명으로는 검증이 실패한다.
# 본문 근거: 이 노트 §4 「서명한 capability」의 소절 「공개 키로 만드는 capability」.
# 검증 근거: 2026-11-08 OpenSSL 3.6.4. RSA 2048 개인 키로 `user=alice;res=report.pdf;rights=read;exp=1893456000` 에 SHA-256 서명(서명 파일 256바이트),
#            공개 키로 검증하면 `Verified OK`, rights 를 write 로 바꾼 내용에 같은 서명을 검증하면 `Verification failure`(정답 6).
# 타입 스펙: type-sequence — 참여자 셋(자원 관리자 · alice · 자원)의 시간순 메시지. 점선은 응답, 틀로 정상 사용과 위조 시도를 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, BAD, KR, MONO

W, H = 880, 608
LW, LH, LY = 216, 44, 96
X_ADM, X_ALI, X_RES = 156, 440, 724
LANES = ((X_ADM, "자원 관리자", "개인 키 보유"), (X_ALI, "alice", "capability 소지자"), (X_RES, "자원", "공개 키 보유"))
d = D(W, H, "OSTEP · 44-02 §4",
      "권한 칸을 고치면 같은 서명은 검증에 실패한다",
      "자원 관리자가 alice 에게 읽기 권한을 담은 capability 를 개인 키로 서명해 발급한다. alice 가 그대로 자원에 내면 공개 키 검증이 Verified OK 로 통과해 읽기가 허용된다. "
      "alice 가 rights 를 write 로 고쳐 같은 서명과 함께 내면 Verification failure 가 나와 거부된다. 자원은 서명만 검증하므로 사용자별 접근 목록을 기억하지 않는다.",
      "자원은 서명만 확인하고, alice 는 개인 키가 없어 새 서명을 만들 수 없다")


def msg(x1, x2, y, label, c=MUTED, mk="ar", dash=None, subs=(), mono_sub=True):
    sgn = 1 if x2 > x1 else -1
    d.arrow([(x1 + 10 * sgn, y), (x2 - 12 * sgn, y)], c, mk, 1.5, dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c if c != MUTED else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t((x1 + x2) / 2, y + 18 + i * 16, s, 12, MUTED, MONO if mono_sub else KR)


def frame(y1, y2, name):
    d.o.append(f'<rect x="24" y="{y1}" width="832" height="{y2 - y1}" rx="4" fill="{INK}08" stroke="{SOFT}" stroke-width="0.9"/>')
    d.o.append(f'<rect x="24" y="{y1}" width="84" height="22" rx="2" fill="#0D1117" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(66, y1 + 16, name, 12, MUTED, KR, "middle", 600)


# 참여자
for x, name, sub in LANES:
    d.box(x - LW / 2, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x, LY + 20, name, 13, INK, KR if any("가" <= c <= "힣" for c in name) else MONO, "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, KR)
    d.line(x, LY + LH + 6, x, H - 24, RULE, 1.0, "3 6")

# 발급
msg(X_ADM, X_ALI, 192, "발급 · 개인 키로 서명", INK, "ar", None,
    ("user=alice;res=report.pdf;", "rights=read;exp=1893456000"))
d.t((X_ADM + X_ALI) / 2, 242, "+ 서명 256바이트", 12, MUTED, KR)

# 정상 사용
frame(262, 404, "정상 사용")
msg(X_ALI, X_RES, 308, "제시 · 내용과 서명", MUTED, "ar", None, ("같은 내용 · 같은 서명",), False)
d.chip(X_RES, 348, "Verified OK", OK, 12, 8)
msg(X_RES, X_ALI, 390, "read 허용", OK, "ok", "5 4")

# 위조 시도
frame(420, 592, "위조 시도")
d.chip(X_ALI, 454, "rights=write 로 고침", ACC, 12, 8)
msg(X_ALI, X_RES, 504, "제시 · 고친 내용과 원래 서명", ACC, "acc", None)
d.chip(X_RES, 526, "Verification failure", BAD, 12, 8)
msg(X_RES, X_ALI, 568, "거부", BAD, "bad", "5 4")

d.save("44-02.crypto-capability.svg")
