FROM python:3.14 
WORKDIR /app 

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./src
EXPOSE 8080 

RUN useradd app 
USER app 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"] 
