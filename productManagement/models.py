from datetime import datetime
from typing import Optional, List

from .const import String


# Create your models here.

class Product:
    id: str
    name: str
    image: List[str]
    unitPrice: float
    quantity: int
    category: str
    description: Optional[str] = None
    provider: str
    rating: float = 0.0
    product_origin: str
    createAt: datetime
    updateAt: datetime

    def __init__(self, _dict):
        self.id = _dict[String.id]
        self.name = _dict[String.name]
        self.unitPrice = float(_dict[String.unitPrice])
        self.quantity = int(_dict[String.quantity])
        self.category = _dict[String.category]
        self.image = _dict[String.image]
        self.product_origin = _dict[String.productOrigin]
        self.provider = _dict[String.provider]
        self.createAt = _dict[String.createAt]
        self.updateAt = _dict[String.updateAt]

        if _dict[String.description] is not None:
            self.description = _dict[String.description]

        if _dict[String.rating] is not None:
            self.rating = float(_dict[String.rating])

    def to_dict(self):
        return {
            String.id: self.id,
            String.name: self.name,
            String.category: self.category,
            String.unitPrice: self.unitPrice,
            String.quantity: self.quantity,
            String.description: self.description,
            String.image: self.image,
            String.provider: self.provider,
            String.rating: self.rating,
            String.productOrigin: self.product_origin,
            String.createAt: self.createAt,
            String.updateAt: self.updateAt
        }


class Category:
    id: str
    name: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self, _dict):
        self.id = _dict[String.id]
        self.name = _dict[String.name]
        self.createdAt = _dict[String.createAt]
        self.updatedAt = _dict[String.updateAt]

    def to_dict(self):
        return {
            String.id: self.id,
            String.name: self.name,
            String.createAt: self.createdAt,
            String.updateAt: self.updatedAt,
        }


class Users:
    id: str
    email: str
    isAdmin: bool = False

    def __init__(self, _dict):
        self.id = _dict[String.id]
        self.email = _dict[String.email]
        if _dict[String.is_admin] is not None:
            self.isAdmin = bool(_dict[String.is_admin])

    def to_dict(self):
        return {
            String.id: self.id,
            String.email: self.email,
            String.is_admin: self.isAdmin,
        }
