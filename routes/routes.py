from fastapi import APIRouter, HTTPException, Query
from model.product import Product
from model.user import User, UserNewProfile
from model.address import Address
from model.order import Order
from config.config import product_collection, user_collection, order_collection
from serializer.serializer import *
from bson import ObjectId
from passlib.context import CryptContext


endPoints = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@endPoints.post("/add-product")
def addNewProduct(product: Product):
    try:
        mDoc = dict(product)
        res = product_collection.insert_one(mDoc)
        document_id = res.inserted_id
        return {
            "status": "success",
            "message": "Product added successfully",
            "id": str(document_id)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
       }

@endPoints.get("/get-products")
async def getProducts():
    try:
        res = product_collection.find()
        list_products = convertProducts(res)
        return {
            "status": "success",
            "message": "Products fetched successfully",
            "data": list_products
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@endPoints.get("/get-product")
async def getProduct(id: str):
    try:
        res = product_collection.find_one({"_id": ObjectId(id)})
        result = convertProduct(res)
        return {
            "status": "success",
            "message": "Product info",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@endPoints.patch("/update-product/{id}")
async def updateProduct(id: str, product: Product):
    try:
        find_res = product_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(product)}
        )
        if find_res:
            return {
                "status": "success",
                "message": f"Updated {id} successfully"
            }
        else:
            return {
                "status": "Not found",
                "message": "Product not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@endPoints.delete("/delete-product/{id}")
async def deleteProduct(id: str):
    try:
        res = product_collection.find_one_and_delete(
            {"_id": ObjectId(id)}
        )
        if res:
            return {
                "status": "success",
                "message": f"Deleted {id} successfully"
            }
        else:
            return {
                "status": "Not found",
                "message": "Product not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def hash_password(password: str):
    return pwd_context.hash(password)

@endPoints.post("/register")
async def createAccount(user: User):
    try:
        # Kiểm tra xem email đã tồn tại hay chưa
        if user_collection.find_one({"email": user.email}):
            raise HTTPException(status_code="error", detail="Email already exists")
        
        newUser = {
            "id": "",
            "email": user.email,
            "password": hash_password(user.password),  # Hash mật khẩu
            "firstName": user.firstName,
            "lastName": user.lastName,
            "imagePath": user.imagePath,
        }
        res = user_collection.insert_one(newUser)
        user_id = res.inserted_id
        return {
            "status": "success",
            "message": "User has created successfully",
            "data": str(user_id)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@endPoints.post("/login")
async def login(email: str, password: str):
    try:
        user = user_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not pwd_context.verify(password, user["password"]):
            raise HTTPException(status_code="error", detail="Invalid password")
        
        res = convertUser(user)
        return {
            "status": "success",
            "message": "Login successfully",
            "data": res
        }
    except HTTPException as e:
        return {
            "status": e.status_code,
            "message": e.detail
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@endPoints.patch("/update-user-info/{id}")
async def updateUserInfo(id: str, firstName: str = None, lastName: str = None, imagePath: str = None):
    try:
        user = user_collection.find_one({"_id": ObjectId(id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        new_user_profile = UserNewProfile(
            firstName=firstName,
            lastName=lastName,
            imagePath=imagePath
        )
        
        user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(new_user_profile)}
        )
        return {
            "status": "success",
            "message": "User information updated successfully",
            "data": id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        

# For Orders
@endPoints.post("/create-order")
async def createOrder(order: Order):
    try:
        check_exist = order_collection.find_one({"orderId": order.orderId})
        if check_exist:
            raise HTTPException(status_code="error", detail="Order already exists")
        
        mOrder = {
            "orderId": order.orderId,
            "userId": order.userId,
            "orderStatus": order.orderStatus,
            "address": convertAddress(order.address),
            "products": convertCartProducts(order.products),
            "totalPrice": order.totalPrice,
            "dateOrder": order.dateOrder
        }
        
        request = order_collection.insert_one(mOrder)
        document_id = request.inserted_id
        return {
            "status": "success",
            "message": "Order has created successfully",
            "id": str(document_id)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
@endPoints.get("/get-orders")
async def getAllOrders(user_id: str = Query(..., alias="userId")):
    try:
        orders = list(order_collection.find({"userId": user_id}))
        
        if not orders:
            return {"message": "No orders found for this user", "orders": []}
        
        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]
        
        return {
            "status": "success",
            "message": f"Orders of {user_id} fetched successfully",
            "data": orders
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    