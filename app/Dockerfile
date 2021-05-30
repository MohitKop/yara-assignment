FROM python:3.9.5-buster

# Make a directory for our application
WORKDIR /app
# Install dependencies
COPY requirements.txt .

RUN pip install awscli
COPY credentials /root/.aws/credentials
COPY config /root/.aws/config

RUN pip install -r requirements.txt

# Copy our source code
COPY . /app

# Run the application
CMD ["python", "api.py"]