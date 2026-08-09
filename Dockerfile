FROM python:3.13.13

RUN useradd -m magic-script

COPY price-fetch /home/magic-script

RUN cd /home/magic-script && \
	pip install -r requirement.txt
