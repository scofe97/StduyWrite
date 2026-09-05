# 02-01 §7 — strace -c 가 센 curl 한 번의 시스템 콜 시간 분포.
# 원문("syscalls"): `strace -c curl -s https://mhausenblas.info > /dev/null` 의 출력에서 저자가 남긴 행은
#       mmap 26.75%(0.031965s · 215회), read 17.52%(0.020935s · 153회 · 오류 3),
#       rt_sigaction 10.15%(0.012124s · 69회), openat 8.00%(0.009561s · 65회 · 오류 1),
#       close 7.61%(0.009098s · 72회)이고, 합계는 100.00%(0.119476s · 843회 · 오류 11)다.
#       나머지 행은 "..." 로 줄여져 있어 이 도식에서도 한 막대로 묶는다.
#       저자의 해석은 "the curl command here spends almost half of its time with mmap and read syscalls" 다.
# 타입 스펙: type-bar — 범주(시스템 콜)별 수치(전체 시간 대비 비율)를 막대 길이로 비교한다.
#           막대 길이는 비율에 정비례하고, 수치는 막대 끝에 글자로 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 880, 524
BAR_X, BAR_MAX, BAR_H, STRIDE, Y0 = 176, 520, 26, 46, 148

ROWS = [
    ("mmap", 26.75, "0.031965s · 215회", True),
    ("read", 17.52, "0.020935s · 153회", True),
    ("rt_sigaction", 10.15, "0.012124s · 69회", False),
    ("openat", 8.00, "0.009561s · 65회", False),
    ("close", 7.61, "0.009098s · 72회", False),
    ("나머지 (원문 생략)", 29.97, "합계 100.00% 에서 뺀 값", False),
]

d = D(W, H, "LEARNING MODERN LINUX · 02-01 §7",
      "curl 한 번이 시간을 어디에 쓰는가",
      "원서가 strace -c 로 센 curl 한 번의 시스템 콜 시간 분포. 막대 길이는 전체 시간 대비 비율이고, "
      "맨 아래 막대는 원문 출력에서 줄임표로 생략된 나머지 행을 합쳐 놓은 것이다.",
      "위 두 막대를 더하면 44.27% — 저자가 거의 절반이라 부른 값입니다")

for i, (name, pct, detail, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    w = BAR_MAX * pct / 100
    c = ACC if focal else (SOFT if i == len(ROWS) - 1 else MUTED)
    if focal:
        d.tone(BAR_X, y, w, BAR_H, ACC, 4, "2E", 1.2)
    else:
        d.o.append(f'<rect x="{BAR_X}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{c}3A"/>')
    d.t(24, y + 19, name, 13, INK, MONO if name[0].isascii() else KR, "start", 600)
    d.t(BAR_X + w + 14, y + 18, f"{pct:.2f}%", 13, c if focal else INK, MONO, "start", 600)
    d.t(BAR_X + w + 82, y + 18, detail, 12, MUTED, KR, "start")

d.t(24, 424, "출력 전체의 합계는 0.119476초에 843번, 그중 11번이 오류로 끝났습니다. "
             "여기서 읽을 것은 개별 수치가 아니라 어디에 몰렸는가입니다.", 12, MUTED, KR, "start")
d.t(24, 446, "저자가 함께 언급한 connect 는 원문 출력이 줄여져 있어 이 표에 행이 없습니다.",
    12, SOFT, KR, "start")

d.legend(462, [("저자가 거의 절반이라 부른 둘", ACC), ("원문에 남은 나머지 행", MUTED),
               ("생략된 행의 합", SOFT)])
d.save("02-01.strace-cost.svg")
print("ok 02-01.strace-cost")
