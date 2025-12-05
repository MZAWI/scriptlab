// main.js
// Główny plik aplikacji
// Importujemy funkcje z modułów
// Pogoda, Ostrzeżenia, Imieniny, Linki
import { fetchWeatherIMGW, renderWeatherBoxIMGW } from "./weather.js";
import { fetchWarningsMeteo, renderWarningsMeteo } from "./warnings.js";
import { fetchNamedaysPL, renderCalendarBox } from "./namedays.js";
import { initLinksForm } from "./links.js";
import { initTheme } from "./toggleTheme.js";

async function main() {
    initTheme();
    // 1. Pogoda
    const weather = await fetchWeatherIMGW("krakow");
    renderWeatherBoxIMGW(weather);

    setInterval(async () => {
        renderWeatherBoxIMGW(await fetchWeatherIMGW("krakow"))
    }, 30 * 1000 * 60);

    // 2. Ostrzeżenia IMGW
    const warnings = await fetchWarningsMeteo();
    renderWarningsMeteo(warnings);

    // 3. Imieniny
    const names = await fetchNamedaysPL();
    renderCalendarBox(names);

    // 4. Formularz URL
    initLinksForm();
}

main();
