FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 暴露埠口
EXPOSE 5001

ENV PORT=5001
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
