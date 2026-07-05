import sys
import os
from pathlib import Path

# ===== Force using local venv =====
# مسیر فعلی فایل
current_dir = Path(__file__).parent.absolute()

# مسیر پوشه venv
venv_path = current_dir / "venv"

if venv_path.exists():
    # پیدا کردن site-packages داخل lib
    lib_path = venv_path / "lib"
    
    if lib_path.exists():
        # پیدا کردن پوشه python3.x
        python_dirs = [d for d in lib_path.iterdir() if d.is_dir() and d.name.startswith("python3")]
        
        for py_dir in python_dirs:
            site_packages = py_dir / "site-packages"
            if site_packages.exists() and str(site_packages) not in sys.path:
                sys.path.insert(0, str(site_packages))
                print(f"✅ Virtualenv site-packages forced: {site_packages}")
                break
    else:
        print("⚠️ پوشه lib پیدا نشد")
else:
    print("⚠️ پوشه venv پیدا نشد")



