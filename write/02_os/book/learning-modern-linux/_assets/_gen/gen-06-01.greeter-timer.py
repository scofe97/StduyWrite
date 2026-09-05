# 06-01 §6 — 단위 파일 둘이 저널 로그 한 줄이 되기까지.
# 원문("Example: scheduling greeter"): "let's assume we want to launch our greeter app every hour.
#       First, we define a systemd unit file of type service. ... Next, we define a timer unit to launch
#       the greeter service every hour. ... Now we copy both unit files to /run/systemd/system so that
#       systemd recognizes them. ... We're now in a position to use the greeter timer, since systemd
#       automatically picked it up when we copied it into the respective directory."
#       상태 출력 — "Active: active (waiting) since Sun 2021-09-12 13:10:35 IST; 2s ago",
#                   "Trigger: Sun 2021-09-12 14:00:00 IST; 49min left".
#       로그 출력 — "Sep 12 14:00:01 starlite systemd[1]: Starting My Greeting Service...",
#                   "Sep 12 14:00:01 starlite greeter.sh[21071]: You are awesome!"
#       저자 노트 — "the stdout output is going directly to the logs".
# 타입 스펙: type-sequence — 시간축 위의 주고받음. accent 는 로그에 찍힌 [1], 곧 앞 절의 PID 1 이
#           지금 도는 타이머와 이어지는 자리. 축약: 배포판별 enable/start 차이는 주석 띠로 뺐다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 648
d = Seq(W, H, "LEARNING MODERN LINUX · 06-01 §6",
        "단위 파일 둘이 로그 한 줄이 되기까지",
        "타이머 단위가 서비스 단위를 부르고, 서비스가 셸 스크립트를 돌리고, 그 표준 출력이 "
        "그대로 저널에 남는다.",
        "로그의 systemd[1] 이 부팅 넷째 단계의 그 PID 1 입니다")

d.lanes([("나", "셸"), ("systemd", "PID 1"),
         ("greeter.sh", "oneshot"), ("저널", "journald")], y0=116, lane_w=190)

d.msg("나", "systemd", "cp 단위파일 → /run/systemd/system/", 184, INFO,
      sub="복사만 하면 systemd 가 알아서 집어 든다")
d.state("systemd", "greeter.timer — active (waiting)", 226, INFO)
d.selfmsg("systemd", "OnCalendar=hourly — 다음 발동까지 49분", 268, MUTED)
d.msg("systemd", "greeter.sh", "Type=oneshot · ExecStart", 312, ACC, mk="acc",
      sub="Starting My Greeting Service...")
d.msg("greeter.sh", "저널", "printf 의 표준 출력", 368, OK, mk="ok",
      sub="You are awesome!")
d.state("저널", "greeter.sh[21071]", 412, OK)
d.msg("저널", "나", "journalctl -f -u greeter.service", 460, INFO, mk="info")

d.rails(492)

d.tone(24, 508, W - 48, 62, ACC)
d.t(44, 536, "배포판이 여기에서 갈립니다", 12.5, INK, KR, "start", 600)
d.t(44, 558, "Debian 계열은 service 단위를 기본으로 활성화하고 시작하지만, "
             "Red Hat 계열은 명시적인 systemctl start 와 enable 을 요구합니다.",
    11.5, MUTED, KR, "start")

d.legend(586, [("사람이 하는 일", INFO), ("systemd 가 앱을 부르는 자리", ACC),
               ("표준 출력이 로그가 되는 길", OK)])
d.save("06-01.greeter-timer.svg")
print("ok 06-01.greeter-timer")
