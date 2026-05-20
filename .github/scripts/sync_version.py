import json
import os
import re
import sys
import urllib.request
from packaging.version import Version


def get_latest_pypi_version(package_name: str) -> str:
    url = f"https://pypi.org/pypi/{package_name}/json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "boscli-sync-workflow (GitHub Actions)"}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        return data["info"]["version"]


def get_current_local_version() -> str:
    # Read version directly from pyproject.toml without external toml dependency
    with open("pyproject.toml", "r") as f:
        content = f.read()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def update_pyproject_toml(new_version: str) -> None:
    with open("pyproject.toml", "r") as f:
        content = f.read()

    # Update version
    content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content,
        count=1
    )

    # Update bos-ai dependency pin
    content = re.sub(
        r'"bos-ai\s*==\s*[^"]+"',
        f'"bos-ai == {new_version}"',
        content,
        count=1
    )

    with open("pyproject.toml", "w") as f:
        f.write(content)




def set_action_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"[Output] {name}={value}")


def main() -> None:
    try:
        latest_version_str = get_latest_pypi_version("bos-ai")
        current_version_str = get_current_local_version()
    except Exception as e:
        print(f"Error checking versions: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Latest bos-ai on PyPI: {latest_version_str}")
    print(f"Current local boscli: {current_version_str}")

    latest = Version(latest_version_str)
    current = Version(current_version_str)

    if latest > current:
        print(f"Updating boscli to version {latest_version_str}...")
        update_pyproject_toml(latest_version_str)
        print("Updated pyproject.toml successfully.")
        set_action_output("updated", "true")
        set_action_output("new_version", latest_version_str)
    else:
        print("boscli is already up-to-date with bos-ai.")
        set_action_output("updated", "false")


if __name__ == "__main__":
    main()
