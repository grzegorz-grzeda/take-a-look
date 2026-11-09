# Throwaway Messenger webhook prototype (issue 0002). Standard library only.
FROM python:3.13-slim

RUN useradd --system --uid 10001 webhook \
 && mkdir /data && chown webhook /data
USER webhook
WORKDIR /app
COPY webhook.py summarize.py ./

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "webhook.py"]
