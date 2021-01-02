FROM python

# setup ycmd
RUN apt-get update && apt-get install -y build-essential cmake
RUN git clone --recurse-submodules https://github.com/ycm-core/ycmd.git /ycmd
RUN cd /ycmd && pip install -r requirements.txt && python build.py --clang-completer

RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY .ycm_extra_conf.py /app/.ycm_extra_conf.py

COPY src /app/src
COPY start_ycmd.sh /app
COPY start_intellisense.sh /app
WORKDIR /app
CMD ./start_ycmd.sh && ./start_intellisense.sh