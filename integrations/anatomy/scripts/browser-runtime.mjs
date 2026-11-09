import { accessSync, constants, existsSync, readdirSync } from "node:fs";
import { homedir } from "node:os";
import { delimiter, join } from "node:path";

function executable(path) {
  if (!path) return false;
  try {
    accessSync(path, process.platform === "win32" ? constants.F_OK : constants.X_OK);
    return true;
  } catch {
    return false;
  }
}

export function chromePath() {
  if (process.env.CHROME_PATH) {
    if (!executable(process.env.CHROME_PATH)) throw new Error("CHROME_PATH must name an executable Chrome or Chromium binary.");
    return process.env.CHROME_PATH;
  }
  const names = process.platform === "win32" ? ["chrome.exe", "chromium.exe"] : ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"];
  const candidates = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/opt/google/chrome/chrome",
    ...[process.env.PROGRAMFILES, process.env["PROGRAMFILES(X86)"], process.env.LOCALAPPDATA].filter(Boolean).map((root) => join(root, "Google", "Chrome", "Application", "chrome.exe")),
    ...(process.env.PATH || "").split(delimiter).filter(Boolean).flatMap((root) => names.map((name) => join(root, name))),
  ];
  const roots = [
    process.env.PLAYWRIGHT_BROWSERS_PATH === "0" ? null : process.env.PLAYWRIGHT_BROWSERS_PATH,
    join(homedir(), ".cache", "ms-playwright"),
    join(homedir(), "Library", "Caches", "ms-playwright"),
    process.env.LOCALAPPDATA ? join(process.env.LOCALAPPDATA, "ms-playwright") : null,
    process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, "playwright-core", ".local-browsers") : null,
    "/ms-playwright",
    "/opt/ms-playwright",
    "/opt/pw-browsers",
  ].filter(Boolean);
  for (const root of new Set(roots)) {
    if (!existsSync(root)) continue;
    let entries;
    try {
      entries = readdirSync(root, { withFileTypes: true }).filter((entry) => entry.isDirectory() && /^chromium(?:_headless_shell)?-\d+$/.test(entry.name)).map((entry) => entry.name).sort((a, b) => b.localeCompare(a, undefined, { numeric: true }));
    } catch {
      continue;
    }
    for (const entry of entries) {
      for (const sub of [
        "chrome-linux64/chrome",
        "chrome-linux/chrome",
        "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        "chrome-win64/chrome.exe",
        "chrome-win/chrome.exe",
        "chrome-headless-shell-linux64/chrome-headless-shell",
        "chrome-linux/headless_shell",
      ]) candidates.push(join(root, entry, sub));
    }
  }
  const found = candidates.find(executable);
  if (!found) throw new Error("No Chrome found. Set CHROME_PATH to an executable Chrome or Chromium binary.");
  return found;
}

export function chromeFlags(profile) {
  return [
    "--headless=new",
    "--remote-debugging-port=0",
    `--user-data-dir=${profile}`,
    "--no-first-run",
    "--no-default-browser-check",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--enable-unsafe-swiftshader",
    "--ignore-gpu-blocklist",
    ...(process.platform === "linux" ? ["--disable-dev-shm-usage"] : []),
    ...(process.platform === "linux" && process.getuid?.() === 0 ? ["--no-sandbox"] : []),
    "about:blank",
  ];
}
