from pydantic import BaseModel, Field, ValidationError

class Person(BaseModel):
    name: str
    age: int = Field(..., gt=0)  # gt=0 → mayor que 0

try:
    person = Person(name="Ana", age=-5)
    print(person)
except ValidationError as e:
    print("Error de validación:", e)

person1 = Person(name="Iván", age=30)
print(person1)