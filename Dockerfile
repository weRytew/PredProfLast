FROM python:3.11-slim
WORKDIR /myApp
COPY requirements.txt /myApp
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /myApp

EXPOSE 5000
CMD ["python", "flask_app.py"]