from pydantic import BaseModel


class SpoonsLocation(BaseModel):
    pub_name: str
    street_address: str
    locality: str
    region: str
    post_code: str
