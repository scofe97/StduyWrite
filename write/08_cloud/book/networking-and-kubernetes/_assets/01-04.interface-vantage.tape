Output "01-04.interface-vantage.gif"

Set Shell "bash"
Set Width 1440
Set Height 340
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
Type "clear"
Enter
Show

Type "ifconfig lo0 | grep -cE '^[[:space:]]*ether'"
Sleep 400ms
Enter
Sleep 700ms

Type "ifconfig en0 | grep -cE '^[[:space:]]*ether'"
Sleep 400ms
Enter
Sleep 900ms

Type "ifconfig lo0 | grep -o 'mtu [0-9]*'"
Sleep 400ms
Enter
Sleep 700ms

Type "ifconfig en0 | grep -o 'mtu [0-9]*'"
Sleep 400ms
Enter
Wait+Screen /mtu 1500/
Sleep 6s
