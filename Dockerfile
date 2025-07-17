FROM python:3.11-alpine3.22  

LABEL maintainer="R.LAB <n@rlab.ru>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./back/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./back/*.py /app
COPY ./front/dist /public

EXPOSE 1406 

ENV STATIC_ROOT="/public"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1406"]
