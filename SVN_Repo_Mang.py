# xml_driven_svn_loader.py
# -*- coding: utf-8 -*-
import os, re, subprocess, xml.etree.ElementTree as ET, shutil
from datetime import datetime
from xml.etree.ElementTree import fromstring
from packaging.version import Version, InvalidVersion

# ---------- Utils ----------
def run(cmd: list[str], cwd: str | None = None) -> str:
    """Run a command and return stdout (raise on error)."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
    return p.stdout

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True);  return p

def parse_semver_from_name(name: str) -> Version | None:
    # Essaye d’extraire 1.2.3 d’un nom du type SGW_1.6.0_20260215-1730.cfx
    tokens = re.split(r'[_\-\.\s]', os.path.basename(name))
    for t in tokens:
        try:
            return Version(t)
        except InvalidVersion:
            continue
    return None

# ---------- SVN helpers (CLI) ----------
def svn_list_xml(repo_url: str) -> list[dict]:
    """
    Retourne une liste de fichiers avec métadonnées en se basant sur 'svn list --xml'.
    Nécessite la CLI Subversion (svn). Ref: Subversion CLI reference.  # [4](https://www.visualsvn.com/support/svnbook/ref/svn/)[5](https://www.visualsvn.com/support/svnbook/ref/)
    """
    out = run(["svn", "list", "--xml", repo_url])
    root = ET.fromstring(out)
    items = []
    for entry in root.findall(".//entry"):
        kind = entry.get("kind")
        name_el = entry.find("name")
        commit_el = entry.find("commit")
        if not name_el is None:
            name = name_el.text or ""
        else:
            name = ""
        if kind == "file" and (name.endswith(".cfg") or name.endswith(".cfx")):
            # date/commit info si disponible
            date_text = ""
            if commit_el is not None:
                d = commit_el.find("date")
                if d is not None and d.text:
                    date_text = d.text
            items.append({
                "name": name,
                "url": repo_url.rstrip("/") + "/" + name,
                "date": date_text
            })
    return items

def svn_export_file(file_url: str, dest_folder: str) -> str:
    """
    Export d’un fichier unique via 'svn export' (checkout de fichier non supporté directement,
    on exporte le fichier voulu).  # [7](https://stackoverflow.com/questions/63987805/how-do-i-limit-pysvn-checkout-to-a-specific-filetype)
    """
    ensure_dir(dest_folder)
    local_path = os.path.join(dest_folder, os.path.basename(file_url))
    # S’il existe déjà, on supprime avant d’exporter
    if os.path.isfile(local_path):
        os.remove(local_path)
    run(["svn", "export", "--force", file_url, local_path])
    return local_path

# ---------- Selection policies ----------
def select_latest(items: list[dict], policy: str = "semver_then_time", name_pattern: str | None = None) -> dict:
    candidates = items
    if name_pattern and name_pattern != "*":
        # simple filtrage wildcard "pattern". Ici on laisse simple: terminaison
        if name_pattern.startswith("*."):
            ext = name_pattern[1:]  # ".cfx"
            candidates = [x for x in items if x["name"].endswith(ext)]

    if not candidates:
        raise FileNotFoundError("No .cfg/.cfx found in SVN folder matching the pattern/policy.")

    def to_ts(s: str) -> float:
        # date ISO 8601 svn -> timestamp
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
        except Exception:
            return 0.0

    if policy == "latest" or policy == "newest_by_time":
        candidates.sort(key=lambda x: to_ts(x["date"]), reverse=True)
        return candidates[0]

    # default: semver_then_time
    def sort_key(x):
        v = parse_semver_from_name(x["name"]) or Version("0.0.0")
        t = to_ts(x["date"])
        return (v, t)
    candidates.sort(key=sort_key, reverse=True)
    return candidates[0]

# ---------- CANoe via py_canoe ----------
def open_canoe_and_run(cfg_local_path: str):
    """
    Ouvre CANoe, compile CAPL, démarre mesure. Fonctions supportées par py_canoe:
    open(), start_measurement(), compile_all_capl_nodes(), stop(), quit().  # [1](https://pypi.org/project/py_canoe/)[2](https://chaitu-ycr.github.io/py_canoe/)
    """
    from py_canoe import CANoe, wait  # type: ignore
    app = CANoe()
    app.open(canoe_cfg=cfg_local_path, visible=True, auto_save=False, prompt_user=False, auto_stop=True)
    app.compile_all_capl_nodes()
    app.start_measurement()
    # … exécution de ta campagne ici …
    # app.stop_measurement(); app.quit()

def resolve_from_xml(xml_path: str) -> tuple[str, str]:
    root = ET.parse(xml_path).getroot()
    repo = (root.findtext("./SVN_Path") or "").strip()
    policy = (root.findtext("./SelectionPolicy") or "semver_then_time").strip()
    pattern = (root.findtext("./NamePattern") or "*.cfx").strip()
    cache = (root.findtext("./LocalCache") or "./_cache_configs").strip()
    if not repo:
        raise ValueError("SVN_Path missing in XML.")
    return repo, policy, pattern, cache

if __name__ == "__main__":
    XML_FILE = "config.xml"
    repo, policy, pattern, cache = resolve_from_xml(XML_FILE)
    entries = svn_list_xml(repo)                      # liste des .cfg/.cfx (svn list --xml)  # [4](https://www.visualsvn.com/support/svnbook/ref/svn/)[5](https://www.visualsvn.com/support/svnbook/ref/)
    chosen = select_latest(entries, policy, pattern)  # choix par semver -> time
    local_cfg = svn_export_file(chosen["url"], cache) # export du fichier choisi (svn export)   # [7](https://stackoverflow.com/questions/63987805/how-do-i-limit-pysvn-checkout-to-a-specific-filetype)
    print(f"[INFO] Selected: {chosen['name']} -> {local_cfg}")
    open_canoe_and_run(local_cfg)                     # ouverture & exécution via py_canoe     # [1](https://pypi.org/project/py_canoe/)[2](https://chaitu-ycr.github.io/py_canoe/)