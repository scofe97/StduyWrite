BINARY := myapp
INSTALL_DIR := $(HOME)/.local/bin

.PHONY: build clean run, check

build:
	@echo "빌드 중 ..."
	go build -o $(BINARY) .
	@echo "완료: $(BINARY)"

clean:
	@echo "정리 중..."
	rm  -f $(BINARY)

run: build
	@echo "실행 중..."
	./$(BINARY)

check:
	@if [ -f $(BINARY) ]; then \
  		echo "$(BINARY) 존재함"; \
	else \
  		echo "$(BINATY) - make build 필요"; \
	fi

install: build
	@mkdir -p "$(INSTALL_DIR)"
	@cp $(BINARY) $(INSTALL_DIR)/
	@echo "설치 완료: $(INSTALL_DIR)/$(BINARY)"

uninstall:
	@rm -f $(INSTALL_DIR)/$(BINARY)
	@echo "제거 완료"