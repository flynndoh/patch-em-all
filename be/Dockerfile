FROM python:3.10

WORKDIR /be
ENV PYTHONPATH "${PYTHONPATH}:/be/app"

COPY ./requirements.txt /be/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /be/requirements.txt

COPY ./src /be/app
RUN mkdir /sqlite_data
RUN chmod 777 /sqlite_data

EXPOSE 3030
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3030"]