// js/utils.js
// Pomocnicze funkcje JavaScript

// Funkcja sprawdzająca dostępność URL (HEAD)
// Użycie: import { checkURL } from "./js/utils.js";
//Wywołanie:
// Zdarzenie kliknięcia przycisku Sprawdź URL
/*
const checkUrlBtn = document.querySelector("#checkUrlBtn");
checkUrlBtn.addEventListener("click", async () => {
  const url = inputURL.value;
  checkURL(url); //wywołanie funkcji
});
*/

export async function checkURL(url, timeout = 3000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      method: "HEAD",
      mode: "no-cors",
      signal: controller.signal
    });

    clearTimeout(id);
    alert("URL jest dostępny.");
  } catch (error) {
    alert("URL jest niedostępny.");
  }
}

// Funkcja do dodawania linku do localStorage
// Użycie: import { addUrlToLocalStorage } from "./js/utils.js";
// Wywołanie:
// addUrlToLocalStorage(text, url);
// gdzie text to opis linku, a url to adres URL

export function addUrlToLocalStorage(text, url) {
  const normalizedUrl = new URL(url).href;

  let links = JSON.parse(localStorage.getItem("links")) || [];
  links.push({ text, url: normalizedUrl });

  localStorage.setItem("links", JSON.stringify(links));
}

//Funkcja usuwania linku z localStorage
// Użycie: import { removeUrlFromLocalStorage } from "./js/utils.js";
// Wywołanie:
// removeUrlFromLocalStorage(taskLi);
// gdzie taskLi to element listy (li) zawierający link do usunięcia

export function removeUrlFromLocalStorage(taskLi) {
  const text = taskLi.querySelector("input").value;
  const url = taskLi.querySelector("a").href;
  let links = JSON.parse(localStorage.getItem("links")) || [];
  links = links.filter(link => !(link.text === text && link.url === url));
  localStorage.setItem("links", JSON.stringify(links));
}
