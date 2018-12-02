from ctypes import byref, CDLL, c_int, c_size_t, POINTER
from ctypes.util import find_library
from errno import ENOENT, ESRCH, EALREADY
from socket import socket

libSystem = CDLL(find_library('System'))


class LaunchdSocketActivateError(Exception):
    # from launch_activate_socket(3)
    errors = {
        ENOENT: "The socket name specified does not exist in the caller's launchd.plist(5).",
        ESRCH: 'The calling process is not managed by launchd(8).',
        EALREADY: 'The specified socket has already been activated.'
    }
        
    def __init__(self, errcode):
        if errcode not in self.errors:
            raise ValueError('unexpected error code')
        super().__init__(self, errcode)
        self.errcode = errcode

    def __str__(self):
        return self.errors[self.errcode]


def launch_activate_socket(name: str):
    fds = POINTER(c_int)()
    count = c_size_t()
    
    res = libSystem.launch_activate_socket(name.encode('utf-8'), byref(fds), byref(count))
    if res:
        raise LaunchdSocketActivateError(res)

    sockets = [socket(fileno=fds[s]) for s in range(count.value)]
    libSystem.free(fds)
    return sockets
