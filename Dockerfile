FROM python:3.10
COPY . .
WORKDIR ./
RUN python --version
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5001

CMD ["app.py" ]
ENTRYPOINT ["python3"]