from python:latest
USER root
RUN apt-get update -y && apt-get install -y socat
RUN pip install pycryptodome 
RUN pip install sympy 

RUN useradd -u 666 --home=/challenge -U CTF
WORKDIR /challenge/
COPY . .
USER CTF
ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'python3 Farfour_post_quantom.py'${SOCAT_OPTIONS}"]
