FROM python

RUN apt-get update && apt-get install -y build-essential cmake patchelf

RUN useradd -ms /bin/bash executor

RUN git clone https://github.com/cloudflare/sandbox.git /usr/src/sandbox
WORKDIR /usr/src/sandbox
RUN curl -L -O https://github.com/seccomp/libseccomp/releases/download/v2.4.3/libseccomp-2.4.3.tar.gz
RUN tar xf libseccomp-2.4.3.tar.gz && mv libseccomp-2.4.3 libseccomp
RUN cd libseccomp && ./configure --enable-shared=no && make
RUN make && cp libsandbox.so /usr/lib/x86_64-linux-gnu

RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir /code

COPY src /app/src
WORKDIR /app

CMD gunicorn src.main:app -b 0.0.0.0:${APPLICATION_PORT} -w ${UVICORN_WORKERS} -k uvicorn.workers.UvicornWorker