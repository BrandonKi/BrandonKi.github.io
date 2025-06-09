const app = document.getElementById("app");

async function loadPage(path) {
    const route = path === "/" ? "/home.html" : `${path}.html`;
    console.log(route);
    try {
        const res = await fetch(route);
        if (!res.ok) throw new Error("Page not found");
        app.innerHTML = await res.text();
    } catch (err) {
        console.error(err);
        app.innerHTML = "<h1>404 - Page not found</h1>";
    }
}

function handleNavigation(event) {
    let target = event.target;
    if (target.classList.contains("blog-tag-x")) {
        event.preventDefault();
        target.parentNode.dispatchEvent(new Event("click", { bubbles: true, cancelable: true }));
    }
    else if (event.target.matches("[data-link]")) {
        event.preventDefault();
        const path = event.target.getAttribute("href");
        history.pushState({}, "", path);
        loadPage(path);
    }
}

window.addEventListener("popstate", () => {
    loadPage(location.pathname);
});

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", handleNavigation);
    loadPage(location.pathname);
});
