from pathlib import Path

site_packages = next(Path(".").rglob("site-packages"))

packages = []

for dist in site_packages.glob("*.dist-info"):
    metadata = dist / "METADATA"
    if metadata.exists():
        name = version = None
        for line in metadata.read_text(errors="ignore").splitlines():
            if line.startswith("Name: "):
                name = line[6:]
            elif line.startswith("Version: "):
                version = line[9:]
        if name and version:
            packages.append(f"{name}=={version}")

packages.sort()

with open("requirements_backup.txt", "w") as f:
    f.write("\n".join(packages))

print("Saved", len(packages), "packages.")
