FROM python:3-slim-buster
<<<<<<< HEAD
=======
# ENV TZ=Asia/Karachi
RUN apt update

RUN apt install clamav -y

RUN freshclam
>>>>>>> c18931cd379c94ab8ef653a2d07b3d6f15040e9e

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9000
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=9000"]