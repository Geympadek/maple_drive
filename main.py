import loader
import api

def main():
    loader.app.run('0.0.0.0', port=443, debug=True, ssl_context=("ssl/tetpix.run.place.cer", "ssl/tetpix.run.place.key"))

if __name__ == "__main__":
    main()