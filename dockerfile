FROM python:3.11.8
ENV TOKEN="your TOKEN" 
ENV NGROK_URL = "YOUR_WEBHOOK_URL"
ENV HOST = '127.0.0.1'
ENV PORT = 80
WORKDIR /bot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]