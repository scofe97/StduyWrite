# 07-03 §4 — 서버를 믿는 걸음과 나를 증명하는 걸음은 다르다.
# 원문("SSH"): "SSH is a cryptographic network protocol to securely provide network services over an
#       insecure network." 저자의 팁 다섯은 전부 클라이언트 쪽 이야기다 — 비밀번호 인증 끄기,
#       "users create key pairs and provide you with their public key, which you add to
#       ~/.ssh/authorized_keys", ssh -tt, TERM=xterm, ServerAliveInterval, -v/-vvv.
# 노트의 읽기: 인증은 양방향인데 원서에는 *서버가 자기를 증명하는 축* 이 없다. known_hosts·호스트 키·
#       TOFU 가 노트에 0건이라 2026-09-07 학습 세션에서 학습자가 이 도식을 직접 요청했다.
#   RFC 4251 §4.1 — "The server host key is used during key exchange to verify that the client is
#       really talking to the correct server. For this to be possible, the client must have a priori
#       knowledge of the server's public host key."
#       TOFU 전략 — "only accept a host key without checking the first time a host is connected, save
#       the key in a local database, and compare against that key on all future connections to that host."
#       대가 — "The connection still provides protection against passive listening; however, it becomes
#       vulnerable to active man-in-the-middle attacks."
#       (RFC 는 'TOFU' 라는 이름을 쓰지 않는다. 전략만 서술한다.)
# 타입 스펙: type-sequence — 시간축 위의 주고받음. 참여자 3(상한 5), 메시지 9(상한 12),
#       프래그먼트 1(상한 1, opt). 반환은 점선 + 채운 마커. coral 은 하나뿐이며 첫 접속에만 있는
#       그 한 걸음이다. 두 인증 축은 칩이 아니라 *색* 이 나르고 범례가 그 뜻을 적는다 —
#       레인 셋뿐이라 여백이 좁아 라벨을 더 얹으면 레인 위에 앉는다.
#       축약: 키 교환의 암호학적 절차는 RFC 4253 의 몫이라 "세션 키 합의" 한 줄로 뭉쳤다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, KR, MONO

W, H = 880, 830
d = Seq(W, H, "LEARNING MODERN LINUX · 07-03 §4",
        "서버를 믿는 걸음과 나를 증명하는 걸음은 다르다",
        "SSH 접속 한 번에 인증이 두 번 일어난다. 서버가 호스트 키로 자기를 증명하고, "
        "그다음에 내가 공개키로 나를 증명한다. 저자는 뒤의 것만 적는다.",
        "첫 접속의 그 한 걸음이 이 방식의 값이자 구멍입니다")

USER, CLI, SRV = "사용자", "ssh 클라이언트", "sshd 서버"
LX = d.lanes([(USER, "터미널 앞"), (CLI, "~/.ssh"), (SRV, "원격 22번")],
             y0=104, lane_w=230)

# ── 서버가 자기를 증명하는 구간 (OK) ────────────────────────────────
d.msg(USER, CLI, "ssh db", 196, MUTED, sub="접속을 시작한다")
d.msg(CLI, SRV, "TCP 22 · 버전 교환", 240, MUTED)
d.msg(SRV, CLI, "호스트 키 제시", 284, OK, mk="ok", dash="5 4",
      sub="서버가 자기를 증명한다")
d.selfmsg(CLI, "known_hosts 대조", 330, OK, sub="적힌 키와 같은가")

# ── opt: 처음 보는 호스트라면 (coral 하나) ──────────────────────────
FX0, FX1 = LX[USER] - 96, LX[CLI] + 96
FY0, FY1 = 366, 498
d.box(FX0, FY0, FX1 - FX0, FY1 - FY0, "rgba(245,245,245,0.04)", "rgba(245,245,245,0.22)", 1, 4)
d.box(FX0, FY0, 44, 16, PAPER, "rgba(245,245,245,0.22)", 1, 2)
d.t(FX0 + 22, FY0 + 12, "OPT", 11, MUTED, MONO)
d.t(FX0 + 12, FY0 + 36, "[처음 보는 호스트]", 11, MUTED, MONO, "start")

d.msg(CLI, USER, "지문 이대로 맞습니까", 424, MUTED, dash="5 4")
d.msg(USER, CLI, "yes", 470, ACC, sub="known_hosts 에 한 줄이 적힌다")

# ── 내가 나를 증명하는 구간 (INFO) ──────────────────────────────────
d.msg(CLI, SRV, "세션 키 합의", 540, MUTED, sub="여기부터 암호화된다")
d.msg(CLI, SRV, "공개키로 서명해 보인다", 590, INFO, mk="info",
      sub="내가 나를 증명한다")
d.msg(SRV, CLI, "인증 성공 · 셸을 연다", 640, INFO, mk="info", dash="5 4")

d.rails(672)

d.tone(24, 690, W - 48, 74, ACC)
d.t(44, 716, "취약한 구간은 첫 접속 한 번뿐입니다", 13, INK, KR, "start", 600)
d.t(44, 738, "그 한 번에 가짜 서버가 끼어들면 그 뒤의 모든 접속이 가짜 키를 믿습니다. "
             "수동적인 엿듣기는 막지만", 12, MUTED, KR, "start")
d.t(44, 756, "능동적인 중간자 공격에는 취약하다고 RFC 4251 이 적습니다.", 12, MUTED, KR, "start")

d.legend(774, [("서버가 자기를 증명한다", OK), ("내가 나를 증명한다", INFO),
               ("첫 접속에만 있는 걸음", ACC)])
d.save("07-03.ssh-handshake.svg")
print("ok 07-03.ssh-handshake")
