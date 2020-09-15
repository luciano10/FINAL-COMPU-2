import socket
def host_is_local(hostname, port=22): # no port specified, just use the ssh port
    """
    Returns True if the hostname points to the localhost, otherwise False.
    """
    hostname = socket.getfqdn(hostname)
    if hostname in ("localhost", "0.0.0.0", "127.0.0.1", "1.0.0.127.in-addr.arpa",
                    "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"):
        return True
    localhost = socket.gethostname()
    if hostname == localhost:
        return True
    localaddrs = socket.getaddrinfo(localhost, port)
    targetaddrs = socket.getaddrinfo(hostname, port)
    for (ignored_family, ignored_socktype, ignored_proto, ignored_canonname,
         sockaddr) in localaddrs:
        for (ignored_rfamily, ignored_rsocktype, ignored_rproto,
             ignored_rcanonname, rsockaddr) in targetaddrs:
            if rsockaddr[0] == sockaddr[0]:
                return True
    return False

print(host_is_local("1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa",22))
