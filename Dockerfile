# Base image
FROM python:3.6

MAINTAINER torgaeva.ksenia

RUN ls
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
