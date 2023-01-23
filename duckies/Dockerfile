FROM ubuntu:18.04

# ENV DEBIAN_FRONTEND noninteractive
# ENV LANG="C.UTF-8"
# ENV LC_ALL="C.UTF-8"

RUN apt update -qq
RUN apt-get install -y gpg-agent
RUN apt install -y --no-install-recommends software-properties-common dirmngr

RUN apt update && apt install -y --no-install-recommends \
	build-essential \
	curl \
	gawk \
	git \
	nano \
	openssh-client \
	sudo \
	texlive-base \
	texlive-bibtex-extra \
	texlive-fonts-recommended \
	texlive-generic-extra \
	texlive-latex-extra \
	texlive-publishers

# Copies files for the python solver
COPY ./src/report.tex /src/report.tex

# Start image
FROM python:3.9.13

# Define starting directory
WORKDIR /src

# Copy requirements for python
COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copies files for the python solver
COPY ./src/Excel_Solver.py /src/Excel_Solver.py
COPY ./src/historical_sales_data.xls /src/historical_sales_data.xls
COPY ./src/bathing_friends_unlimited.xls /src/bathing_friends_unlimited.xls

# Copy files for the report
COPY ./src/report.tex /src/report.tex

# Specify starting command
 CMD [ "python", "Excel_Solver.py"]
