export async function fetchNamedaysPL(){
    const url = "https://nameday.abalin.net/api/V2/today?timezone=Europe/Warsaw"
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error: ${response.status}`);

        return await response.json();
    } catch (error) {
        const response = await fetch("./DanePogoda_Zajęcia-6.json");
        const warnings = await response.json();
        return localWarnings;
    }
}

export function renderCalendarBox(names){
    const box = document.getElementById("calendar-content");
    const today = new Date();
    const weekdayf = today.toLocaleString("pl-PL", { weekday: "long"});
    const datef = today.toLocaleDateString("pl-PL", {
        day: "numeric",
        month: "long",
        year: "numeric"
    });

    const namesArr = names.data.pl.split(",");
    const badges = namesArr.map(name => {
        return `<span class="badge m-1 badge-custom">${name}</span>`
    }).join("");

    document.getElementById("c-weekday").textContent = weekdayf.charAt(0).toUpperCase() + weekdayf.slice(1);
    document.getElementById("c-date").textContent = datef;
    document.getElementById("c-names").innerHTML = badges;

    document.getElementById("calendar-load").classList.add("d-none");
    box.classList.remove("d-none");
    return
}
