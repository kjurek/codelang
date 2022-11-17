FROM python:3.10

RUN apt-get update && apt-get install -y build-essential cmake

RUN useradd -ms /bin/bash intellisense
USER intellisense
WORKDIR /home/intellisense

# setup ycmd
RUN git clone --recurse-submodules https://github.com/ycm-core/ycmd.git
RUN python -m venv venv
RUN . /home/intellisense/venv/bin/activate && pip install --upgrade pip
RUN . /home/intellisense/venv/bin/activate && cd ycmd && pip install -r requirements.txt && python build.py --clang-completer

COPY requirements.in /tmp
RUN . /home/intellisense/venv/bin/activate && pip install pip-tools && pip-compile /tmp/requirements.in && pip-sync /tmp/requirements.txt

COPY .ycm_extra_conf.py /home/intellisense/app/.ycm_extra_conf.py

COPY src /home/intellisense/app/src
COPY start_ycmd.sh /home/intellisense/app
COPY start_intellisense.sh /home/intellisense/app
WORKDIR /home/intellisense/app
CMD . /home/intellisense/venv/bin/activate && ./start_ycmd.sh && ./start_intellisense.sh
