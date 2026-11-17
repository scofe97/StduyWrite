# 09-01 §5 「pam_limits — 로그인할 때 거는 자원 한도」 — limits 파일을 읽는 순서와 이기는 줄.
# 1차 자료 pam_limits(8): limits.conf 다음 limits.d/*.conf 를 "C" 로케일 순서로 읽고, 효과는 그 순서로 이어 붙인 것과 같다.
#       limits.conf(5): "In general, individual limits have priority over group limits" ·
#       "group and wildcard limits are not applied to the root user" · "all limit settings are set per login".
# 실측(debian:12, libpam-modules 1.5.2): 10-a.conf "alice soft nofile 2048" + 20-b.conf "* soft nofile 4096"
#       → su alice -c 'ulimit -Sn' = 2048. 파일을 바꾸기 전에 띄운 alice 의 sleep 은 /proc/PID/limits 1024 그대로.
# 주의: 예전 판의 "Debian 12 기본 limits.conf 는 전부 주석" 은 본문에 없는 실측이라 그 띠의 값을 뺐다.
# 타입 스펙: type-data-flow — su 가 PAM 세션을 열고(/etc/pam.d/su), pam_limits 가 파일 셋을 이름순으로 읽어
#           이기는 줄 하나를 골라 alice 셸의 한도로 거는 흐름. 오른쪽 칸은 같은 흐름을 거치지 않아
#           limits.conf 가 닿지 않는 세 프로세스와 그 실측값이다. accent 는 이기는 줄 하나.
# 근거: 본문 §5 — Debian 12 의 /etc/pam.d/su 등록, C 로케일 이름순, 우선순위 규칙 셋, 표 둘째 줄
#       (10-a alice 2048 + 20-b * 4096 → 2048), sleep 의 /proc/PID/limits 1024 1048576, docker exec 20480,
#       systemctl show 의 LimitNOFILE=1048576 · LimitNOFILESoft=1024, 표 넷째·다섯째 줄(root).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 656
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §5",
      "같은 nofile 을 두 파일이 말하면 사용자 줄이 이긴다",
      "su alice 가 PAM 세션을 열면 /etc/pam.d/su 에 등록된 pam_limits 가 limits.conf, limits.d/10-a.conf, "
      "limits.d/20-b.conf 를 이름순으로 읽는다. 나중에 읽힌 * soft nofile 4096 보다 사용자 줄 alice soft "
      "nofile 2048 이 이겨 alice 셸의 ulimit -Sn 이 2048 이 된다. systemd 서비스, docker exec 셸, 고치기 "
      "전에 띄운 sleep 은 이 흐름을 거치지 않아 각자의 값을 유지한다.",
      "나중에 읽힌 * 줄도 alice 를 지목한 줄을 못 이깁니다")

L0, L1 = 24, 572              # 로그인 흐름
R0, R1 = 604, 856             # PAM 밖
CX = 300                      # 흐름 화살표 x

d.t(L0, 102, "로그인 · su 세션", 12, SOFT, KR, "start")
d.t(R0, 102, "PAM 세션을 안 여는 길", 12, WARN, KR, "start")

# 선 먼저
d.arrow([(CX, 156), (CX, 176)], MUTED, "ar", 1.3)
d.arrow([(CX, 220), (CX, 240)], MUTED, "ar", 1.3)
d.arrow([(CX, 464), (CX, 484)], OK, "ok", 1.3)

# 1. su
d.box(L0, 116, L1 - L0, 40, PAPER2, RULE, 1.0, 6)
d.t(L0 + 16, 141, "su alice -c 'ulimit -Sn'", 12, INK, MONO, "start", 600)
d.t(L1 - 16, 141, "PAM 세션 열기", 12, MUTED, KR, "end")
# 2. /etc/pam.d/su
d.box(L0, 180, L1 - L0, 40, PAPER2, RULE, 1.0, 6)
d.t(L0 + 16, 205, "/etc/pam.d/su", 12, INK, MONO, "start", 600)
d.t(L0 + 136, 205, "session required pam_limits.so", 12, MUTED, MONO, "start")

