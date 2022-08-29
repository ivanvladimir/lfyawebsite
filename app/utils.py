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
