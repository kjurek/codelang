FROM python
RUN apt-get update && apt-get install -y apt-utils build-essential cmake
WORKDIR /workdir/ycmd
RUN git clone --recurse-submodules https://github.com/ycm-core/ycmd.git /workdir/ycmd
RUN pip install -r requirements.txt && python build.py --clangd-completer
COPY .ycm_extra_conf.py /workdir
EXPOSE 80
CMD ["python", "-m", "ycmd", "--options_file", "/workdir/ycmd/ycmd/default_settings.json", "--host", "0.0.0.0", "--port", "80"]
