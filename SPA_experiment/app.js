const app = document.getElementById("app");

async function loadPage(path) {
  const route = path === "/" ? "/home.html" : `${path}.html`;
  try {
    const res = await fetch(route);
    if (!res.ok) throw new Error("Page not found");
    const html = await res.text();
    app.innerHTML = html;
  } catch (err) {
    app.innerHTML = "<h1>404 - Page not found</h1>";
  }
}

function handleNavigation(event) {
  if (event.target.matches("[data-link]")) {
    event.preventDefault();
    const path = event.target.getAttribute("href");
    history.pushState({}, "", path);
    loadPage(path);
  }
}

// Handle browser navigation
window.addEventListener("popstate", () => {
  loadPage(location.pathname);
});

// Initial page load
document.addEventListener("DOMContentLoaded", () => {
  document.body.addEventListener("click", handleNavigation);
  loadPage(location.pathname);
});
