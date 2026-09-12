Output "05-04.icmp-roundtrip.gif"

Require tcpdump

Set Shell "bash"
Set Width 1440
Set Height 620
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 16ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "tcpdump -n -i en0 -c 9 'icmp or (udp and dst host 1.1.1.1)' &"
Sleep 500ms
Enter
Sleep 2s

Type "traceroute -m 2 -w 1 1.1.1.1 > /dev/null"
Sleep 500ms
Enter
Sleep 6s

Sleep 6s
