FROM harbor.kinmall.lan/public/python:3.6
RUN mkdir /app
COPY wsgi_app.py /app/
WORKDIR /app/
RUN pip install flask
RUN pip install flask_jsonrpc
ENTRYPOINT ["python", "wsgi_app.py"]
