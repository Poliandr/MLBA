FROM python:3.9
WORKDIR /app
COPY ./src/ ./src/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./src/model.py" ]
