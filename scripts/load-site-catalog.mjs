// Reads window.LIBRARY from a built site (_site) the same way the home page does: it runs the catalog
// scripts that index.html loads, in the same order, inside a small sandbox. Used by the post-integration
// deploy steps (build-integrated-unit-pages.mjs, add-site-header.mjs, test-site-hygiene.mjs).
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const CATALOG_SCRIPT = /^(data|course-integrations|unit-specific-arcade|resource-details|course-catalog|unit-generator-cards|grade\d-main-catalog|grade\d\/grade\d-main-catalog)\.js$/;

export function loadSiteCatalog(OUT, { siteUrl = "https://mrksclassroom.com/", quiet = false } = {}) {
  const indexHtml = fs.readFileSync(path.join(OUT, "index.html"), "utf8");
  const scripts = [...indexHtml.matchAll(/<script[^>]+src="([^"]+)"/g)]
    .map((m) => m[1].split("?")[0].replace(/^\.?\//, ""))
    .filter((src) => CATALOG_SCRIPT.test(src));
  const noop = () => {};
  const element = () => ({ setAttribute: noop, appendChild: noop, addEventListener: noop, style: {}, classList: { add: noop, remove: noop, toggle: noop } });
  const store = new Map();
  const sandbox = {
    console: { log: noop, info: noop, warn: noop, error: noop },
    location: { href: siteUrl, origin: siteUrl.replace(/\/$/, ""), pathname: "/", search: "", hash: "" },
    localStorage: { getItem: (k) => store.get(k) ?? null, setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k) },
    navigator: { userAgent: "node" },
    URL, URLSearchParams, setTimeout: noop, clearTimeout: noop, queueMicrotask: noop,
  };
  sandbox.window = sandbox; sandbox.self = sandbox; sandbox.globalThis = sandbox;
  sandbox.document = {
    readyState: "complete", currentScript: { src: siteUrl + "index.js" }, documentElement: element(), body: element(), head: element(),
    addEventListener: noop, removeEventListener: noop, querySelector: () => null, querySelectorAll: () => [],
    getElementById: () => null, createElement: element,
  };
  sandbox.addEventListener = noop;
  vm.createContext(sandbox);
  const problems = [];
  for (const src of scripts) {
    const file = path.join(OUT, src);
    if (!fs.existsSync(file)) { problems.push("not found: " + src); continue; }
    try { vm.runInContext(fs.readFileSync(file, "utf8"), sandbox, { filename: src, timeout: 10000 }); }
    catch (e) { problems.push(src + ": " + e.message); }
  }
  if (!quiet) for (const p of problems) console.warn("Catalog script skipped (" + p + ")");
  const library = sandbox.LIBRARY || sandbox.window.LIBRARY;
  if (!library || !Array.isArray(library.courses)) throw Error("window.LIBRARY was not found after loading " + scripts.join(", "));
  return { library, scripts, problems };
}

// "grade3/artifacts/x/index.html?y=1#z" -> "grade3/artifacts/x/index.html"; folders get index.html.
export function sitePath(p) {
  let s = String(p || "").split("#")[0].split("?")[0].replace(/^\.?\//, "").replace(/^\/+/, "");
  try { s = decodeURIComponent(s); } catch { /* keep as is */ }
  if (!s || s.endsWith("/")) s += "index.html";
  return s;
}
