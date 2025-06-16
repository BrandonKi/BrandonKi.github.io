const app = document.getElementById("app");

async function loadPage(path) {
    const route = path === "/" ? "/home.html" : `${path}.html`;
    console.log(route);
    let res;
    try {
        res = await fetch(route);
        if (!res.ok) throw new Error("Page not found");
    } catch (err) {
        console.error(err);
        app.innerHTML = "<h1>404 - Page not found</h1>";
        return;
    }

    const html = await res.text();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html;

    // HACK
    // can I instead just dedup and rerun the scripts?
    // everything gets reloaded and appended to the body without this
    const scriptTag = document.body.querySelector('script[src="app.js"]');
    if (scriptTag) {
        // Remove everything after <script src="app.js"> in the wrapper
        let next = scriptTag.nextSibling;
        while (next) {
          const toRemove = next;
          next = next.nextSibling;
          toRemove.parentNode.removeChild(toRemove);
        }
    }

    // Dynamically run <script> tags
    wrapper.querySelectorAll('script').forEach(oldScript => {
        console.log("Running script:", oldScript.src || oldScript.textContent);
        const newScript = document.createElement('script');
        if (oldScript.src) {
            newScript.src = oldScript.src;
        } else {
            newScript.textContent = oldScript.textContent;
        }
        document.body.appendChild(newScript);
    });

    // Replace content (excluding script tags)
    const app = document.getElementById('app');
    app.innerHTML = '';
    wrapper.childNodes.forEach(node => {
        if (node.tagName !== 'SCRIPT')
            app.appendChild(node.cloneNode(true));
    });
}

const loadedScripts = new Set();

function handleNavigation(event) {
    console.log("Handling navigation for:", event.target);
    let target = event.target;
    if (target.classList.contains("blog-tag-x")) {
        console.log("Blog tag clicked:", target);
        event.preventDefault();
        target.parentNode.dispatchEvent(new Event("click", { bubbles: true, cancelable: true }));
    }
    else if (event.target.matches("[data-link]")) {
        console.log("Data link clicked:", event.target);
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
