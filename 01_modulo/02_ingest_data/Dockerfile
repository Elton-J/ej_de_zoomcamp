FROM python:3.9

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
RUN curl -k -fsSL https://www.amazontrust.com/repository/AmazonRootCA1.pem -o /usr/local/share/ca-certificates/amazon-root-ca1.crt && update-ca-certificates

RUN pip install pandas sqlalchemy psycopg2 pyarrow requests --no-cache-dir --upgrade certifi

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]