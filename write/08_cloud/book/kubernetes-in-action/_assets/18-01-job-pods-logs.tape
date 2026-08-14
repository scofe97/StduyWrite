Output "18-01-job-pods-logs.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 300
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/18-job.kubeconfig"
Enter
Type "kubectl config set-context --current --namespace=job-lab"
Enter
Type "kubectl delete job quiz-init --ignore-not-found"
Enter
Type "kubectl apply -f /tmp/job-demo.yaml"
Enter
Type "kubectl wait --for=condition=complete job/quiz-init --timeout=90s"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "kubectl get pods -l job-name=quiz-init"
Sleep 400ms
Enter
Wait+Screen /Completed/
Sleep 4s

Type "kubectl logs job/quiz-init --all-containers --prefix"
Sleep 400ms
Enter
Wait+Screen /imported/
Sleep 6s
