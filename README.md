# Orbital-24-Infinity-AI

## RunModel
RunModel is used to test the fine tuned weights  
model weights can be downloaded at https://drive.google.com/drive/folders/1RkVwqAxOW6EiE8vG74a-uc2CuAg51I2d?usp=drive_link

## api
To configure the api add a .env file with the variables and add a link to the database.
database should be called "POSTGRES_URL"
generally follow the frontend's format for the .env file (Jun Kang knows better)

![alt text](https://github.com/neohengkai/Orbital-24-Infinity-AI-dev/blob/main/InfinityGuy.jpg)

## Usage
to launch the api, run these in order

```bash
python manage.py makemigrations
python manage.py migrate --fake
python manage.py runserver
```
note that it is safe to do --fake here as all the data tables should have been initialized by the frontend  
please do check that it has been done before u perform the migrations