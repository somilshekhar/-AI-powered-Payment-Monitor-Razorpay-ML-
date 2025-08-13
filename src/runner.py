import time, subprocess, sys
if __name__ == "__main__":
    while True:
        print("→ ingest"); subprocess.call([sys.executable, "-m", "src.ingest", "--count", "50"])
        print("→ predict"); subprocess.call([sys.executable, "-m", "src.predict"])
        time.sleep(60)
