# 22. Go로 컨테이너 만들기 학습 회고

학습 완료 후 작성합니다.

---

## 핵심 개념 정리

### 컨테이너 vs VM
```
내가 이해한 차이점:

VM이 "무거운" 이유:

컨테이너가 "가벼운" 이유:

```

### Namespaces
```
내가 이해한 내용:

각 Namespace가 격리하는 것:
- UTS:
- PID:
- MNT:
- NET:
- IPC:
- USER:

```

### CGroups
```
내가 이해한 내용:

CGroups가 제한하는 리소스:
- memory:
- cpu:
- io:

```

### chroot vs pivot_root
```
chroot의 한계:

pivot_root가 더 안전한 이유:

Docker가 pivot_root를 사용하는 이유:

```

---

## 실험 기록

### Namespace 격리 테스트

| 테스트 | 결과 | 비고 |
|--------|------|------|
| UTS (hostname) | | |
| PID (ps aux) | | |
| MNT (/proc) | | |

### CGroups 리소스 제한 테스트

| 테스트 | 결과 | 비고 |
|--------|------|------|
| 메모리 100MB 제한 | | |
| OOM Killer 동작 | | |
| CPU 제한 | | |

---

## 질문과 답변

### Q: run/child 패턴이 필요한 이유는?
```
A:

```

### Q: /proc을 마운트해야 하는 이유는?
```
A:

```

### Q: 컨테이너가 호스트 커널을 공유한다는 의미는?
```
A:

```

### Q: Docker가 추가로 하는 일들은?
```
A:

```

---

## 어려웠던 점



---

## Docker와 비교

| 기능 | 우리 구현 | Docker |
|------|----------|--------|
| Namespace | 기본 3개 | 모든 6개 |
| 파일시스템 | chroot | pivot_root + overlayfs |
| CGroups | 메모리만 | 전체 리소스 |
| 네트워크 | X | veth + bridge |
| 이미지 | 수동 rootfs | 레이어드 이미지 |

---

## 추가 학습 계획

- [ ] pivot_root 구현
- [ ] 네트워크 격리 (veth 페어)
- [ ] OverlayFS 사용
- [ ] runc 소스 코드 읽기
- [ ] containerd 아키텍처 이해
