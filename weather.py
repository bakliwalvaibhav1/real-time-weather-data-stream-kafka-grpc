import datetime, random, time, os
from datetime import datetime, timedelta

def get_next_weather_main():
    start_date = datetime.strptime("2000-01-01", "%Y-%m-%d")

    i = 0
    while True:
        for station in "ABCDEFGHIJ":
            temp = random.gauss(30, 15)
            yield start_date.strftime("%Y-%m-%d"), float(temp), f"Station{station}"
        start_date += timedelta(days=1)
        i += 1

def get_next_weather(delay_sec=1):
    weather_generator = get_next_weather_main()
    while True:
        yield next(weather_generator)
        time.sleep(delay_sec)

if __name__ == "__main__":
    for record in get_next_weather(0.1):
        print(record)
