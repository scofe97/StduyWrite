# 06-03 §6 — PreStop hook 과 SIGTERM 의 실행 순서
# 본문: "컨테이너에 PreStop hook 이 설정돼 있으면 쿠버네티스가 hook 을 먼저 실행하고, 완료될 때까지 SIGTERM 전송을 미룹니다."
#       "busybox 실측(sleep 2): 06:31:03 pre-stop hook 실행 → 2초 뒤 06:31:05 SIGTERM 받음"
#       "hook 실행 중 프로세스가 이미 종료되면 SIGTERM 미전송 · hook 실패해도 종료 진행"
# 타입 스펙: type-sequence.md — kubectl · kubelet · PreStop hook · 메인 프로세스 네 참여자 사이의
#           시간순 메시지 교환과 유예 시간 만료 여부의 alt 분기 프레임.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, RULE, KR, MONO
import ddx

d = Seq(1000, 728, "KUBERNETES IN ACTION · 06-03",
        "PreStop 이 끝날 때까지 SIGTERM 전송을 미룬다",
        "kubectl delete pod 가 오면 deletionGracePeriodSeconds(기본 30s) 카운트가 시작되고, "
        "kubelet 은 PreStop hook(예: sleep 2)이 끝난 뒤에야 메인 프로세스에 SIGTERM(15)을 보낸다.",
        "busybox 실측: 06:31:03 preStop(sleep 2) → 06:31:05 SIGTERM (2초 뒤 도착)")

ddx.lanes(d, [("kubectl / API", "삭제 요청"),
              ("kubelet", "종료 절차 관리"),
              ("PreStop hook", "exec · httpGet · sleep"),
              ("메인 프로세스", "컨테이너 PID 1")], y0=104, lane_w=192)
d.rails(612)

# 메시지 1: delete pod (t=0s)
ddx.msg(d, "kubectl / API", "kubelet", "kubectl delete pod", 184, ACC, mk="acc")
d.t((d.LX["kubectl / API"] + d.LX["kubelet"]) / 2, 202, "06:31:03 · 종료 시작", 11, MUTED, KR)

# kubelet 상태: grace period 시작
ddx.state(d, "kubelet", "유예 시간 30s 카운트 시작", 236, WARN)

# 메시지 2: kubelet -> PreStop
ddx.msg(d, "kubelet", "PreStop hook", "preStop 실행", 280, INFO, mk="info")
d.t((d.LX["kubelet"] + d.LX["PreStop hook"]) / 2, 298, "sleep 2", 11, MUTED, MONO)

# PreStop 대기
ddx.selfmsg(d, "PreStop hook", "sleep 2 완료 대기", 332, INFO)

# 리턴 메시지 (dashed + filled marker per type-sequence)
ddx.msg(d, "PreStop hook", "kubelet", "hook 종료 (성공·실패 무관)", 376, MUTED, mk="ar", dash="6 4")

# 메시지 3: kubelet -> 메인 프로세스 SIGTERM (라벨은 PreStop~메인 사이에 배치해 lifeline 겹침 방지)
x_kub, x_main = d.LX["kubelet"], d.LX["메인 프로세스"]
x_gap_mid = (d.LX["PreStop hook"] + x_main) / 2
d.path(f"M {x_kub+10} 428 L {x_main-12} 428", ACC, 1.6, m="acc")
d.t(x_gap_mid, 419, "SIGTERM (15)", 11, ACC, MONO, "middle", 600)
d.t(x_gap_mid, 446, "06:31:05 · 2초 뒤 도착", 11, MUTED, KR)

# ALT combined fragment spanning kubelet .. 메인 프로세스
FX = d.LX["kubelet"] - 24
FW = (d.LX["메인 프로세스"] + 24) - FX
FY, FH = 468, 136
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" '
           f'fill="{INK}08" stroke="{INK}38" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="44" height="18" rx="2" '
           f'fill="{PAPER}" stroke="{INK}38" stroke-width="1"/>')
d.t(FX + 22, FY + 13, "ALT", 8, MUTED, MONO, "middle", 600)

# Region 1: 정상 정리
d.t(FX + 56, FY + 14, "[남은 유예 시간 내 정리 완료]", 11, OK, KR, "start")
d.path(f"M {x_main-10} 516 L {x_kub+12} 516", OK, 1.5, m="ok", dash="6 4")
d.t(x_gap_mid, 507, "exit 0 (정상 종료)", 11, OK, KR, "middle", 600)

# Divider
d.line(FX + 8, 536, FX + FW - 8, 536, RULE, 1.0, "4 3")

# Region 2: 유예 만료 (kubelet lifeline=FX+24 오른쪽에 배치)
d.t(FX + 36, 554, "[30s 만료 · PID 1 미응답 등]", 11, BAD, KR, "start")
d.path(f"M {x_kub+10} 584 L {x_main-12} 584", BAD, 1.5, m="bad")
d.t(x_gap_mid, 575, "SIGKILL (9) · 코드 137", 11, BAD, MONO, "middle", 600)

d.t(24, 640, "hook 실행 중 프로세스 종료 시 SIGTERM 미전송 · hook 실패 시 FailedPreStopHook 후 종료 진행",
     12, MUTED, KR, "start")
d.legend(672, [("삭제 · SIGTERM", ACC), ("유예 카운트", WARN), ("PreStop 실행", INFO),
               ("정상 종료", OK), ("강제 종료", BAD)])
d.save("06-03-prestop-sigterm-sequence.svg")
print("ok prestop-sigterm-sequence")
