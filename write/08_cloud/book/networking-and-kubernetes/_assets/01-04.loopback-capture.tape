Output "01-04.loopback-capture.gif"

Require tcpdump
Require curl

# 사용자가 직접 굽는 테이프다.
#
# macOS sudo 는 터미널마다 자격 증명을 따로 캐시한다(tty_tickets). vhs 는 새 가상
# 터미널을 띄우므로 밖에서 sudo -v 를 해 두어도 그 캐시가 넘어가지 않는다. 그래서
# 녹화 중 암호 프롬프트가 떠 멈춘다. 캡처는 굽기 전에 미리 떠 두고, 화면에서는
# 저장된 파일을 읽기만 한다 — pcap 읽기는 root 권한이 필요 없다.
#
# 굽기 전에 두 가지를 먼저 한다.
#   1. go run web-server.go &                                  # 8081 로 서버를 띄운다
#   2. sudo tcpdump -i lo0 -n port 8081 -w /tmp/loop.pcap &     # 캡처를 켠다
#      curl -s localhost:8081 && sudo pkill tcpdump             # 요청 한 번 뒤 멈춘다
#      sudo chmod 644 /tmp/loop.pcap                            # 읽기 권한을 준다
#
# 캡처 대상은 lo0 뿐이라 남의 트래픽이 섞이지 않는다.

Set Shell "bash"
Set Width 1440
Set Height 560
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "rm -f /tmp/loop.pcap"
Enter
Type "clear"
Enter
Show

Type "curl -s localhost:8081"
Sleep 400ms
Enter
Sleep 2s

Type "tcpdump -r /tmp/loop.pcap -n | wc -l"
Sleep 400ms
Enter
Wait+Screen /12/
Sleep 3s

Type `tcpdump -r /tmp/loop.pcap -n | awk '{split($3,a,"."); split($5,b,"."); gsub(",","",$7); printf "%-6s -> %-6s %-5s len=%s\n", a[length(a)], b[length(b)], $7, $NF}'`
Sleep 400ms
Enter
Sleep 8s
