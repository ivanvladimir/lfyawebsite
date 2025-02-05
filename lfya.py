import typer
import asyncio
from datetime import datetime
from app import crud
from app.models import Token, UserEnum, Course

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
def courses_list(user_id: str):
    groups = asyncio.run(crud.get_courses())
    groups.sort(key=lambda g: g.created, reverse = True)
    print(f"Lista de grupos:")
    for g in groups:
        print(g.course_name, g.course_id)

@courses_app.command("add")
def course_ass():
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

@users_app.command("create")
def users_create(user_name: str):
    print(f"Creating user: {user_name}")


@users_app.command("delete")
def users_delete(user_name: str):
    print(f"Deleting user: {user_name}")


if __name__ == "__main__":
    app()
