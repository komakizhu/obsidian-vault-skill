import os
import sys
import json
import argparse
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "obsidian-vault"
SAVED_PATH_FILE = CONFIG_DIR / "path.txt"

def get_platform_obsidian_json():
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "obsidian" / "obsidian.json"
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "obsidian" / "obsidian.json"
    else:  # linux
        return home / ".config" / "obsidian" / "obsidian.json"
    return None

def scan_common_folders():
    search_roots = [
        Path.home() / "Documents",
        Path.home() / "Desktop",
        Path.home()
    ]
    
    found_vaults = []
    for root in search_roots:
        if not root.exists():
            continue
        try:
            for item in root.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    if (item / ".obsidian").exists():
                        found_vaults.append(item)
                    try:
                        for subitem in item.iterdir():
                            if subitem.is_dir() and not subitem.name.startswith('.') and subitem.name != "node_modules":
                                if (subitem / ".obsidian").exists():
                                    found_vaults.append(subitem)
                    except PermissionError:
                        continue
        except PermissionError:
            continue
            
    unique_vaults = []
    seen = set()
    for vault in found_vaults:
        p = str(vault.resolve())
        if p not in seen:
            seen.add(p)
            unique_vaults.append(vault)
    return unique_vaults

def get_remembered_path():
    if SAVED_PATH_FILE.exists():
        try:
            path_str = SAVED_PATH_FILE.read_text(encoding="utf-8").strip()
            if path_str and os.path.exists(path_str):
                return path_str
        except Exception:
            pass
    return None

def save_path(path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    resolved_path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(resolved_path):
        print(f"Error: Path '{resolved_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    SAVED_PATH_FILE.write_text(resolved_path, encoding="utf-8")
    print(f"Remembered Obsidian vault path: {resolved_path}")
    return resolved_path

def get_active_path():
    # 1. Check remembered path
    remembered = get_remembered_path()
    if remembered:
        return remembered
        
    # 2. Try parsing obsidian.json
    obsidian_json_path = get_platform_obsidian_json()
    if obsidian_json_path and obsidian_json_path.exists():
        try:
            with open(obsidian_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                vaults = data.get("vaults", {})
                valid_vaults = []
                for _, vault_info in vaults.items():
                    v_path = vault_info.get("path")
                    if v_path and os.path.exists(v_path):
                        valid_vaults.append(vault_info)
                if valid_vaults:
                    valid_vaults.sort(key=lambda x: x.get("ts", 0), reverse=True)
                    detected_path = valid_vaults[0]["path"]
                    save_path(detected_path)
                    return detected_path
        except Exception as e:
            print(f"Debug: failed parsing obsidian.json: {e}", file=sys.stderr)
            
    # 3. Try scanning common folders
    detected_vaults = scan_common_folders()
    if detected_vaults:
        detected_path = str(detected_vaults[0].resolve())
        save_path(detected_path)
        return detected_path
        
    return None

def main():
    parser = argparse.ArgumentParser(description="Manage Obsidian Vault Path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--get", action="store_true", help="Get the active vault path")
    group.add_argument("--set", type=str, help="Save a specific vault path")
    
    args = parser.parse_args()
    
    if args.set:
        save_path(args.set)
    elif args.get:
        path = get_active_path()
        if path:
            print(path)
        else:
            print("Error: No Obsidian vault detected on this machine. Please provide the path using --set <path>.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
