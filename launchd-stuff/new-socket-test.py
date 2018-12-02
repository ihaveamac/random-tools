from launchdsocket import launch_activate_socket

ss = launch_activate_socket('Listeners')

print(ss)

so = ss[0]
so.listen()

cs, a = so.accept()
print('Got conn from', a)
cs.send(b'Go away\n')

for s in ss:
    s.close()
