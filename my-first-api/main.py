## api de contactos
## arquitectura monolítica
## CRUD completo: GET | POST | PUT | DELETE |
## USAREMOS MEMORIA LOCAL, UNA LISTA DICCIONARIOS
## {"id": 1, "name": "Juan", "cif": "123456789"}

from itertools import count

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI()
contacts: list[dict] = []
contact_ids = count(1)


class ContactInput(BaseModel):
	name: str = Field(min_length=1)
	cif: str = Field(min_length=1, pattern=r"^[0-9]+$")


def find_contact(contact_id: int) -> dict:
	for contact in contacts:
		if contact["id"] == contact_id:
			return contact
	raise HTTPException(status_code=404, detail="Contact not found")


@app.get("/contacts")
def list_contacts():
	return contacts


@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
	return find_contact(contact_id)


@app.post("/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(data: ContactInput):
	contact = {"id": next(contact_ids), **data.model_dump()}
	contacts.append(contact)
	return contact


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, data: ContactInput):
	contact = find_contact(contact_id)
	contact.update(data.model_dump())
	return contact


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int):
	contacts.remove(find_contact(contact_id))