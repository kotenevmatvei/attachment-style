import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# production url
url = str(os.getenv("ATTACHMENT_STYLE_DB_URL"))
# dev url
# url = "postgresql://postgres:password@localhost:32772/"

engine = create_engine(url=url)

# get the data from the database
with Session(engine) as session:
# create a plot for test-yourself

# create a plot for test-your-partner