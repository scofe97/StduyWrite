Output "05-04.traceroute-probes.gif"

Require traceroute

Set Shell "bash"
Set Width 1440
Set Height 700
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

Type "traceroute -m 5 -w 1 1.1.1.1; traceroute -m 5 -w 1 -q 1 1.1.1.1"
Sleep 700ms
Enter
Sleep 11s

Sleep 6s
