import os

class Config:
    FLIGHTSTATS_APP_ID = os.getenv('FLIGHTSTATS_APP_ID', '8808bb23')
    FLIGHTSTATS_APP_KEY = os.getenv('FLIGHTSTATS_APP_KEY', 'b138ee0863859350ffb19c540be19713')
    MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN', 'sk.eyJ1IjoiZmxkaW52Z3JwIiwiYSI6ImNseHk4ZjdmazNjaWIyam9kcWl0M2IwaTAifQ.mdOrw9b-Xyjp7uLPs12KaA')
