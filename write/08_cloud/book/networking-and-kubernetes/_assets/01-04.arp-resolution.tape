Output "01-04.arp-resolution.gif"

Require tcpdump
Require ping

# §3 실행 장면. 이 랜의 게이트웨이 IP 와 양쪽 MAC 은 화면에 그대로 찍히므로
# 캡처를 미리 떠 두고, 화면에서는 sed 로 마스킹한 결과만 읽는다.
# 그래서 이 GIF 는 공개 저장소에 올려도 된다.
#
# 굽기 전에 (터미널에서 직접, sudo 암호를 여기서만 친다):
#   GW=$(netstat -rn -f inet | awk '$1=="default" && $NF=="en0"{print $2; exit}')
#   sudo tcpdump -i en0 -e -n arp -c 4 -w /tmp/arp.pcap &
#   sleep 2; sudo arp -d "$GW"; ping -c 1 "$GW" >/dev/null; sleep 2
#   sudo pkill tcpdump; sudo chmod 644 /tmp/arp.pcap
#
# vhs 는 새 가상 터미널을 띄우고 macOS sudo 는 터미널마다 자격 증명을 따로
# 캐시하므로(tty_tickets), 화면 안에서 sudo 를 쓰면 암호를 물어 멈춘다.

Set Shell "bash"
Set Width 1440
Set Height 420
Set FontSize 18
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "# 주소는 마스킹해 읽는다 — 형태만 보면 되기 때문이다"
Enter
Sleep 1s

Type `tcpdump -r /tmp/arp.pcap -e -n 2>/dev/null | sed -E 's/([0-9a-f]{1,2}:){5}[0-9a-f]{1,2}/MAC/g; s/([0-9]{1,3}\.){3}[0-9]{1,3}/IP/g' | cut -c1-104`
Sleep 400ms
Enter
Sleep 8s
