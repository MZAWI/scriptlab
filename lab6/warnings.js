export async function fetchWarningsMeteo(){
    const url = "https://danepubliczne.imgw.pl/api/data/warningsmeteo"
    try {
        const response = await fetch(url);
        const warnings = await response.json();
        if (warnings.status = "false") {
            throw new Error('No data to display');
        }
        return warnings;
    } catch (error) {
        console.error("Warning: ", error);
        const localResponse = await fetch("./DaneOstrzezenia_Zajęcia-6.json");
        const localWarnings = await localResponse.json();
        return localWarnings;
        }
    }
}

export function renderWarningsMeteo(warnings) {
    const container = document.getElementById("warnings-content");
    if (!container) return;
    if (!warnings || warnings.length === 0) {
        container.innerHTML = "<div class='alert alert-info'>Brak aktualnych ostrzeżeń meteorologicznych.</div>";
        return ;
    }

    const warn_cards = warnings.map(w => {
        return `
        <div class="card-text">
        <div class="row row-cols-2 mb-3">
            <h2 class="w-name col-12"><span class="badge badge-warning">${w.nazwa_zdarzenia}</span></h2>
            <div class="warn-description col-12"> ${w.tresc}</div>
            <div class="col-12"> <strong>Biuro:</strong> ${w.biuro}</div>
            <div class="col"> <strong>Stopień:</strong> ${w.stopien}</div>
            <div class="col"> <strong>Prawdopodobieństwo:</strong> ${w.prawdopodobienstwo}% </div>
            <div class="col"> <strong>Od:</strong> ${w.obowiazuje_od}</div>
            <div class="col"> <strong>Do:</strong> ${w.obowiazuje_do}</div>
            <div class="col"> <strong>Komentarz:</strong> ${w.komentarz}</div>
            <div class="col"> <strong>Liczba powiatów:</strong> ${w.teryt.length}</div>
        </div>
            <hr></hr>
        </div>
        `
    }).join("")

    container.innerHTML = warn_cards;
}

