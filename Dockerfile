FROM ubuntu:22.04

# Environmental variables
ENV ENVIRONMENT="prod"
ENV TZ="Europe/Warsaw"

ENV DB_Address="tn_database"
ENV DB_Port="5432"
ENV DB_Name="TravelNest"
ENV DB_Username="tn_api_write"
ENV DB_Password="cba"

ENV EMAIL_ADDRESS="travelnest2407@gmail.com"
ENV EMAIL_PASS="ssym dqry bsdz nlzd"
ENV LOGO_HTTPS_PATH="https://lh3.googleusercontent.com/d/1fBRxFZ_CbRr99CYcK89wAqAmr4PVbdKE"
ENV INVOICE_DEST_PATH="/usr/INVOICES"
ENV INVOICE_TEMPLATE_PATH="src/model/templates/INVOICE/Invoice_template.docx"

# install ubuntu pakages
RUN apt update
RUN apt install -y python3-dev
RUN apt install -y pip
RUN apt install -y gcc libpcre3-dev libpcre3

# set timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

# set working dir directory
WORKDIR /App
COPY . /App

# install python packages
RUN pip install -r requirements.txt

# create directory for logs
RUN mkdir /var/log/flask-app

CMD ["uwsgi", "--ini", "./wsgi.ini"]