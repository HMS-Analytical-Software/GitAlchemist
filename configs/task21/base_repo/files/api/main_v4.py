from generator import PasswordGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# init
app = FastAPI(
    title="password generator API",
    version="0.0.1",
    contact={
        "name": "Betty Blue",
        "email": "<betty@pw-compa.ny>"
    },
    description="We generate your passwords!",
    openapi_tags=None
)

# cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://..."],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
