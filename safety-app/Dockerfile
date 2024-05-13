FROM python:3-onbuild

WORKDIR /var/app
COPY . .
COPY requirements.txt .
COPY safety_data.csv .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4100

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:4100", "--timeout","120", "--config","gunicorn_conf.py"]
