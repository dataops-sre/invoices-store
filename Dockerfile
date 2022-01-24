From python:3.8

COPY requirements.txt .

RUN apt-get update && \
	apt-get install -y netcat

RUN pip install --no-cache-dir -r requirements.txt

COPY invoices_store /invoices_store

WORKDIR invoices_store

RUN chmod +x entrypoint.sh

CMD ["/invoices_store/entrypoint.sh"]
