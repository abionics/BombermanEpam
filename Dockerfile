FROM python:3.7-slim
RUN apt-get update
RUN pip install --upgrade pip
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./algorithm /app/algorithm
COPY ./core /app/core
COPY ./graphic /app/graphic
COPY ./sprites /app/sprites
COPY ./act.py /app/act.py
COPY ./config.py /app/config.py
COPY ./main.py /app/main.py
COPY ./solver.py /app/solver.py
CMD python main.py