# 3. pam_limits 가 읽는 파일
d.box(L0, 244, L1 - L0, 220, PAPER, INFO, 1.1, 8)
d.t(L0 + 16, 266, "pam_limits", 13, INFO, MONO, "start", 600)
d.t(L0 + 112, 266, "C 로케일 이름순으로 읽음", 12, MUTED, KR, "start")
files = [("1", "/etc/security/limits.conf", "", "먼저"),
         ("2", "limits.d/10-a.conf", "alice soft nofile 2048", "사용자 줄"),
         ("3", "limits.d/20-b.conf", "*     soft nofile 4096", "* 줄 · 나중")]
for i, (n, f, line, note) in enumerate(files):
    y = 280 + i * 40
    d.box(L0 + 16, y, L1 - L0 - 32, 32, PAPER2, RULE, 0.9, 4)
    d.t(L0 + 30, y + 21, n, 12, SOFT, MONO, "start", 600)
    d.t(L0 + 50, y + 21, f, 12, INK, MONO, "start")
    if line:
        d.t(L0 + 222, y + 21, line, 12, INK, MONO, "start")
    d.t(L1 - 30, y + 21, note, 12, MUTED, KR, "end")
d.tone(L0 + 16, 408, L1 - L0 - 32, 40, ACC, 6, "16", 1.4)
d.t(L0 + 30, 433, "→", 13, ACC, MONO, "start", 600)
d.t(L0 + 50, 433, "alice soft nofile 2048", 13, ACC, MONO, "start", 600)
d.t(L1 - 30, 433, "사용자 줄 > * · 같으면 나중 줄", 12, ACC, KR, "end")

# 4. 결과
d.tone(L0, 488, L1 - L0, 40, OK, 6, "12", 1.2)
d.t(L0 + 16, 513, "alice 셸", 12, OK, KR, "start", 600)
d.t(L0 + 90, 513, "ulimit -Sn → 2048", 12, INK, MONO, "start")
d.t(L1 - 16, 513, "세션마다 · 소급 안 됨", 12, MUTED, KR, "end")

# PAM 밖
outs = [(116, 92, "systemd 서비스", "PAMName= 없음", ["LimitNOFILESoft=1024", "LimitNOFILE=1048576"]),
        (224, 72, "docker exec 셸", "PAM 안 거침", ["nofile 20480"]),
        (312, 92, "고치기 전에 띄운 sleep", "/proc/PID/limits", ["Max open files", "1024  1048576"])]
for y, h, name, sub, vals in outs:
    d.o.append(f'<rect x="{R0}" y="{y}" width="{R1 - R0}" height="{h}" rx="6" fill="{WARN}0D" '
               f'stroke="{WARN}" stroke-width="1" stroke-dasharray="5 4"/>')
    d.t(R0 + 14, y + 22, name, 12, WARN, KR, "start", 600)
    d.t(R0 + 14, y + 42, sub, 12, MUTED, MONO if sub.isascii() else KR, "start")
    for j, v in enumerate(vals):
        d.t(R0 + 14, y + 62 + j * 18, v, 12, INK, MONO, "start")
d.t(R0, 432, "limits.conf 가 닿지 않음", 12, WARN, KR, "start")
d.t(R0, 452, "서비스는 유닛의 Limit*= 로", 12, MUTED, KR, "start")

d.t(L0, 564, "root 는 * 줄을 안 받음 · * - nofile 5000 → root 그대로 · root - nofile 6000 → 6000",
    11, SOFT, KR, "start")
d.legend(588, [("읽는 파일", INFO), ("이기는 줄", ACC), ("걸린 한도", OK), ("PAM 밖", WARN)])
d.save("09-01.pam-limits.svg")
print("ok 09-01.pam-limits")
