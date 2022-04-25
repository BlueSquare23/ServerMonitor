from app import run_app
import platform

HOSTNAME = platform.uname().node

# Set's hostname (useful for development)
if HOSTNAME != "wopaguz.com" and HOSTNAME != "vps2754.pairvps.com":
	HOSTNAME = "localhost"

if __name__ == "__main__":
	app = run_app()
	app.run(host=HOSTNAME, debug=True)
