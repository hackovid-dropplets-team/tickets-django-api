FROM python:3.7

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
# ENV PYTHONUNBUFFERED 1

COPY . /project
WORKDIR /project

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /project/requirements.txt

CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn tickets_project.wsgi --timeout 60 -b 0.0.0.0:8000"]