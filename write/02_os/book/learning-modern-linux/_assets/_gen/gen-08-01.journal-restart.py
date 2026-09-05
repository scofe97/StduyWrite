# 08-01 §7 — 서비스 하나를 재시작할 때 저널에 남는 순서.
# 원문("journalctl"): "in one terminal we restart the service using systemctl restart apparmor, and in
#       another we execute the following command" 뒤의 `journalctl -f -u apparmor.service` 출력.
#       남은 줄은 "-- Logs begin at Sun 2021-01-24 14:36:30 GMT. --",
#       "Sep 26 17:10:02 starlite apparmor[13883]: All profile caches have been cleared, but no profiles
#       have been unload", "... Unloading profiles will leave all running processes permanently",
#       "Sep 26 17:10:02 starlite systemd[1]: Stopped AppArmor initialization.",
#       "Sep 26 17:10:02 starlite systemd[1]: Starting AppArmor initialization...",
#       "Sep 26 17:10:02 starlite apparmor[13904]: * Starting AppArmor profiles",
#       "Sep 26 17:10:03 starlite apparmor[13904]: Skipping profile in /etc/apparmor.d/disable: usr.sbin.rsy",
#       "Sep 26 17:10:09 starlite apparmor[13904]: ...done.",
#       "Sep 26 17:10:09 starlite systemd[1]: Started AppArmor initialization."
#       저자가 붙인 주석은 "After systemd has stopped the service, here it comes back up again" 이다.
# 주의: PID 가 13883 에서 13904 로 바뀌는 것은 출력에 그대로 있는 사실이고, 그것이 재시작의 증거다.
#       첫 메시지 라벨이 cle 에서 끊긴 것은 원서 지면이 자른 자리다. 본문이 그 절단을 보존하므로
#       도식도 채우지 않는다. 채우면 같은 노트 안에서 본문과 도식이 어긋난다.
#       원문 출력은 편집됐다고 밝혀져 있어 Skipping profile 줄은 이 도식에서 생략했다.
# 타입 스펙: type-sequence — 주체 넷 사이의 시간순 메시지. 같은 초 안에 여러 줄이 오고 마지막 두 줄만
#           7초 뒤라는 것이 이 그림에서만 보인다. 축약: 원문의 편집된 줄임표 줄은 담지 않았다.
import sys; sys.path.insert(0, ".")
from dd import Seq, D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        kr = any("가" <= ch <= "힣" for ch in str(txt))
        w = len(txt) * (11.0 if kr else 7.0) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, KR if kr else MONO)


W, H = 880, 640
d = SeqKR(W, H, "LEARNING MODERN LINUX · 08-01 §7",
          "재시작 한 번이 저널에 남기는 순서",
          "원서가 두 터미널로 나눠 보인 장면을 한 그림으로 세운 것. 왼쪽에서 명령을 치면 오른쪽 터미널의 "
          "journalctl -f 에 두 주체의 줄이 섞여 흐른다.",
          "타임스탬프를 보면 마지막 두 줄만 7초 뒤입니다")

d.lanes([("터미널 1", "systemctl"), ("systemd", "PID 1"),
         ("apparmor.service", "유닛"), ("터미널 2", "journalctl -f -u")], 108, 190)
d.rails(520)

d.state("apparmor.service", "PID 13883", 176, INFO)
d.msg("터미널 1", "systemd", "systemctl restart apparmor", 216, INK,
      sub="유닛 하나만 다시 올린다")
d.msg("systemd", "apparmor.service", "중지 요청", 258, MUTED)
d.msg("apparmor.service", "터미널 2", "All profile caches have been cle", 296, MUTED,
      sub="17:10:02 · apparmor[13883] · 원문이 여기서 잘림")
d.msg("systemd", "터미널 2", "Stopped AppArmor initialization.", 340, MUTED,
      sub="17:10:02 · systemd[1]")
d.msg("systemd", "터미널 2", "Starting AppArmor initialization...", 384, ACC, mk="acc",
      sub="17:10:02 · 저자가 짚은 자리 — 여기서 다시 올라온다")
d.state("apparmor.service", "PID 13904", 420, WARN)
d.msg("apparmor.service", "터미널 2", "* Starting AppArmor profiles", 452, MUTED,
      sub="17:10:02 · apparmor[13904]")
d.msg("apparmor.service", "터미널 2", "...done.", 494, OK, mk="ok",
      sub="17:10:09 · 7 초 뒤")

d.t(24, 548, "PID 가 13883 에서 13904 로 바뀐 것이 재시작의 증거입니다. 같은 유닛 이름이지만 프로세스는 다른 것입니다.",
     12, MUTED, KR, "start")
d.t(24, 570, "-u 로 유닛 하나만 걸러 두었기 때문에 이 화면에는 다른 서비스의 줄이 섞이지 않습니다.",
     12, SOFT, KR, "start")

d.legend(596, [("저자가 짚은 자리", ACC), ("재시작 전 PID", INFO),
                  ("재시작 후 PID", WARN), ("7 초 뒤 끝난 자리", OK)])
d.save("08-01.journal-restart.svg")
print("ok 08-01.journal-restart")
