FROM ubuntu:latest
FROM python:3.8-buster

RUN pip3 install Flask

RUN useradd -U -m phishy && mkdir -p /home/phishy/static/css /home/phishy/static/images /home/phishy/templates
RUN chown -R root:phishy /home/phishy && chmod 750 /home/phishy

COPY ./3v1l.vbs /home/phishy/3v1l.vbs
COPY ./app.py /home/phishy/app.py
COPY ./siskol.png /home/phishy/siskol.png
COPY ./asik.exe /home/phishy/asik.exe

COPY templates/index.html /home/phishy/templates/index.html
COPY static/css/style.css /home/phishy/static/css/style.css
COPY static/images/gulugulu.jpg /home/phishy/static/images/gulugulu.jpg
COPY static/images/googleavatar.png /home/phishy/static/images/googleavatar.png

WORKDIR /home/phishy
RUN chown -R root:phishy /home/phishy
RUN chmod +x ./malserver.sh

CMD ["flask","run","--host","0.0.0.0","-p","42069"]
