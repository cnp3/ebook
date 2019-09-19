CFLAGS = --std=c99 -Wall -Werror -Wextra
server: time_protocol_server.c
	gcc $(CFLAGS) time_protocol_server.c -o server

systemd-server: time_protocol_server.c
	gcc $(CFLAGS) -DUSE_SYSTEMD -lsystemd time_protocol_server.c -o systemd-server

.PHONY: install-systemd
install-systemd:
	test -e systemd-server || { echo "please run `make systemd-server` before installation"; exit 1; }
	groupadd -f cnp3
	id -u cnp3 >/dev/null 2>&1 || useradd -N cnp3
	usermod -a -G cnp3 cnp3
	cp systemd-server /usr/sbin/timeprotocol-cnp3-server
	cp timeprotocolserver-cnp3.service /usr/lib/systemd/system/
	cp timeprotocolserver-cnp3-stream.socket /usr/lib/systemd/system/
	cp timeprotocolserver-cnp3-datagram.socket /usr/lib/systemd/system/



clean:
	rm -f server
