FROM python:3.9.14-alpine3.16
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run","--host=0.0.0.0"]