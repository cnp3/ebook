# Time protocol server implementation

This is a Time protocol (RFC868) server implementation. It can run as a simple executable and will listen by default on TCP and UDP port 37.

This program can be run as a `systemd` service.

## Installation

Here are the compilation/installation steps, both as a standalone app and as a `systemd` service.

### Standalone app

To compile the program without the `systemd` capabilities, simply run the following line :

    make server

### Systemd service

You first need to install the systemd header files. 

**On Ubuntu, you can run:**

    apt-get install libsystemd-dev

**On CentOS 7, you can run:**

    yum install systemd-devel

Then, you can run the following commands :

    make systemd-server
    make install-systemd
    systemctl enable timeprotocolserver-cnp3  # auto-start the server at boot
    systemctl start timeprotocolserver-cnp3  # start the server now



