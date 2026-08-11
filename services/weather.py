import requests
from datetime import datetime,timedelta,timezone

class WeatherService:
    URL="https://api.open-meteo.com/v1/forecast"
    def get(self,lat,lon):
        params={"latitude":lat,"longitude":lon,
                "hourly":"temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,wind_speed_10m",
                "forecast_days":7,"timezone":"auto"}
        try:
            d=requests.get(self.URL,params=params,timeout=8).json()
            h=d["hourly"]; pts=[]
            for i,t in enumerate(h["time"][:168]):
                pts.append({"time":t,"temperature":h["temperature_2m"][i],
                            "humidity":h["relative_humidity_2m"][i],
                            "rain_probability":h["precipitation_probability"][i],
                            "rainfall":h["precipitation"][i],"wind_speed":h["wind_speed_10m"][i]})
            return {"source":"open-meteo","current":pts[0],"hourly":pts,"latitude":lat,"longitude":lon}
        except Exception:
            return self.demo()
    def demo(self):
        now=datetime.now(timezone.utc).replace(minute=0,second=0,microsecond=0)
        pts=[]
        pattern=[12,10,8,15,25,40,65,78,82,70,45,20,12,8,7,9,11,18,35,62,75,80,55,25]
        for i in range(72):
            rp=pattern[i%len(pattern)]
            pts.append({"time":(now+timedelta(hours=i)).isoformat(),"temperature":28+i%7,
                        "humidity":70+i%10,"rain_probability":rp,
                        "rainfall":2.5 if rp>=65 else 0,"wind_speed":7+i%6})
        return {"source":"demo","current":pts[0],"hourly":pts,"latitude":None,"longitude":None}
