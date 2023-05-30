from pydantic import BaseModel
from uuid import uuid4

from model.Delivery.pochta_rf import RussianMailDeliveryBody

class NewPayloadBody(BaseModel):
    delivery: RussianMailDeliveryBody
    first_name: str
    last_name: str
    email: str
    phone: str
    sum: float
    session_key: str
    discount: float
    result: float


def create_uniq_id ():
    return "mky_" + str(uuid4())[:12]
