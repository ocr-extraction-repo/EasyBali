from pydantic import BaseModel
from fastapi import UploadFile

class VillaData(BaseModel):
    name_of_villa: str
    address: str
    google_maps_link: str
    directions: str
    entrance_picture: UploadFile
    location: str
    contact_vm: str
    contact_mt: str
    passport_collection: str
    number_of_bdr: str
    website_url: str = ""
    whatsapp_url: str = ""
    messenger_url: str = ""
    instagram_url: str = ""