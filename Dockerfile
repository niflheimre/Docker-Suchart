FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/

RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html --default-timeout=100
RUN pip install simpletransformers --default-timeout=100

RUN pip install -r requirements.txt --default-timeout=100

COPY . /code/

CMD python manage.py runserver 0.0.0.0:$PORT
