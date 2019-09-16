/**
 *  This file implements a simple Time Protocol (RFC868) server using the socket API.
 *  The server listens on both IPv4 and IPv6 using both UDP and TCP.
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <getopt.h>
#include <time.h>
#include <sys/select.h>

#ifdef USE_SYSTEMD
#include <systemd/sd-daemon.h>
#endif

#define TIME_PORT 37
#define MAX_MESSAGE_SIZE 2000
#define SECONDS_FROM_1900_TO_1970 2208988800U // according to RFC868

// returns the number of seconds elapsed from 1st of January 1900 until now
double get_number_of_seconds_since_1900() {
    return SECONDS_FROM_1900_TO_1970 + (double) time(NULL);  // 1900->1970 + 1970->now (UTC)
}

// works with both STREAM and DGRAM
// sends the current Time as defined in RFC868 on sock
//
// returns -1 upon error, 0 otherwise
int handle_request(int sock, struct sockaddr *addr, socklen_t addrlen) {
    uint32_t val = htonl((uint32_t) get_number_of_seconds_since_1900());
    ssize_t sent = sendto(sock, &val, sizeof(val), 0, addr, addrlen);
    if (sent == -1) {
        perror("couldn't send data on socket");
        return -1;
    }
    return 0;
}

// this server won't work correctly anymore from year 2036
int multi_sockets_time_server(in_port_t port, bool daemon) {
    const size_t max_error_size = 250;
    char errstr[max_error_size+1];
    errstr[max_error_size] = '\0'; // by this, we ensure that snpritnf never ends up having a string not null-terminated
    const int DGRAM = 0, STREAM = 1;
    // create the sockets
    int err = 0;
    int sockets[2];
    if (!daemon) {
        sockets[DGRAM] = socket(AF_INET6, SOCK_DGRAM, 0);
        if (sockets[DGRAM] == -1) {
            perror("couldn't create the socket");
            return -1;
        }
        sockets[STREAM] = socket(AF_INET6, SOCK_STREAM, 0);
        if (sockets[STREAM] == -1) {
            perror("couldn't create the dgram socket");
            return -1;
        }
        struct sockaddr_in6 local_addr;    // allocate the IPv6 socket address on the stack
        memset(&local_addr, 0, sizeof(struct sockaddr_in6));
        local_addr.sin6_family = AF_INET6;
        local_addr.sin6_port = htons(port);
        memcpy(&local_addr.sin6_addr, &in6addr_any, sizeof(in6addr_any));   // listen to any address
        for (int i = 0 ; i < 2 ; i++) {
            int err = setsockopt(sockets[i], IPPROTO_IPV6, IPV6_V6ONLY, &(int){0}, sizeof(int)); // allow both IPv4 and IPv6
            if (err == -1) {
                snprintf(errstr, max_error_size, "couldn't disable V6ONLY for socket %d", i);
                perror(errstr);
                return -1;
            }
        }
        err = setsockopt(sockets[STREAM], SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));
        if (err) {
            perror("couldn't set SO_REUSEADDR on STREAM socket");
            return -1;
        }
        for (int i = 0 ; i < 2 ; i++) {
            int err = bind(sockets[i], (struct sockaddr *) &local_addr, sizeof(local_addr));
            if (err) {
                snprintf(errstr, max_error_size, "couldn't bind the socket %d", i);
                perror(errstr);
                return -1;
            }
        }
        // the streaming socket is a passive socket that will give us one socket per connection
        err = listen(sockets[STREAM], 50);
        if (err == -1) {
            perror("couldn't listen on the stream socket");
            return -1;
        }
    } 
#ifdef USE_SYSTEMD
    else {
        int n_fds = sd_listen_fds(0);
        if (n_fds != 2) {
            printf("error: systemd returned the wrong number of fds: %d instead of %d\n", n_fds, 2);
            return -1;
        }
        sockets[STREAM] = sockets[DGRAM] = -1;
        for (int i = SD_LISTEN_FDS_START ; i < SD_LISTEN_FDS_START + n_fds ; i++) {
            if (sockets[STREAM] == -1 && sd_is_socket_inet(i, AF_INET6, SOCK_STREAM, 1, port))
                sockets[STREAM] = i;
            else if (sockets[DGRAM] == -1 && sd_is_socket_inet(i, AF_INET6, SOCK_DGRAM, 0, port))
                sockets[DGRAM] = i;
            else {
                printf("socket %d does not fit our needs\n", i);
                return -1;
            }
        }
    }
#endif

    // allocate the peer addr on the stack
    struct sockaddr_storage peer_addr;
    socklen_t addrlen = sizeof(peer_addr);

    // allocate the reception buffer on the stack (it could be of size 0 without problem)
    uint8_t buffer[MAX_MESSAGE_SIZE];

    fd_set set;
    while(1) {
        addrlen = sizeof(peer_addr);
        FD_ZERO(&set);
        int max_fd = sockets[STREAM];
        for (int i = 0 ; i < 2 ; i++) {
            FD_SET(sockets[i], &set);
            max_fd = (max_fd < sockets[i]) ? sockets[i] : max_fd;
        }

        // listen on both SOCK_STREAM (TCP) and SOCK_DGRAM (UDP)
        err = select(max_fd + 1, &set, NULL, NULL, NULL);
	    if (err == -1) {
            perror("couldn't perform select");
            return -1;
        }
        if (FD_ISSET(sockets[STREAM], &set)) {
            // with TCP, a Time Protocol request is a connection
            int conn_socket = accept(sockets[STREAM], (struct sockaddr *) &peer_addr, &addrlen);
            err = handle_request(conn_socket, (struct sockaddr *) &peer_addr, addrlen);
            if (err) {
                printf("error when handling request\n");
            }
            close(conn_socket);
        }
        if (FD_ISSET(sockets[DGRAM], &set)) {
            // with UDP, a Time Protocol request is an empty datagram
            ssize_t read_bytes = recvfrom(sockets[DGRAM], buffer, MAX_MESSAGE_SIZE, 0, (struct sockaddr *) &peer_addr, &addrlen);
            if (read_bytes == -1) {
                perror("couldn't receive data on socket");
                return -1;
            }
            err = handle_request(sockets[DGRAM],  (struct sockaddr *) &peer_addr, addrlen);
            if (err) {
                printf("error when handling request");
            }
        }
    }
}



int main(int argc, char *argv[]) {
    in_port_t port = TIME_PORT;
    int opt;
    int status_code = EXIT_FAILURE;
    bool daemon = false;
    while ((opt = getopt(argc, argv, "Dhp:")) != -1) {
        switch (opt) {
        case 'p':
            port = atoi(optarg);
            break;
        case 'D':
#ifdef USE_SYSTEMD
            // daemon mode
            daemon = true;
#else
            fprintf(stderr, "-D arg is not activated on this version of the server. Please recompile it with -DUSE_SYSTEMD\n");
            exit(EXIT_FAILURE);
#endif
            break;
        case 'h':
            status_code = 0;
            // fall through
        default: /* '?' */
            fprintf(stderr, "Usage: %s [-D] [-p port]\nThe port will be used both for TCP and UDP. It is set to 37 if -p is not used. If -D is used, the programs will retrieve the sockets from systemd\n",
                    argv[0]);
            exit(status_code);
        }
    }
    multi_sockets_time_server(port, daemon);
    return 0;
}
