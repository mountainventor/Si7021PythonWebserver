import time
import smbus
import socket
from flask import Flask

SI7021_I2C_ADDRESS = 0x40
SI7021_HUMIDITY_REGISTER_ADDRESS = 0xE5
SI7021_HUMIDITY_REGISTER_NO_OF_BYTES = 2
SI7021_TEMPERATURE_REGISTER_ADDRESS = 0xE3
SI7021_TEMPERATURE_REGISTER_BYTES = 2

bus = smbus.SMBus(1)
app = Flask(__name__)


def main():
    @app.route("/")
    def hello_world():
        response = f"""
        <!doctype html>
        <html>
        <head>
        <meta http-equiv="refresh" content="5" />
        </head>
        <body>
        <h2>Relative Humidity: {read_humidity():.1f} %</h2> 
        <h2>Temperature: {read_temperature():.1f} °C</h2>
        </body>
        </html>
        """
        return response

    raspis_ip = get_raspis_ip()
    app.run(host=raspis_ip, port=80)


def read_temperature():
    temp_raw = bus.read_i2c_block_data(SI7021_I2C_ADDRESS, SI7021_TEMPERATURE_REGISTER_ADDRESS, SI7021_TEMPERATURE_REGISTER_BYTES)
    time.sleep(0.1)
    temp_deg_c = ((temp_raw[0] * 256 + temp_raw[1]) * 175.72 / 65536.0) - 46.85
    return temp_deg_c


def read_humidity():
    rh_raw = bus.read_i2c_block_data(SI7021_I2C_ADDRESS, SI7021_HUMIDITY_REGISTER_ADDRESS, SI7021_HUMIDITY_REGISTER_NO_OF_BYTES)
    time.sleep(0.1)
    rh_percent = ((rh_raw[0] * 256 + rh_raw[1]) * 125 / 65536.0) - 6
    return rh_percent


def get_raspis_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    raspis_ip = f"{s.getsockname()[0]}"
    s.close()
    return raspis_ip


if __name__ == "__main__":
    main()
