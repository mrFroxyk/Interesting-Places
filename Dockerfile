FROM python:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "collectstatic"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:5001"]

CMD ["gunicorn", "core.wsgi:application", "--workers", "2", "--bind", "0.0.0.0:5001"]

EXPOSE 5001
