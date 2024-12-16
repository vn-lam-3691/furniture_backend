def convertProduct(product) -> dict:
    if isinstance(product, dict):
        return {
            "id": str(product["_id"]),
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "offerPercentage": product.get("offerPercentage", None),
            "description": product.get("description", None),
            "colors": product.get("colors", []),
            "sizes": product.get("sizes", []),
            "images": product.get("images", [])
        }
    else:  # Trường hợp product là Pydantic model
        return {
            "id": str(product.id),
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "offerPercentage": product.offerPercentage,
            "description": product.description,
            "colors": product.colors or [],
            "sizes": product.sizes or [],
            "images": product.images or []
        }
    
def convertProducts(products) -> list:
    return [convertProduct(product) for product in products]

def convertCartProduct(cartProduct) -> dict:
    if isinstance(cartProduct, dict):
        # Trường hợp cartProduct là dictionary
        return {
            "product": convertProduct(cartProduct["product"]),
            "quantity": cartProduct["quantity"],
            "selectedColor": cartProduct["selectedColor"],
            "selectedSize": cartProduct["selectedSize"]
        }
    else:  # Trường hợp cartProduct là Pydantic model
        return {
            "product": convertProduct(cartProduct.product),
            "quantity": cartProduct.quantity,
            "selectedColor": cartProduct.selectedColor,
            "selectedSize": cartProduct.selectedSize
        }

def convertCartProducts(cartProducts) -> list:
    return [convertCartProduct(cartProduct) for cartProduct in cartProducts]


def convertUser(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "imagePath": user.get("imagePath", None)
    }


def convertAddress(address) -> dict:
    if isinstance(address, dict):
        # Trường hợp address là dictionary
        return {
            "addressTitle": address["addressTitle"],
            "fullName": address["fullName"],
            "phone": address["phone"],
            "city": address["city"],
            "street": address["street"],
            "state": address["state"]
        }
    else:  # Trường hợp address là Pydantic model
        return {
            "addressTitle": address.addressTitle,
            "fullName": address.fullName,
            "phone": address.phone,
            "city": address.city,
            "street": address.street,
            "state": address.state
        }

def convertOrder(order) -> dict:
    return {
        "id": str(order["_id"]),
        "orderId": order["orderId"],
        "userId": str(order["userId"]),
        "orderStatus": order["orderStatus"],
        "address": convertAddress(order["address"]),
        "products": convertCartProducts(order["products"]),
        "totalPrice": order["totalPrice"],
        "dateOrder": order["dateOrder"]
    }

def convertListOrders(orders) -> list:
    return [convertOrder(order) for order in orders]