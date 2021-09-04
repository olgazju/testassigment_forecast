FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
ENV PYTHONUNBUFFERED=1

# A simple dockerfile to provide gnu netcat.
RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /testassigment_forecast
COPY requirements.txt /testassigment_forecast/
RUN pip install -r requirements.txt

#COPY ./entrypoint.sh /testassigment_forecast/

#RUN chmod +x /testassigment_forecast/entrypoint.sh

#ENTRYPOINT ["/testassigment_forecast/entrypoint.sh"]