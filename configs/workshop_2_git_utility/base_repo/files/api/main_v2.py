from generator import PasswordGenerator

from fastapi import FastAPI

app = FastAPI()


@app.get("/pwd")
async def get_password():
    password_generator = PasswordGenerator()
    pwd = password_generator.generate_password(20)
    return {"password": pwd}


@app.get("/pwd/short")
async def get_short_password():
    password_generator = PasswordGenerator()
    pwd = password_generator.generate_password(10)
    return {"password": pwd}


@app.get("/pwd/long")
async def get_long_password():
    password_generator = PasswordGenerator()
    pwd = password_generator.generate_password(30)
    return {"password": pwd}


if __name__ == "__main__":
    print("use gunivorn to start server")
    exit(1)
