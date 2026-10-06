# 타입 스펙: type-state
# 07-01 소켓 파일 생애주기와 정리 방식
# 사실 출처: NPG Ch.7 p.3-4, 6-7, 10 (net.Listen/ListenUnix vs net.ListenPacket, os.Chmod, os.Remove)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, SOFT, RULE, OK, ACC, INFO, KR, MONO

W, H = 880, 420
d = D(W, H, "NPG CH.7 — SOCKET FILE LIFECYCLE",
      "소켓 파일 생애주기와 정리 방식",
      "리스너 바인딩부터 권한 설정 및 종료 시 파일 삭제 경로",
      "Listen 계열의 자동 언링크와 ListenPacket 의 직접 삭제 갈래")

def draw_state(x, y, w, h, name, sub=None, c=INFO, focal=False):
    fill = f"{c}15" if focal else PAPER2
    stroke = c if focal else RULE
    sw = 1.6 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=8)
    d.t(x + w / 2, y + (h / 2 + 5 if not sub else h / 2 - 2), name, 13, INK if not focal else c, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + h / 2 + 13, sub, 11, SOFT, KR if any('가'<=ch<='힣' for ch in sub) else MONO, "middle")

# 시작 점
d.o.append(f'<circle cx="36" cy="196" r="6" fill="{INK}"/>')
d.t(36, 222, "시작", 11, SOFT, KR, "middle")

# 시작 -> 소켓 파일 생성 (간격 76px)
d.arrow([(42, 196), (118, 196)], c=INFO, m="info")
d.t(80, 184, "Listen*", 10, INFO, MONO, "middle", 600)

# 상태 1: 소켓 생성
draw_state(118, 168, 124, 56, "소켓 파일 생성", "ModeSocket", INFO)

# 소켓 생성 -> 권한 설정 (간격 78px)
d.arrow([(242, 196), (320, 196)], c=INFO, m="info")
d.t(281, 184, "os.Chmod", 10, INFO, MONO, "middle", 600)

# 상태 2: 권한 완료
draw_state(320, 168, 124, 56, "권한 설정 완료", "0666 / 0622", INFO)

# 갈래 1 (상단): net.Listen / net.ListenUnix (UnlinkOnClose: true)
d.arrow([(444, 184), (480, 184), (480, 132), (620, 132)], c=OK, m="ok")
d.t(550, 120, "Listen.Close()", 10, OK, MONO, "middle", 600)

draw_state(620, 104, 136, 56, "자동 언링크", "UnlinkOnClose", OK)

d.arrow([(756, 132), (824, 132)], c=OK, m="ok")
d.t(790, 120, "정리", 11, OK, KR, "middle")

# 상단 종료 링
d.o.append(f'<circle cx="836" cy="132" r="8" fill="none" stroke="{OK}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="836" cy="132" r="4" fill="{OK}"/>')
d.t(836, 158, "소켓 제거", 11, SOFT, KR, "middle")

# 갈래 2 (하단): net.ListenPacket (unixgram)
d.arrow([(444, 208), (480, 208), (480, 260), (620, 260)], c=ACC, m="acc")
d.t(550, 248, "ListenPacket.Close()", 10, ACC, MONO, "middle", 600)

draw_state(620, 232, 136, 56, "소켓 파일 잔존", "언링크 미지원", ACC, focal=True)

d.arrow([(756, 260), (824, 260)], c=ACC, m="acc")
d.t(790, 248, "os.Remove", 10, ACC, MONO, "middle", 600)

# 하단 종료 링
d.o.append(f'<circle cx="836" cy="260" r="8" fill="none" stroke="{ACC}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="836" cy="260" r="4" fill="{ACC}"/>')
d.t(836, 286, "수동 제거", 11, SOFT, KR, "middle")

# 범례
d.legend(360, [("공통 생애주기", INFO), ("자동 언링크", OK), ("직접 파일 삭제", ACC)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07-01.socket-file-life.svg"))
d.save(out)
print(f"saved: {out}")
