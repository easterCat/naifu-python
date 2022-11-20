# syntax=docker/dockerfile:1

FROM python:3.8.15

WORKDIR /

RUN mkdir projects \ 
    && cd projects \
    && git clone https://github.com/easterCat/stable-diffution-utils-python.git \ 
    && cd stable-diffution-utils-python \
    && pip install --upgrade pip \
    && pip install torchvision \
    && pip install torchaudio \
    && pip install --upgrade setuptools \
    && python -m venv venv \
    && pip install -r requirements.txt

WORKDIR /projects/stable-diffution-utils-python

EXPOSE 5000
CMD [ "python", "run.py"]
