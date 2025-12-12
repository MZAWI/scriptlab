export async function fetchWeatherIMGW(location) {
    try {
        const url = "https://danepubliczne.imgw.pl/api/data/synop/station/" + location
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        const response = await fetch("./DanePogoda_Zajęcia-6.json");
        const data = await response.json();
        return data;
    }; 
}

export function renderWeatherBoxIMGW(weather) {
    const box = document.getElementById("weather-content");
    document.getElementById('w-city').textContent = weather.stacja;
    document.getElementById('w-temp').textContent = weather.temperatura;
    document.getElementById('w-wind').textContent = weather.predkosc_wiatru;
    document.getElementById('w-rain').textContent = weather.suma_opadu;
    document.getElementById('w-humidity').textContent = weather.wilgotnosc_wzgledna;
    document.getElementById('w-pressure').textContent = weather.cisnienie;

    document.getElementById('weather-load').classList.add('d-none');
    document.getElementById('weather-content').classList.remove('d-none');
    return
}


