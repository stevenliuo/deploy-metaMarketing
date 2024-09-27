FROM python:3.11

RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN chmod +x entrypoint.sh
ENV PROFILE=prod
ENTRYPOINT ["bash","/app/entrypoint.sh"]