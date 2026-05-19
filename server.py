from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from urllib.parse import unquote
from urllib.request import Request, urlopen


WORKSPACE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parent / "www.adamhartwig.co.uk"
PORT = 8000
APP_ROUTES = {"/", "/about", "/skills", "/work-and-play", "/awards", "/contact"}
ROOT_RESOLVED = ROOT.resolve()
WORKSPACE_RESOLVED = WORKSPACE.resolve()
CACHE_ROOT = WORKSPACE_RESOLVED / ".remote-cache"
REMOTE_ORIGIN = "https://www.adamhartwig.co.uk"
PID_FILE = WORKSPACE_RESOLVED / "server.pid"


def find_matching_file(relative_path):
    clean_relative = relative_path.strip("/\\")
    relative_obj = Path(clean_relative) if clean_relative else Path()
    candidate_paths = []

    if clean_relative:
        candidate_paths.extend([
            ROOT_RESOLVED / relative_obj,
            WORKSPACE_RESOLVED / relative_obj,
        ])
    else:
        candidate_paths.append(ROOT_RESOLVED / "index.html")

    for candidate in candidate_paths:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved

    if not clean_relative:
        return ROOT_RESOLVED / "index.html"

    html_name = relative_obj.name
    stem = relative_obj.stem or html_name
    app_html_candidates = [
        ROOT_RESOLVED / f"{stem}.html",
        ROOT_RESOLVED / stem / "index.html",
        WORKSPACE_RESOLVED / f"{stem}.html",
        WORKSPACE_RESOLVED / stem / "index.html",
    ]

    for candidate in app_html_candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved

    search_name = relative_obj.name
    if search_name:
        matches = []
        for match in WORKSPACE_RESOLVED.rglob(search_name):
            try:
                rel_parts = match.resolve().relative_to(WORKSPACE_RESOLVED).parts
            except ValueError:
                continue

            if len(rel_parts) >= len(relative_obj.parts):
                tail_parts = rel_parts[-len(relative_obj.parts):]
                if tuple(part.lower() for part in tail_parts) == tuple(part.lower() for part in relative_obj.parts):
                    return match.resolve()

            matches.append(match.resolve())

        if len(matches) == 1:
            return matches[0]

    return None


def fetch_remote_file(url_path):
    clean_path = url_path.split("?", 1)[0].split("#", 1)[0]
    if not clean_path or clean_path in APP_ROUTES:
        return None

    cache_relative = clean_path.lstrip("/\\")
    if not cache_relative:
        return None

    cache_target = (CACHE_ROOT / cache_relative).resolve()
    if CACHE_ROOT.resolve() not in cache_target.parents:
        return None

    if cache_target.exists():
        return cache_target

    cache_target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(
        REMOTE_ORIGIN + clean_path,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = response.read()
    except Exception as error:
        print(f"[remote-miss] {clean_path} ({error})", flush=True)
        return None

    if not data:
        return None

    cache_target.write_bytes(data)
    print(f"[remote-cache] {clean_path} -> {cache_target}", flush=True)
    return cache_target


class PortfolioHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean_path = unquote(path.split("?", 1)[0].split("#", 1)[0])
        normalized = clean_path.rstrip("/") or "/"

        if normalized in APP_ROUTES:
            html_candidates = [
                normalized.strip("/") + ".html",
                normalized.strip("/") + "/index.html",
            ]
            for html_candidate in html_candidates:
                matched = find_matching_file(html_candidate)
                if matched:
                    print(f"[route] {normalized} -> {matched}", flush=True)
                    return str(matched)
            return str(ROOT_RESOLVED / "index.html")

        relative_path = clean_path.lstrip("/")
        matched = find_matching_file(relative_path)

        if matched:
            if WORKSPACE_RESOLVED not in matched.parents and matched != WORKSPACE_RESOLVED:
                return str(ROOT_RESOLVED / "index.html")
            return str(matched)

        if "." not in Path(relative_path).name:
            return str(ROOT_RESOLVED / "index.html")

        remote_match = fetch_remote_file(clean_path)
        if remote_match:
            return str(remote_match)

        print(f"[missing] {clean_path}", flush=True)
        return str(ROOT_RESOLVED / "__missing__")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), PortfolioHandler)
    PID_FILE.write_text(str(os.getpid()), encoding="ascii")
    print(f"Serving portfolio at http://127.0.0.1:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if PID_FILE.exists():
            PID_FILE.unlink()
