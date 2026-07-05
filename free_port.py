
import os
import sys
import subprocess
import signal

def kill_port(port=5000, kill_flask=True):
    print(f"🔍 جستجو برای پورت {port}...")

    killed = False

    # روش ۱: ss
    try:
        result = subprocess.check_output(f"ss -ltnp 2>/dev/null | grep :{port}", shell=True, text=True)
        for line in result.strip().split('\n'):
            if line:
                pid = None
                if 'pid=' in line:
                    pid = line.split('pid=')[1].split(',')[0]
                elif '/' in line:
                    pid = line.split('/')[-2].split()[0]
                
                if pid:
                    print(f"🛑 کشتن پروسس PID: {pid} (پورت {port})")
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                        killed = True
                    except:
                        os.system(f"sudo kill -9 {pid} 2>/dev/null")
    except:
        pass

    # روش ۲: پیدا کردن پروسس‌های Flask / routes.py
    if kill_flask:
        print("🔍 جستجو برای پروسس‌های Flask...")
        try:
            result = subprocess.check_output("ps aux | grep -E 'python|flask|routes.py' | grep -v grep", shell=True, text=True)
            for line in result.strip().split('\n'):
                if line:
                    pid = line.split()[1]
                    print(f"🛑 کشتن پروسس Flask با PID: {pid}")
                    os.system(f"sudo kill -9 {pid} 2>/dev/null")
        except:
            pass

    print(f"✅ پورت {port} آزاد شد!" if killed else f"✅ پورت {port} قبلاً آزاد بود.")

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    
    kill_port(port)

