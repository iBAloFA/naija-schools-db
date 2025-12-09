# Run once:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

engine = create_engine("sqlite:///schools.db")
Session = sessionmaker(bind=engine)

states = ["Lagos","Ogun","Abuja FCT","Rivers","Kano","Oyo","Kaduna","Enugu"]
lgas = ["Ikeja","Abeokuta","AMAC","Port Harcourt","Kano Municipal","Ibadan North"]

session = Session()
for i in range(100):
    session.execute(text("""INSERT INTO schools (name,lga,state,type,ownership) 
                         VALUES (:n,:l,:s,:t,:o)"""),
                    {"n": f"Community School {i+1}", "l": random.choice(lgas), 
                     "s": random.choice(states), "t": random.choice(["Primary","Secondary"]), 
                     "o": random.choice(["Public","Private"])})
session.commit()
print("100 sample schools added!")
