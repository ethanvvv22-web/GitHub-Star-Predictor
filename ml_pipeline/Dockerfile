FROM python:3.12.10-slim-bookworm

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["sh", "-c", "python3 src/preprocess.py && pytho cn3 src/train_models.py && python3 src/evaluate.py"]