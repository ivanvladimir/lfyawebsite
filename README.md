# lfyawebsite

Website for the class


## Creating course

Execute and fill the interactive fields

    flask --app app.flask_app:app course add

List courses:

    flask --app app.flask_app:app course list

Import list from _csv_

    flask --app app.flask_app:app student import CSV_file id_course

CSV should be in the format: School ID, LAST NAME, NAME, EMAIL

Assign teacher to couse

    flask --app app.flask_app:app user assign email id_course

## Executing webservice

    flask --app app.flask_app:app run


