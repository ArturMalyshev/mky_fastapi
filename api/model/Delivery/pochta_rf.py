from pydantic import BaseModel

class RussianMailDeliveryBody(BaseModel):
    method: str
    region: str
    city: str
    address: str
    zip: int
    type: str
    track: str
    pvz_type: str
    description: str
    price: float
    comment: str


def create_address(db, data: RussianMailDeliveryBody):
    sql = "INSERT INTO address_pochta_rf (region, city, address, zip, delivery_type, pvz_type, track_num, delivery_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    crsr = db.cursor()
    crsr.execute(sql, [data.region, data.city, data.address, data.zip, data.type, data.pvz_type, data.track, data.description])
    db.commit()

    sql = "SELECT address_id FROM address_pochta_rf WHERE region='" + data.region + "' AND city='" + data.city + "' AND address='" + data.address + "' AND zip=" + str(data.zip) + " AND delivery_type='" + data.type + "' AND pvz_type='" + data.pvz_type + "' AND track_num='" + data.track + "' AND delivery_description='" + data.description + "'  ORDER BY created_at DESC LIMIT 1"
    # cursor.execute(sql, [data.region, data.city, data.address, data.zip, data.type, data.pvz_type, data.track, data.description])

    return sql
