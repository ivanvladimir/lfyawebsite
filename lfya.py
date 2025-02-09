import typer
import asyncio
from datetime import datetime
from app import crud
from app.models import Token, UserEnum, Course, User
from app.core.db import client
import tqdm
import uuid

import getpass

def read_value(info, passwd=False):
    value = input(info) if not passwd else getpass.getpass(info)
    while len(value.strip()) == 0:
        print("Sin valor, intentar de nuevo")
        value = input(info) if not passwd else getpass.getpass(info)
    return value.strip()

def chose_value(info, options):
    value = input(info)
    while not value.strip() in options.keys():
        print("No es un valor aceptado, escoger de:", ", ".join(options.keys()))
        value = input(info)
    return options[value.strip()]

app = typer.Typer()
courses_app = typer.Typer()
app.add_typer(courses_app, name="courses")
users_app = typer.Typer()
app.add_typer(users_app, name="users")


@courses_app.command("list")
def courses_list():
    groups = asyncio.run(crud.get_courses())
    groups.sort(key=lambda g: g.created, reverse = True)
    print(f"Lista de grupos:")
    for g in groups:
        print(g.course_name, g.course_id)

@courses_app.command("add")
def course_add():
    name = read_value("Nombre: ")
    initials = read_value("Iniciales: ")
    year = read_value("Año (eg. 2023): ")
    semester = read_value("Semestre (1 o 2): ")
    dt = datetime.utcnow()

    course = Course(
        name=name,
        initials=initials,
        year=year,
        semester=semester,
        course_id=f"{initials.lower()}{year[-2:]}{'i' if semester=='1' else 'ii'}",
        created=dt,
        modified=dt,
        info="",
        links="",
        starting_date="",
        finished_date="",
        starting_time="",
        finishin_time="",
    )
    c=asyncio.run(crud.create_course(course))
    print("Created course:",c)

@courses_app.command("import")
def course_import(csv_filename, course_id):
    import csv

    total_students=0
    course = True
    if course:
        with open(csv_filename) as csv_file:
            csv = [l for l in csv.reader(csv_file, delimiter=",")]

        users=[]
        for r in tqdm.tqdm(csv):
            dt = datetime.utcnow()
            user = User(
                role=UserEnum.student,
                email=r[3].strip(),
                lastname=r[1].strip(),
                firstname=r[2].strip(),
                url=str(uuid.uuid4()),
                idunam=r[0].strip(),
                created=dt,
                modified=dt,
            )
            total_students+=1
            users.append(user)
        loop = client.get_io_loop()
        loop.run_until_complete(crud.create_students(users,course_id))
    else:
            print(f"Error {course_id} course not found")

        
    print("Total created students:",total_students)




@users_app.command("create")
def users_create(user_name: str):
    print(f"Creating user: {user_name}")


@users_app.command("delete")
def users_delete(user_name: str):
    print(f"Deleting user: {user_name}")


if __name__ == "__main__":
    app()
