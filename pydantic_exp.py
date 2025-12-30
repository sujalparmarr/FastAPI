from pydantic import BaseModel, Field, ValidationError, field_validator, computed_field
from typing import Optional, List, Dict
  
class User(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., ge=0)
    stock: int = Field(default=0, ge=0)

class OrderItem(BaseModel):
    product: Product
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    order_id: str
    items: List[OrderItem]
    metadata: Dict[str, str] = {}

class Signup(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def check_email(cls, v):
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v

    @field_validator("password")
    def strong_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 chars")
        return v

class Person(BaseModel):
    full_name: str = Field(alias="fullName")
    country: str

    model_config = {
        "populate_by_name": True
    }

class Employee(BaseModel):
    first_name: str
    last_name: str
    salary: float

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def yearly_salary(self) -> float:
        return self.salary * 12

class Admin(User):
    role: str = "admin"

if __name__ == "__main__":
    user = User(id=1, name="Sujal")
    print(user.model_dump())

    product = Product(name="Laptop", price=60000)
    print(product)

    order = Order(
        order_id="ORD101",
        items=[OrderItem(product=product, quantity=2)]
    )
    print(order.model_dump())

    try:
        Signup(email="invalid-email", password="123")
    except ValidationError as e:
        print("Validation Error:", e.errors())

    person = Person(fullName="Virat Kohli", country="India")
    print(person.model_dump(by_alias=True))

    emp = Employee(first_name="Rohit", last_name="Sharma", salary=50000)
    print(emp.full_name, emp.yearly_salary)

    admin = Admin(id=9, name="Admin User")
    print(admin)
