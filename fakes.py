import random
from faker import Faker
fake = Faker()

first_name = fake.first_name()
middle_name = fake.first_name()
county = fake.word()
eye_color = random.choice(['blue', 'brown', 'green'])
hair_color = random.choice(['blonde', 'brown', 'black'])
age = random.randint(18, 90)
location = fake.address()
description = fake.text()
image = fake.image_url()
gender = random.choice(['male', 'female'])
