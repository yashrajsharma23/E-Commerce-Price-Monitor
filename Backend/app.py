from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / 'config/.env'
load_dotenv(dotenv_path=env_path)

cred = credentials.Certificate("config/firebase_pvt_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# It's necessary to import below class after initializing firebase
import module.schedule_job as job
from module.product import Product
from module.user import UserLogin, RegisterUser

app = Flask(__name__)
api = Api(app)
CORS(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


scheduler.add_job(id='notification_job', func=job.product_price_notification, trigger='interval', seconds=300)

api.add_resource(UserLogin, '/login')
api.add_resource(RegisterUser, '/register')
api.add_resource(Product, '/product')

if __name__ == '__main__':
    app.run()
