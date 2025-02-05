## Attachment Style Test

deployed at: https://attachmentstyletest.org

This app is inspired by a book on adult attachment styles I read last summer.
I disliked all of the quizes I could find on the internet both content and implementation
wise. So I decided to code my own.

Distinguishing features:
- a pdf with all the questions and answers is generated at the end ready for download
- extra quiz to asses other people with more behavior-based questions
- dashboard representing the global results based on a few demographic features

Above all, however, this is just a coding exercise for myself. I wanted to see if one
could use Dash Plotly to build a full-fledged interactive website without any html
or javascript. It is by no means the right tool for the job, but it is fun to see 
what it is, in principle, capable of.

## Deployment

If you would like to host your own instance of this quiz (the instruction for customization
follow below), you need to follow these steps:

1. clone the repo
2. create an instance of a postgres database, you can use the official docker image with
`docker pull postgres` and then
`docker run --name postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres`
3. add a standard alembic.ini from https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment
and replace the sqlalchemy.url with the url of your database
4. run `alembic upgrade heads` in attachment_style directory to migrate the database 
(create all the necessary tables)
5. if you want to run the app locally you can either 

    5.1. do it directly by

        5.1.1. creating a virtual environment (for example `python3 -m venv venv`)

        5.1.2. installing dependencies with `pip install -r requirements.txt` (execute in 
        the root directory

        5.1.3. running `python app.py` in the root directory 

    5.2. or build a docker image by
        * running `docker build -t attachment-style-test .`
        * start the container and set the envronment variable DB_URL by
        `docker run -e DB_URL=<your db url> -p 8050:8050 attachment-style-test`

6. if you decide to host it in the cloud, in the cloud of your choice, choose the option 
to build from the docker image and the environment variable DB_URL to the url of your 
database, the port to 8050 and the command to "python app.py".
