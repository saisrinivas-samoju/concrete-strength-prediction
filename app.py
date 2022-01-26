from main import app
import os

host = '0.0.0.0'
port = int(os.getenv("PORT",5000))

if __name__ == '__main__':
    app.run(host= host, port= port)
