#sudo docker build -t fastapi .

sudo docker run -d --name MyContainer -p 8000:8000 fastapi

#sudo docker run -it --rm -v $PWD/:/app fastapi python /app/app.py
