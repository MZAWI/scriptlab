export function initTheme() {
    const themeToggle = document.getElementById("theme-toggle");
    const html = document.documentElement;

    const setLight = () => {
        html.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    }

    const setDark = () => {
        html.removeAttribute("data-theme");
        localStorage.setItem("theme", "dark");
    };

    if (localStorage.getItem("theme") === "light") {
        setLight();
    }

    themeToggle.addEventListener("change", event => {
        if (event.target.checked) {
            setDark();
        } else {
            setLight();
        }
    });
}
