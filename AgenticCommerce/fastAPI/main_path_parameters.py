from enum import Enum

from fastapi import FastAPI

class FilePaths(str, Enum):
    john = "john"
    koushal = "koushal"

app = FastAPI()
# Server -> Client
@app.get("/files/{file_name}")
async def read_file(file_name: FilePaths):
    if file_name is FilePaths.john:
        return {"filepath": "/home/johndoe/myfile.txt", "message": "John, this is for you!"}
    if file_name.value == FilePaths.koushal.value:
        return {"filepath": "/home/koushalsmodi/ganpati.txt", "message": "Koushal, this one is for you!"}

