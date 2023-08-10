FROM ubuntu

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY Tomojiski .
COPY flag.txt .
COPY font.txt .
COPY ynetd .
 
RUN chmod 777 ynetd
RUN chmod 777 Tomojiski

USER ctf
CMD ./ynetd -p 1323 ./Tomojiski