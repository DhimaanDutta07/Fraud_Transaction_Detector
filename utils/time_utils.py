from datetime import datetime

def get_scaled_time():
    hour = datetime.now().hour
    minute = datetime.now().minute
    scaled = (hour * 60 + minute) / (24 * 60)
    return round(scaled, 4)

def get_time_feature():
    return (datetime.now().hour - 12) / 12