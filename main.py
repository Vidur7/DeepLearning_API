from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

languages = ["English", "French", "German", "Romanian"]

class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str
    
    @validator('base_lang', 'final_lang')
    def valid_lang(cls, lang):
        if lang not in languages:
            raise ValueError('Invalid language')
        return lang


## Route1 get/
@app.get("/")
def get_root():
    return {"message": "Hello World!"}
            

## Route2 /translate 
@app.post("/translate")
def post_translations(t: Translation, background_tasks: BackgroundTasks):
    t_id = tasks.store_translation(t)
    background_tasks.add_task(tasks.run_translation,t_id)
    return {"task_id": t_id}

## Route3 /results
@app.get("/results")
def get_translations(t_id: int):
    return {"translations": tasks.find_translations(t_id)}