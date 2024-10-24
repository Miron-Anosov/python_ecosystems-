from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    """
    Если вы объявите тип параметра у функции операции пути как bytes, то FastAPI прочитает файл за вас,
    и вы получите его содержимое в виде bytes.
    Следует иметь в виду, что все содержимое будет храниться в памяти. Это хорошо подходит для небольших файлов.
    """
    return {"file_size": len(file)}


"""
File - это класс, который наследуется непосредственно от Form.

Но помните, что когда вы импортируете Query, Path, File и другие из fastapi, на самом деле это функции, 
которые возвращают специальные классы.
"""


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """Использование UploadFile имеет ряд преимуществ перед bytes:

    Использовать File() в значении параметра по умолчанию не обязательно.
    При этом используется "буферный" файл:
        Файл, хранящийся в памяти до максимального предела размера,
        после преодоления которого он будет храниться на диске.
    Это означает, что он будет хорошо работать с большими файлами, такими как изображения, видео, большие
    бинарные файлы и т.д., не потребляя при этом всю память."""
    return {"filename": file.filename}


"""
Для объявления тела файла необходимо использовать File, поскольку в противном случае параметры будут интерпретироваться 
как параметры запроса или параметры тела (JSON).
"""


###################################################################

@app.post("/files2/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


"""
Необязательная загрузка файлов
Вы можете сделать загрузку файла необязательной, используя стандартные аннотации типов и установив значение 
по умолчанию None
"""


@app.post("/uploadfile2/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


####################################################################


"""
UploadFile с дополнительными метаданными

Вы также можете использовать File() вместе с UploadFile, например, для установки дополнительных метаданных
"""


@app.post("/files3/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile3/")
async def create_upload_file(
        file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    print(type(file))  # <class 'starlette.datastructures.UploadFile'>
    return {"filename": file.filename}


###########################################################################################

"""
Загрузка нескольких файлов
Можно одновременно загружать несколько файлов.
Они будут связаны с одним и тем же "полем формы", отправляемым с помощью данных формы.
Для этого необходимо объявить список bytes или UploadFile
"""


@app.post("/files4/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles4/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
        """
    return HTMLResponse(content=content)


##############################################################################

@app.post("/files5/")
async def create_files(
        files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles6/")
async def create_upload_files(
        files: Annotated[
            list[UploadFile], File(description="Multiple files as UploadFile")
        ],
):
    return {"filenames": [file.filename for file in files]}

"""
Загрузка нескольких файлов с дополнительными метаданными
Так же, как и раньше, вы можете использовать File() для задания дополнительных параметров, даже для UploadFile
"""