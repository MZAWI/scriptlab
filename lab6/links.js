import { checkURL, addUrlToLocalStorage, removeUrlFromLocalStorage } from "./utils.js"

export async function initLinksForm() {
    const inputDesc = document.getElementById("linkDesc");
    const inputUrl = document.getElementById("linkUrl");
    const btnCheck = document.getElementById("btn-check");
    const btnAdd = document.getElementById("btn-add");
    const listContainer = document.getElementById("link-list");

    const defaultLinks = [
        { text: "Dokumentacja MDN", url: "https://developer.mozilla.org" },
        { text: "Jednokostkowy saper", url: "https://onesquareminesweeper.com/" },
        { text: "Fighting AI scrapbots", url: "https://lwn.net/Articles/1008897/" }
    ];

   if (localStorage.getItem("links") === null) {
        localStorage.setItem("links", JSON.stringify(defaultLinks));
    }

    const savedLinks = JSON.parse(localStorage.getItem("links"));
    if (savedLinks) {
    savedLinks.forEach(link => {
        const element = createLinkElement(link.text, link.url);
        listContainer.append(element);
    })
    }

    btnCheck.addEventListener("click", () => {
        const url = inputUrl.value.trim();
        if (!url) return;
        btnCheck.disabled = true;
        checkURL(url).then(() => {
            btnCheck.disabled = false;
        })
    })

    btnAdd.addEventListener("click", () => {
        const desc = inputDesc.value;
        let url = inputUrl.value.trim();
        if (!desc || !url) return;
        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "https://" + url;
        }

        const element = createLinkElement(desc, url);
        listContainer.append(element);
        addUrlToLocalStorage(desc, url);

        inputUrl.value = ""
        inputDesc.value = ""
    })

}

    function createLinkElement(desc, url) {
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.className = "list-group-item list-group-item-action active";

        const header = document.createElement("div");
        header.className = "d-flex w-100 justify-content-between";

        const h5 = document.createElement("h5");
        h5.className = "mb-1";
        h5.append(desc);

        const p = document.createElement("p");
        p.className = "mb-1";
        p.append(url);

        header.append(h5);
        a.append(header, p);
        
        return a;
    }
