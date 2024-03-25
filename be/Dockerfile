FROM python:3.10
WORKDIR /be
ENV PYTHONPATH "${PYTHONPATH}:/be/app"
COPY ./requirements.txt /be/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /be/requirements.txt
COPY ./.env /be/.env
COPY ./src /be/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]