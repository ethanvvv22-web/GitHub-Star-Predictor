#FROM python:3.12.10-slim-bookworm
#
#WORKDIR /app
#
#RUN pip3 install --no-cache-dir Flask requests pandas scikit-learn joblib numpy
#
#COPY . .
#
#ENV FLASK_APP=app.api
#ENV FLASK_RUN_HOST=0.0.0.0
#
#CMD ["flask", "run"]

FROM python:3.12.10-slim-bookworm

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码（包括模型文件）
COPY . .

# 设置 Flask 启动
ENV FLASK_APP=app.api
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run","--host=0.0.0.0", "--port=5000"]