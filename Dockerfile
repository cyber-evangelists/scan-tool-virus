FROM python:3-slim-buster
# ENV TZ=Asia/Karachi
RUN apt update

RUN apt install clamav -y

RUN freshclam

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9000
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=9000"]