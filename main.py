import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

location = "New Delhi"

app = Flask(__name__)


@app.route("/sms", methods=["POST"])
def sms():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if "weather" in incoming_msg:
        position_api_key = "556e00daaffef61e92d718bbd58b3ff1"
        position_endpoint = "http://api.positionstack.com/v1/forward"
        position_params = {
            "access_key": position_api_key,
            "query": location,
        }

        response = requests.get(position_endpoint, params=position_params)
        latitude = response.json()["data"][0]["latitude"]
        longitude = response.json()["data"][0]["longitude"]

        weather_api_key = "5e973f5b4df7d99b7d106ca7a7b409b1"
        weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": latitude,
            "lon": longitude,
            # "exclude":"current,minutely,hourly",
            "appid": weather_api_key,
            "units": "metric",
        }

        response = requests.get(weather_endpoint, params=weather_params)

        msg.body(
            "Today the Weather is: "
            + response["weather"][0]["main"]
            + "\nCurrent. Teperature: "
            + response["main"]["temp"]
            + "\nFeels Like: "
            + response["main"]["feel_like"]
            + "\nMin. Temp: "
            + response["main"]["temp_min"]
            + "\nMax. Temp: "
            + response["main"]["temp_max"]
        )
        responded = True

    if not responded:
        msg.body("Sorry, I didn't understand")
        responded = True

    return str(resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
