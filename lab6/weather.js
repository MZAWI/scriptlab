export async function fetchWeatherIMGW(location) {
    const url = "https://danepubliczne.imgw.pl/api/data/synop/station/" + location
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error: ${response.status}`);

        return await response.json();
    } catch (error) {
        console.error("Error: ", error);
        return null;
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


