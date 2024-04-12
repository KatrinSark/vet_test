FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS=ignore
ENV CURL_CA_BUNDLE=""
EXPOSE 8000/tcp
RUN apt-get update -y --no-install-recommends
RUN apt-get install -y --no-install-recommends \
    git `# для установки зависимостей из git` \
    gcc `# для cryptography`
RUN pip install certifi==2021.10.8
RUN mkdir /app
WORKDIR /app/
COPY / /app/
RUN pip install -r requirements.txt
