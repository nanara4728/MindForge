from pydantic import BaseModel, Field, ConfigDict
from math import ceil
from fastapi import FastAPI, HTTPException
app = FastAPI()
materials = {}

class MaterialInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=100, max_length=30000)

def prepare_paragraphs(text: str):    
    paragraphs = []
    for part in text.split("\n\n"):
        cleaned = part.strip()
        if cleaned:
            paragraphs.append(cleaned)
    
    numbered_paragraphs = []
    for number, paragraph in enumerate(paragraphs, start=1):
        numbered_paragraphs.append({"number": number, "text": paragraph})
    return numbered_paragraphs

@app.post("/materials")
def create_material(material: MaterialInput):
    material_id = len(materials) + 1
    words_count = len(material.text.split())
    numbered_paragraphs = prepare_paragraphs(material.text)

    result = {
        "title": material.title, 
        "text": material.text, 
        "characters": len(material.text),
        "words": words_count,
        "paragraphs": numbered_paragraphs,
        "paragraph_count": len(numbered_paragraphs),
        "reading_minutes": ceil(words_count / 200),
        "id": material_id
    }
    materials[material_id] = result
    return result

@app.get("/materials")
def list_materials():
    return {
        "count": len(materials),
        "items": list(materials.values())
    }
    
@app.get("/materials/{material_id}")
def get_materials(material_id: int):
    if material_id not in materials:
        raise HTTPException(status_code = 404, detail = "материал не найден")
    return materials[material_id]

