Output "18-01-job-delete.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 260
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/18-job.kubeconfig >/dev/null 2>&1"
Enter
Sleep 500ms
Type "kubectl config set-context --current --namespace=job-lab >/dev/null 2>&1"
Enter
Sleep 500ms
Type "kubectl delete job quiz-init demo-suspend --ignore-not-found >/dev/null 2>&1"
Enter
Sleep 2s
Type "kubectl delete po --all --ignore-not-found >/dev/null 2>&1"
Enter
Sleep 3s
Type "kubectl apply -f /tmp/job-demo.yaml >/dev/null 2>&1"
Enter
Sleep 2s
Type "kubectl wait --for=condition=complete job/quiz-init --timeout=90s >/dev/null 2>&1"
Enter
Sleep 20s
Type "export PS1='$ '"
Enter
Sleep 500ms
Type "clear"
Enter
Sleep 1s
Show

Type "kubectl delete job quiz-init"
Sleep 400ms
Enter
Wait+Screen /deleted/
Sleep 2s

Type "kubectl get po -l job-name=quiz-init"
Sleep 400ms
Enter
Wait+Screen /No resources found/
Sleep 6s
