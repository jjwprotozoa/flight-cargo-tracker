import os

class Config:
    TRACKINGMORE_API_KEY = os.environ.get('TRACKINGMORE_API_KEY') or 'fld2md4s-vrr0-5egt-mvbi-3rx546nbx105'
    WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY') or 'yhttps://api.weatherapi.com/v1/current.json?q=32827&lang=1087'
    MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY') or 'sk.eyJ1IjoiZmxkaW52Z3JwIiwiYSI6ImNseHk4ZjdmazNjaWIyam9kcWl0M2IwaTAifQ.mdOrw9b-Xyjp7uLPs12KaA'