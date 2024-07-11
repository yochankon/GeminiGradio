from fastapi import FastAPI
from tts import TTS
import uvicorn

app = FastAPI()


@app.get("/")
async def read_root():
    return "connect ok"

@app.get("/tts")
async def get_tts():

    return TTS().greet()
    # return TTS().greet(query)

# if __name__ == '__main__':
#     uvicorn.run(app, port=9300, host='0.0.0.0' )

# @app.get("/sql/{query}")
# async def get_query_data(query: str):
#     return SqlManager().select_query(query)
#
#
# @app.get("/schema/tables")
# async def get_tables():
#     return SqlManager().get_table_list()
#
#
# @app.get("/schema/table/{table_name}")
# async def get_table_schema(table_name: str):
#     return SqlManager().get_table_schema(table_name)
# ~