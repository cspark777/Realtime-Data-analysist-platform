FROM python:3.7-slim-stretch

RUN apt-get update
 
RUN apt-get install -y --no-install-recommends \
    gcc \
    musl-dev \
    python3-dev \
    build-essential \
    libpq-dev 

RUN apt-get -y install libblas3 liblapack3 liblapack-dev libblas-dev 
RUN apt-get -y install gfortran

RUN pip install numpy
RUN pip install uwsgi
RUN pip install pystan

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /DATA-admin-gui

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /DATA-admin-gui/files

COPY uwsgi.ini .
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
EXPOSE 8000
EXPOSE 8888

RUN date >/build-date.txt

ENTRYPOINT ["bash", "entrypoint.sh"]
