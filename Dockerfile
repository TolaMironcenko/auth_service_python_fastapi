FROM python:3.12-alpine

WORKDIR /auth_service
COPY . /auth_service/
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["fastapi", "run", "/auth_service/main.py"]
