import requests
import telebot

def Api_calls(city):
    api_key = '87da75f2ddaf4a9d98d42cbf9f96c752'
    geocode = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}')
    data = geocode.json()
    if len(data['results']) > 0:      
        latitude = data['results'][0]['annotations']['DMS']['lat'].split('°')[0]
        longitude = data['results'][0]['annotations']['DMS']['lng'].split('°')[0]
        weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,precipitation')
        country = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={latitude}%2C{longitude}&address_only=1&key={api_key}')
        weather_data = weather.json()
        country_data = country.json()
        country_name = country_data['results'][0]['components']['country']
        temperature = weather_data['current']['temperature_2m']
        temperature_unit = weather_data['current_units']['temperature_2m']
        humidity = weather_data['current']['relative_humidity_2m']
        humidity_unit = weather_data['current_units']['relative_humidity_2m']
        precipitation = weather_data['current']['precipitation']
        precipitation_unit = weather_data['current_units']['precipitation']
        answer = f'Weather data for: {city}, {country_name}\nTemperature: {temperature} {temperature_unit}\nHumidity: {humidity} {humidity_unit}\nPrecipitation: {precipitation} {precipitation_unit}'
        return answer
    else:
        return ("No such city found")

bot = telebot.TeleBot('8027042410:AAE3evkLe6_rOyT_-mmDSLNIH58nfuIfvx8')
@bot.message_handler(commands = ['start'])
def main(message):
    bot.send_message(message.chat.id, 'Выбери город:')
@bot.message_handler()
def info(message):
    bot.reply_to(message, Api_calls(message.text))
bot.polling(none_stop = True)