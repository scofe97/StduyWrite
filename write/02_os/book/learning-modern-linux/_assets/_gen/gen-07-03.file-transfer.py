# 07-03 §5 — 무엇을 어디로 옮기느냐가 도구를 정한다.
# 원문("File Transfer"): "scp (short for 'secure copy') works on top of SSH. Given that scp defaults to
#       ssh, we need to make sure that we have the password (or even better, key-based authentication) in
#       place for it to work."
#       "Synchronizing files with rsync is much more convenient and faster than scp. Under the hood, rsync
#       uses SSH by default."
#       "-a for archive (incremental, preserve), -v for verbose so that we see something, and -z for using
#       compression." / "since -a includes -r which is recursive"
#       "If you're unsure what rsync will do, use the --dry-run option ... It will essentially tell you
#       what it will do without actually carrying out the operation, so it's safe."
#       경고 — "Don't forget the : after the host! Without it, rsync will happily go ahead and interpret
#       the source or destination as a local directory."
#       S3 — "aws s3 sync ... --no-sign-request" 로 공개 버킷에서 받는다.
#       FTP — "we don't recommend using it anymore. Not only are these insecure, but there are also many
#       better alternatives ... So, there's no actual need for FTP anymore."
# 주의: 원문의 rsync 목적지는 `mh9@:63.32.106.149:` 로 @ 뒤에 콜론이 하나 더 있어 그대로는 안 된다.
#       저자 자신이 "Destination in user@host format" 이라 적으므로 도식은 고친 형태를 쓰고 표시한다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 선택. accent 는 조용히 실패하는 자리.
#           축약: NFS·SMB 는 복사가 아니라 마운트라 이 갈래에 넣지 않고 별도 띠로 표시.
# 2026-11-17: 제목이 셋이라면서 상자가 넷이던 것을 고쳤다 — NFS 는 §6 의 copy-sync-mount 가 맡으므로
#       여기서 뺐다. 콜론 경고 상자는 노트가 rsync 시트로 넘겼으므로 지웠다. SSH 위라는 표시는
#       왼쪽 산문 상자 대신 각 행의 머리표로 옮겼다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 496
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §5",
      "둘은 SSH 위에 있고, 하나는 아예 다른 길이다",
      "파일을 옮기는 도구는 상황이 정한다. scp 와 rsync 는 SSH 위에 얹히고 "
      "S3 는 그것과 무관한 길이다. 복사 대신 마운트하는 NFS 는 §6 에서 따로 본다.",
      "FTP 는 더는 권하지 않는 길")

QX, QY, QW, QH = 32, 164, 208, 76
d.box(QX, QY, QW, QH, PAPER2, INFO, 1.2, 8)
d.t(QX + QW / 2, QY + 32, "무엇을 옮기는가", 14, INFO, KR, "middle", 600)
d.t(QX + QW / 2, QY + 54, "그리고 몇 번 옮기는가", 11.5, MUTED, KR)

BX, BW, BH2, BGAP = 288, 560, 76, 12
opts = [
    ("scp", "파일 하나를 한 번", "scp copyme user@host:/path/", OK, 0),
    ("rsync -avz", "디렉토리를 반복해서 맞출 때", "더해지거나 바뀐 파일만 복사한다", ACC, 1),
    ("aws s3 sync", "공개 S3 버킷에서 받을 때", "--no-sign-request 로 인증을 건너뛴다", INFO, 0),
]
for i, (name, when, how, col, focal) in enumerate(opts):
    y = QY + i * (BH2 + BGAP)
    if focal:
        d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH2}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(BX, y, BW, BH2, PAPER2, col, 1.2, 8)
    d.t(BX + 18, y + 28, name, 13.5, col, MONO, "start", 600)
    d.t(BX + 18, y + 50, when, 11.5, MUTED, KR, "start")
    d.t(BX + BW - 18, y + 60, how, 11.5, SOFT, MONO, "end")
    if col is not INFO:
        d.t(BX + BW - 18, y + 28, "SSH 위 · 키 인증 먼저", 11.5, OK, KR, "end", 600)
    d.path(f"M {QX + QW} {QY + 38} L {(QX + QW + BX) / 2} {QY + 38} "
           f"L {(QX + QW + BX) / 2} {y + 38} L {BX - 8} {y + 38}",
           col, 1.3, m="acc" if focal else "ar")

d.legend(446, [("SSH 위 · 한 번", OK), ("SSH 위 · 반복해서 맞춤", ACC), ("SSH 와 무관한 길", INFO)])
d.save("07-03.file-transfer.svg")
print("ok 07-03.file-transfer")
