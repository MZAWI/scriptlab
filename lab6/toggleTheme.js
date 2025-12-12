export function initTheme() {
    const themeToggle = document.getElementById("theme-toggle");
    const html = document.documentElement;
    if (localStorage.getItem("theme") === "light") {
        document.documentElement.setAttribute("data-theme", "light");
    }

    const setLight = () => {
        html.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
        themeToggle.checked = false;
    }

    const setDark = () => {
        html.removeAttribute("data-theme");
        localStorage.setItem("theme", "dark");
        themeToggle.checked = true;
    };

    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light") {
        setLight();
    } 
    else {
        setDark();
    }


    themeToggle.addEventListener("change", event => {
        if (event.target.checked) {
            setDark();
        } else {
            setLight();
        }
    });
}
