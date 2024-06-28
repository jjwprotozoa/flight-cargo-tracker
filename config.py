import os

class Config:
    TRACKINGMORE_API_KEY = os.environ.get('TRACKINGMORE_API_KEY') or 'fld2md4s-vrr0-5egt-mvbi-3rx546nbx105'
    WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY') or 'b9ec000c25f642d0a5c180924242806'
    MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY') or 'pk.eyJ1IjoiZmxkaW52Z3JwIiwiYSI6ImNscjl2cmw4bDA1eGQya3Q2cThhejEyN2kifQ.K0cDZ_0cUwJktVaAQZm1pA'