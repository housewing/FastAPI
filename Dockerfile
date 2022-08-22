# buster version for debian 10
FROM python:3.8-slim-buster

EXPOSE 8000

WORKDIR /fastAPI

COPY ./requirements.txt /fastAPI/requirements.txt

# install mssql driver
RUN apt-get update && apt-get install -y gcc curl gnupg unixodbc-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql18
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# install python requirement module
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /fastAPI/requirements.txt

COPY ./.env /fastAPI
COPY ./__init__.py /fastAPI
COPY ./main.py /fastAPI
COPY ./config/ /fastAPI/config/
COPY ./router/ /fastAPI/router/
COPY ./model/ /fastAPI/model/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

