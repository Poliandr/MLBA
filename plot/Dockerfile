FROM python:3.9
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
RUN mkdir logs
CMD ["python", "./src/plot.py"]
