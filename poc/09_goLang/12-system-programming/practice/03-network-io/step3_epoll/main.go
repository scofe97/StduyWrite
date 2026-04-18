//go:build linux

package main

import (
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

// Step 3: epoll로 I/O 멀티플렉싱
//
// 목표: epoll을 사용하여 다중 연결을 효율적으로 처리합니다.
// 단일 스레드로 수천 개의 연결을 관리하는 방법을 배웁니다.
//
// 실행:
//   go run main.go
//
// 테스트:
//   다른 터미널에서: for i in {1..10}; do nc localhost 8082 & done
//
// 검증:
//   strace -e epoll_create1,epoll_ctl,epoll_wait go run main.go

const (
	serverPort = 8082
	maxEvents  = 64
)

func main() {
	fmt.Println("=== epoll 멀티플렉싱 서버 ===")

	// ----------------------------------------
	// Part 1: 서버 소켓 생성 (논블로킹)
	// ----------------------------------------
	serverFd, err := createNonBlockingServer(serverPort)
	if err != nil {
		fmt.Printf("서버 생성 실패: %v\n", err)
		return
	}
	defer unix.Close(serverFd)
	fmt.Printf("서버 소켓 생성됨 (fd: %d, 포트: %d)\n", serverFd, serverPort)

	// ----------------------------------------
	// TODO 1: epoll 인스턴스 생성
	// ----------------------------------------
	// 힌트:
	// epollFd, err := unix.EpollCreate1(0)
	// - EpollCreate1(0)은 epoll 파일 디스크립터 반환
	// - 이 fd로 여러 소켓을 모니터링

	// epollFd, err := unix.EpollCreate1(0)
	// if err != nil {
	// 	fmt.Printf("epoll 생성 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(epollFd)
	// fmt.Printf("epoll 인스턴스 생성됨 (fd: %d)\n", epollFd)

	fmt.Println("(TODO: epoll 인스턴스 생성)")
	epollFd := 5 // 임시값

	// ----------------------------------------
	// TODO 2: 서버 소켓을 epoll에 등록
	// ----------------------------------------
	// 힌트:
	// unix.EpollCtl(epollFd, op, fd, event)
	// - op: EPOLL_CTL_ADD (등록), EPOLL_CTL_MOD (수정), EPOLL_CTL_DEL (삭제)
	// - event.Events: EPOLLIN (읽기 가능), EPOLLOUT (쓰기 가능)
	// - event.Fd: 이벤트 발생 시 어떤 fd인지 식별

	// event := unix.EpollEvent{
	// 	Events: unix.EPOLLIN,
	// 	Fd:     int32(serverFd),
	// }
	// err = unix.EpollCtl(epollFd, unix.EPOLL_CTL_ADD, serverFd, &event)
	// if err != nil {
	// 	fmt.Printf("서버 소켓 등록 실패: %v\n", err)
	// 	return
	// }
	// fmt.Println("서버 소켓을 epoll에 등록함")

	fmt.Println("(TODO: 서버 소켓을 epoll에 등록)")

	// ----------------------------------------
	// TODO 3: 이벤트 루프
	// ----------------------------------------
	fmt.Println("\n이벤트 루프 시작...")
	fmt.Println("다른 터미널에서: nc localhost", serverPort)

	events := make([]unix.EpollEvent, maxEvents)

	// for {
	// 	// epoll_wait: 이벤트가 발생할 때까지 대기
	// 	// - 타임아웃 -1: 무한 대기
	// 	// - 반환값 n: 발생한 이벤트 개수
	// 	n, err := unix.EpollWait(epollFd, events, -1)
	// 	if err != nil {
	// 		if err == unix.EINTR {
	// 			continue  // 시그널에 의한 인터럽트, 재시도
	// 		}
	// 		fmt.Printf("epoll_wait 실패: %v\n", err)
	// 		break
	// 	}
	//
	// 	// 발생한 이벤트 처리
	// 	for i := 0; i < n; i++ {
	// 		fd := int(events[i].Fd)
	//
	// 		if fd == serverFd {
	// 			// 새 연결 요청
	// 			handleNewConnection(epollFd, serverFd)
	// 		} else {
	// 			// 기존 클라이언트 데이터
	// 			handleClientData(epollFd, fd)
	// 		}
	// 	}
	// }

	fmt.Println("(TODO: 이벤트 루프 구현)")
	_ = events
	_ = epollFd
}

// handleNewConnection은 새 클라이언트 연결을 처리합니다.
func handleNewConnection(epollFd, serverFd int) {
	// ----------------------------------------
	// TODO 4: 새 연결 Accept
	// ----------------------------------------

	// clientFd, clientAddr, err := unix.Accept(serverFd)
	// if err != nil {
	// 	fmt.Printf("Accept 실패: %v\n", err)
	// 	return
	// }

	// 클라이언트 정보 출력
	// if addr, ok := clientAddr.(*unix.SockaddrInet4); ok {
	// 	fmt.Printf("새 연결: %d.%d.%d.%d:%d (fd: %d)\n",
	// 		addr.Addr[0], addr.Addr[1], addr.Addr[2], addr.Addr[3],
	// 		addr.Port, clientFd)
	// }

	// ----------------------------------------
	// TODO 5: 클라이언트 소켓을 논블로킹으로 설정
	// ----------------------------------------
	// unix.SetNonblock(clientFd, true)

	// ----------------------------------------
	// TODO 6: 클라이언트 소켓을 epoll에 등록
	// ----------------------------------------
	// clientEvent := unix.EpollEvent{
	// 	Events: unix.EPOLLIN | unix.EPOLLET,  // Edge-Triggered 모드
	// 	Fd:     int32(clientFd),
	// }
	// unix.EpollCtl(epollFd, unix.EPOLL_CTL_ADD, clientFd, &clientEvent)

	fmt.Println("(TODO: 새 연결 처리 구현)")
}

// handleClientData는 클라이언트로부터 데이터를 처리합니다.
func handleClientData(epollFd, clientFd int) {
	// ----------------------------------------
	// TODO 7: 데이터 읽기
	// ----------------------------------------
	buf := make([]byte, 1024)

	// n, err := unix.Read(clientFd, buf)
	// if err != nil || n == 0 {
	// 	// 연결 종료 또는 에러
	// 	fmt.Printf("클라이언트 연결 종료 (fd: %d)\n", clientFd)
	// 	unix.EpollCtl(epollFd, unix.EPOLL_CTL_DEL, clientFd, nil)
	// 	unix.Close(clientFd)
	// 	return
	// }

	// fmt.Printf("수신 (fd: %d): %s", clientFd, string(buf[:n]))

	// ----------------------------------------
	// TODO 8: 에코 응답
	// ----------------------------------------
	// response := []byte(fmt.Sprintf("Echo: %s", buf[:n]))
	// unix.Write(clientFd, response)

	fmt.Println("(TODO: 데이터 처리 구현)")
	_ = buf
}

func createNonBlockingServer(port int) (int, error) {
	serverFd, err := unix.Socket(unix.AF_INET, unix.SOCK_STREAM|unix.SOCK_NONBLOCK, 0)
	if err != nil {
		return -1, err
	}

	unix.SetsockoptInt(serverFd, unix.SOL_SOCKET, unix.SO_REUSEADDR, 1)

	addr := &unix.SockaddrInet4{Port: port, Addr: [4]byte{127, 0, 0, 1}}
	if err := unix.Bind(serverFd, addr); err != nil {
		unix.Close(serverFd)
		return -1, err
	}

	if err := unix.Listen(serverFd, 128); err != nil {
		unix.Close(serverFd)
		return -1, err
	}

	return serverFd, nil
}

// ----------------------------------------
// 추가 실험: Edge-Triggered vs Level-Triggered
// ----------------------------------------

func edgeTriggeredNote() {
	// Level-Triggered (기본값)
	// - 조건이 충족되면 계속 이벤트 발생
	// - 예: 버퍼에 데이터가 있으면 계속 EPOLLIN 발생
	// - 장점: 놓치기 어려움
	// - 단점: 불필요한 이벤트 발생 가능

	// Edge-Triggered (EPOLLET)
	// - 상태 "변화" 시에만 이벤트 발생
	// - 예: 새 데이터가 도착할 때만 EPOLLIN 발생
	// - 장점: 효율적
	// - 단점: 모든 데이터를 한 번에 읽어야 함 (놓칠 수 있음)

	fmt.Println(`
Edge-Triggered 사용 시 주의:
1. 한 번의 이벤트에서 모든 데이터를 읽어야 함
2. EAGAIN이 발생할 때까지 읽기 반복
3. 논블로킹 소켓 필수

for {
    n, err := unix.Read(fd, buf)
    if err == unix.EAGAIN {
        break  // 모든 데이터 읽음
    }
    // 데이터 처리...
}
`)
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. epoll_wait의 타임아웃
//    - -1: 이벤트 발생까지 무한 대기
//    - 0: 즉시 반환 (논블로킹 체크)
//    - n: n 밀리초 대기
//
// 2. 왜 epoll이 select보다 빠른가?
//    - select: O(n) - 매번 모든 fd 검사
//    - epoll: O(1) - 커널이 준비된 fd만 반환
//    - 많은 연결에서 차이가 극명함
//
// 3. Go의 netpoll
//    - Go 런타임이 내부적으로 epoll 사용
//    - 고루틴이 I/O 대기 시 자동으로 epoll에 등록
//    - 개발자는 블로킹 코드처럼 작성
//
// 4. 실무에서의 사용
//    - 직접 epoll 사용: 극한의 성능이 필요할 때
//    - 대부분: Go의 net 패키지 사용 (충분히 빠름)

func main2() {
	_ = os.Args
}
