
import os,json
class AdvisoryEngine:
    def __init__(self):
        path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"data","guidance.json")
        self.data=json.load(open(path,encoding="utf-8"))
    def score(self,w):
        rain=float(w.get("rain_probability",0)); wind=float(w.get("wind_speed",0)); temp=float(w.get("temperature",0))
        s=100; reasons=[]
        if rain>=70:s-=55;reasons.append("High rain probability")
        elif rain>=40:s-=25;reasons.append("Moderate rain probability")
        else:reasons.append("Low rain probability")
        if wind>=25:s-=30;reasons.append("Strong wind")
        elif wind>=15:s-=12;reasons.append("Moderate wind")
        if temp>=35:s-=20;reasons.append("High temperature")
        elif temp>=32:s-=8;reasons.append("Warm conditions")
        return max(0,min(100,s)),reasons
    def build(self,pred,wx):
        current=wx["current"]; score,reasons=self.score(current)
        window=None
        for p in wx["hourly"][1:72]:
            sc,_=self.score(p)
            if sc>=75:
                window={"start":p["time"],"score":sc,"rain_probability":p["rain_probability"],
                        "temperature":p["temperature"],"wind_speed":p["wind_speed"]};break
        if pred["confidence"]<50:
            action="VERIFY";headline="Verify the crop condition before acting."
        elif score>=75: action="ACT";headline="Weather is favorable for the next planned field action."
        elif score>=45: action="CAUTION";headline="Conditions are marginal — re-check before acting."
        else: action="WAIT";headline="Wait — current weather is unfavorable."
        key=pred["disease"].lower().replace(" ","_")
        guidance=self.data.get(key,self.data["unknown"])
        return {
          "decision":{"action":action,"headline":headline,"score":score,"reasons":reasons,"next_window":window},
          "guidance":guidance,
          "climate_risk":self.risk(wx["hourly"][:24]),
          "farmer_message":self.message(pred,action,window),
          "sources":guidance.get("sources",[])
        }
    def risk(self,pts):
        h=sum(x["humidity"] for x in pts)/len(pts) if pts else 0
        r=max([x["rain_probability"] for x in pts],default=0)
        disease="high" if h>=75 and r>=60 else "moderate" if h>=70 or r>=40 else "low"
        heat="high" if max([x["temperature"] for x in pts],default=0)>=35 else "low"
        overall="high" if disease=="high" or heat=="high" else "moderate" if disease=="moderate" else "low"
        return {"disease_pressure":disease,"heat_stress":heat,"overall":overall}
    def message(self,p,a,w):
        if p["confidence"]<50:return "ఈ చిత్రంపై ఆధారపడి వెంటనే చికిత్స నిర్ణయం తీసుకోకండి. స్పష్టమైన ఫోటో తీసి మళ్లీ పరిశీలించండి."
        if a=="WAIT":return "ప్రస్తుత వాతావరణం అనుకూలంగా లేదు. తదుపరి అనుకూల సమయాన్ని పరిశీలించండి."
        if a=="ACT":return f"{p['disease']} అనేది ప్రధాన AI అంచనా. ప్రస్తుత వాతావరణం అనుకూలంగా ఉంది. స్థానికంగా ఆమోదించబడిన వ్యవసాయ సూచనలను అనుసరించండి."
        return f"{p['disease']} అనేది ప్రధాన AI అంచనా. నిర్ణయం తీసుకునే ముందు వాతావరణాన్ని మళ్లీ పరిశీలించండి."
