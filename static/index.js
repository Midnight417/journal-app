const darkButton = document.querySelector("#light-dark-button");
const body = document.body;
var darkMode = false;

const theme = localStorage.getItem("theme");
const themeIcon = localStorage.getItem("icon");

if (theme) {
    body.classList.add(theme);
    darkButton.classList.add(themeIcon);
    darkMode = (theme!="light");
} else {
    body.classList.add("light");
    darkButton.classList.add("fa-moon");
}

darkButton.onclick = () => {
    document.documentElement.style.cssText = `
        --modeswap: color 1s ease-in-out, background-color 0.5s ease-in-out, border 0.5s ease-in-out;
    `
    if (darkMode) {
        body.classList.replace("dark", "light");
        localStorage.setItem("theme", "light");
        darkButton.classList.replace("fa-sun", "fa-moon");
        localStorage.setItem("icon", "fa-moon");
    } else {
        body.classList.replace("light", "dark");
        localStorage.setItem("theme", "dark");
        darkButton.classList.replace("fa-moon", "fa-sun");
        localStorage.setItem("icon", "fa-sun");
    }
    darkMode = !darkMode;
};