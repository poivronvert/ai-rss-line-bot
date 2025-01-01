FROM --platform=linux/amd64 python:3.11.9-alpine

# 設定環境變數，避免 Python 生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USER_AGENT=YOUR_USER_AGENT
ENV OPENAI_API_KEY=YOUR_OPENAI_API_KEY
ENV FRONTEND_URL=YOUR_FRONTEND_URL
ENV BACKEND_URL=YOUR_BACKEND_URL
ENV LINE_LOGIN_URI=YOUR_LINE_LOGIN_URI
ENV LINE_MESSAGING_CHANNEL_ACCESS_TOKEN=YOUR_LINE_MESSAGING_CHANNEL_ACCESS_TOKEN
ENV LINE_LOGIN_CHANNEL_ID=YOUR_LINE_LOGIN_CHANNEL_ID
ENV LINE_LOGIN_CHANNEL_SECRET=YOUR_LINE_LOGIN_CHANNEL_SECRET
ENV SESSION_MIDDLEWARE_SECRET=YOUR_SESSION_MIDDLEWARE_SECRET
ENV USER_INFO_TOKEN_SECRET=YOUR_USER_INFO_TOKEN_SECRET
ENV API_TOKEN=YOUR_API_TOKEN
ENV IS_RSS_DB_INITIALIZED=YOUR_IS_RSS_DB_INITIALIZED
ENV DATABASE_USER=YOUR_DATABASE_USER
ENV DATABASE_PASSWORD=YOUR_DATABASE_PASSWORD
ENV DATABASE_HOST=YOUR_DATABASE_HOST
ENV DATABASE_PORT=YOUR_DATABASE_PORT
ENV DATABASE_DB=YOUR_DATABASE_DB
ENV REDIS_HOST=YOUR_REDIS_HOST
ENV REDIS_PORT=YOUR_REDIS_PORT
ENV REDIS_DB=YOUR_REDIS_DB
# 安裝依賴和工具
RUN apk update && \
    apk add --no-cache \
    build-base \
    libffi-dev \
    curl \
    dcron \
    tzdata \
    && cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
    && echo "Asia/Taipei" > /etc/timezone

# 建立工作目錄
WORKDIR /app

# 創建 logs 資料夾
RUN mkdir -p logs

# 複製已打包好的 wheel 檔案到容器
COPY .tmp/my_journalist-*-py3-none-any.whl /app/

# 使用 pip 安裝 wheel 檔案
RUN pip install --no-cache-dir /app/my_journalist-*-py3-none-any.whl

# 複製腳本到bin
COPY script/init_db_script.py /bin/
COPY script/parse_rss_script.py /bin/
COPY script/trigger_broadcast_script.py /bin/
COPY script/docker-entrypoint.sh /bin/

# 設置權限
RUN chmod +x /bin/init_db_script.py
RUN chmod +x /bin/parse_rss_script.py
RUN chmod +x /bin/trigger_broadcast_script.py 
RUN chmod +x /bin/docker-entrypoint.sh

EXPOSE 8000

# 執行應用程式
CMD ["docker-entrypoint.sh"]

