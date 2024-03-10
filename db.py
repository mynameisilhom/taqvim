from datetime import datetime
import requests
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from keyboards import regions
from config import DATABASE

engine = create_engine(DATABASE, echo=True)
Base = declarative_base()


def fetch_prayer_times(region, month):
    url = "https://islomapi.uz/api/monthly"
    params = {"region": region, "month": month}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from API")
        return None


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    first_name = Column(String(100))
    region = Column(String(100))


class PrayerTime(Base):
    __tablename__ = 'prayer_times'

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(100))
    regionNumber = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    date = Column(Date)
    hijri_month = Column(String(100))
    hijri_day = Column(Integer)
    weekday = Column(String(100))
    tong_saharlik = Column(Time)
    quyosh = Column(Time)
    peshin = Column(Time)
    asr = Column(Time)
    shom_iftor = Column(Time)
    hufton = Column(Time)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def save_prayer_times(prayer_times):
    for prayer_time in prayer_times:
        hijri_month = prayer_time['hijri_date']['month']
        hijri_day = prayer_time['hijri_date']['day']

        # Remove 'Z' character from the ISO format date string
        iso_date_string = prayer_time['date'][:-1]

        prayer = PrayerTime(
            region=prayer_time['region'],
            regionNumber=prayer_time['regionNumber'],
            month=prayer_time['month'],
            day=prayer_time['day'],
            date=datetime.fromisoformat(iso_date_string).date(),
            hijri_month=hijri_month,
            hijri_day=hijri_day,
            weekday=prayer_time['weekday'],
            tong_saharlik=datetime.strptime(prayer_time['times']['tong_saharlik'], '%H:%M').time(),
            quyosh=datetime.strptime(prayer_time['times']['quyosh'], '%H:%M').time(),
            peshin=datetime.strptime(prayer_time['times']['peshin'], '%H:%M').time(),
            asr=datetime.strptime(prayer_time['times']['asr'], '%H:%M').time(),
            shom_iftor=datetime.strptime(prayer_time['times']['shom_iftor'], '%H:%M').time(),
            hufton=datetime.strptime(prayer_time['times']['hufton'], '%H:%M').time()
        )
        session.add(prayer)
    session.commit()


months = [3, 4]

for region in regions:
    for month in months:
        prayer_times_data = fetch_prayer_times(region, month)
        if prayer_times_data:
            save_prayer_times(prayer_times_data)
