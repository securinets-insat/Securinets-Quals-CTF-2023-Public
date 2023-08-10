FROM ubuntu
from python:latest
USER root
RUN apt-get update -y && apt-get install -y socat
RUN pip install pycryptodome 
RUN apt-get install  libgmp3-dev -y
RUN pip install fastecdsa
RUN apt-get install socat -y

RUN useradd -u 666 --home=/challenge -U CTF
WORKDIR /challenge/
COPY . .
USER CTF
ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'python3 DigestiveV2.py'${SOCAT_OPTIONS}"]

