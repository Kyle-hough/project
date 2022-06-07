async function get_location(city, state) {
    var response = await fetch(`http://api.openweathermap.org/geo/1.0/direct?q=${city},${state},{countrycode}&limit=1&appid=57ba3df4acf884513d99b69e881360bc`);
    var location_data = await response.json();
    console.log(location_data);
    return get_weather(location_data);
}
async function get_weather(location_data) {
    var response = await fetch(`https://api.openweathermap.org/data/2.5/onecall?lat=${location_data['lat']}&lon=${location_data['lon']}&exclude=minutely,hourly,alerts&appid=57ba3df4acf884513d99b69e881360bc=${tempFormat}`);
    var weather_data = await response.json();
    console.log(weather_data);
    return weather_data;}

    