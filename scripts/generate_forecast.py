import os
import json
import itertools
from datetime import datetime
from openai import OpenAI
from astropy.coordinates import get_body, GeocentricTrueEcliptic
from astropy.time import Time
import astropy.units as u
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Set it in .env file or as environment variable.")

client = OpenAI(api_key=api_key)

today = datetime.utcnow()
date_str = today.strftime("%d%m%Y%H")
output_path = f"data/{date_str}.json"

zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def degree_to_sign(deg):
    return zodiac_signs[int(deg // 30)]

def aspect_between(lon1, lon2, orb=6):
    diff = abs(lon1 - lon2)
    diff = diff if diff <= 180 else 360 - diff
    
    aspect_angles = {
        "conjunction": 0,
        "sextile": 60,
        "square": 90,
        "trine": 120,
        "opposition": 180
    }
    
    for name, angle in aspect_angles.items():
        if abs(diff - angle) < orb:
            return name
    return None

def check_retrograde(body, date):
    t1 = Time(date)
    t2 = Time(date) + 1 * u.day
    
    pos1 = get_body(body, t1).transform_to(GeocentricTrueEcliptic()).lon.deg % 360
    pos2 = get_body(body, t2).transform_to(GeocentricTrueEcliptic()).lon.deg % 360
    
    diff = (pos2 - pos1) % 360
    return diff > 180

date = Time(today.strftime("%Y-%m-%d"))
bodies = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]
planets = {}

for body in bodies:
    sc = get_body(body, date)
    ecl = sc.transform_to(GeocentricTrueEcliptic())
    lon = ecl.lon.deg % 360
    planets[body] = lon

planetary_info = []
for body in bodies:
    lon = planets[body]
    sign = degree_to_sign(lon)
    info = f"{body.title()} in {sign}"
    
    if body in ["mercury", "venus"] and check_retrograde(body, date):
        info += " (retrograde)"
    
    planetary_info.append(info)

aspects = []
for (p1, lon1), (p2, lon2) in itertools.combinations(planets.items(), 2):
    asp = aspect_between(lon1, lon2)
    if asp:
        aspects.append(f"{p1.title()} {asp} {p2.title()}")

planetary_data = ", ".join(planetary_info[:3]) + ". " + ", ".join(aspects[:5])

system_prompt = """You are Moonalyzer, a cosmic crypto analyst who blends astrology and market intuition. 
Each day, you analyze planetary transits to forecast the mood of the crypto market. 
Your tone is witty, confident, and slightly mystical — like a trader who reads both charts and stars.
Always output concise, structured results:
1. A one-sentence global market mood.
2. A short justification referencing planetary positions.
3. Individual signals for BTC, ETH, and ALTCOINS (each marked ↑ or ↓ with an emoji and reason).
Avoid disclaimers. Keep the vibe fun but coherent.
Output valid JSON only, following this schema:
{
  "date": "YYYY-MM-DD",
  "market_mood": "...",
  "astro_justification": "...",
  "signals": {
    "BTC": {"direction": "...", "emoji": "...", "reason": "..."},
    "ETH": {"direction": "...", "emoji": "...", "reason": "..."},
    "ALTS": {"direction": "...", "emoji": "...", "reason": "..."}
  },
  "quote": "..."
}"""

user_prompt = f"Today's planetary data: {planetary_data}\n\nGenerate Moonalyzer's forecast for the day."

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    response_format={"type": "json_object"}
)

forecast = json.loads(resp.choices[0].message.content)
forecast["date"] = today.strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)
with open(output_path, "w") as f:
    json.dump(forecast, f, indent=2)

with open("data/latest.json", "w") as f:
    json.dump(forecast, f, indent=2)

print(f"Saved forecast to {output_path} and data/latest.json")
