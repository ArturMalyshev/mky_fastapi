from model.Delivery.pochta_rf import RussianMailDeliveryBody, create_address


def create_delivery(db, data: RussianMailDeliveryBody):
    if data.method == 'pochta_rf':
        return create_address(db, data)
    else:
        return 0

