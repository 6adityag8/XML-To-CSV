# Base Image
FROM python:3.6

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# set AWS credentials
ENV AWS_ACCESS_KEY ''
ENV AWS_SECRET_KEY ''
ENV S3_BUCKET_NAME ''

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install project dependencies
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

CMD python xml_to_csv.py