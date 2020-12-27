document.querySelectorAll(".section-header").forEach(function (item) {
    item.addEventListener("click", dropdown)
})

document.querySelectorAll(".entry").forEach(function (item) {
    item.addEventListener("mouseleave", dontdelete)
    item.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    }, false);
    item.addEventListener("contextmenu", deleteentry)
})

document.querySelectorAll(".entry-icon").forEach(function (item) {
    item.addEventListener("click", function (e) {
        if (!confirm('Are sure you want to delete this entry? It will be gone forever...')) {
            e.preventDefault();
        }
    }, false);
})

function dropdown() {
    selected = this.getAttribute("data-section");
    document.querySelectorAll("[data-section='" + selected + "-entry']").forEach(function (item) {
        if (item.style.display == "none") {
            //display entries
            item.style.display = "flex";
            document.querySelector("[data-section='" + selected + "'] i").style.transform = "rotate(0deg)"
        }
        else {
            //hide entries
            item.style.display = "none";
            document.querySelector("[data-section='" + selected + "'] i").style.transform = "rotate(90deg)"
        }
    });
}

function deleteentry() {
    document.documentElement.style.cssText = `
        --modeswap: color 1s ease-in-out, background-color 0.5s ease-in-out, border 0.5s ease-in-out;
    `
    selected = document.querySelector("[data-id='" + this.getAttribute("data-id") + "'] i")
    button = document.querySelector("[data-id='" + this.getAttribute("data-id") + "'] button")
    if (selected.classList.contains("fa-book")) {
        selected.classList.replace("fa-book", "fa-trash-alt");
        button.disabled = false;
    } else {
        selected.classList.replace("fa-trash-alt", "fa-book");
        button.disabled = true;
    }
}

function dontdelete() {
    selected = document.querySelector("[data-id='" + this.getAttribute("data-id") + "'] i")
    selected.classList.replace("fa-trash-alt", "fa-book");
    button.disabled = true;
}

var entries;

function pass(list) {
    entries = list;
    for (i = 0; i < entries.length; i++) {
        document.querySelector("[data-id='" + entries[i]['id'] + "']").onclick = loadentry;
    }
}

function loadentry() {
    let id = this.getAttribute("data-id");
    for (i = 0; i < entries.length; i++) {
        if (entries[i]["id"] == id) {
            //change journal content
            document.querySelector("#journal-title").value = entries[i]["title"];
            document.querySelector("#journal-id").value = entries[i]["id"];
            document.querySelector("#journal-text").innerHTML = entries[i]["entry"];

            //change modeswap time
            document.documentElement.style.cssText = `
                --modeswap: color 1s ease-in-out, background-color 0.5s ease-in-out;
            `

            //change color of selected
            document.querySelectorAll(".entry").forEach(function (item) {
                let display = item.style.display;
                item.style.cssText = `background-color: var(--background);`
                item.style.display = display;
            });
            this.style.cssText = `background-color: var(--selected-background);`
            break;
        }
    }
    if (document.querySelector(".empty-area").style.display != "flex") {
        document.querySelector(".empty-area").style.display = "none";
        document.querySelector(".journal-area").style.display = "flex";
    }
}
