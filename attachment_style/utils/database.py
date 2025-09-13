from datetime import datetime as dt
from datetime import timedelta
import logging
import os
from sqlalchemy import literal_column, union_all
from sqlalchemy.orm import Session
from models import (
    Base,
    AssessYourself,
    AssessOthers,
)
from sqlalchemy import create_engine, select

try:
    DB_URL = os.environ['DB_URL']
    # DB_URL = os.environ['DB_URL_DEBUG']
except KeyError:
    raise RuntimeError("DB_URL environment variable not set.")

engine = create_engine(url=DB_URL)

logger = logging.getLogger(__name__)

def upload_to_db(
        answers: dict[str, tuple[str, float, str]],
        personal_answers: dict[str, str],
        test: bool = False,
):
    anxious_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "anxious"]
    )
    secure_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "secure"]
    )
    avoidant_answers = sorted(
        [(value[2], value[1]) for value in answers.values() if value[0] == "avoidant"]
    )
    values = []
    values.extend([value[1] for value in anxious_answers])
    values.extend([value[1] for value in secure_answers])
    values.extend([value[1] for value in avoidant_answers])

    if len(values) == 36:
        result_object = AssessYourself(
            timestamp=dt.now() + timedelta(hours=2),
            test=test,
            age=personal_answers["age"],
            relationship_status=personal_answers["relationship_status"],
            gender=personal_answers["gender"],
            therapy_experience=personal_answers["therapy_experience"],
            anxious_q1=values[0],
            anxious_q2=values[1],
            anxious_q3=values[2],
            anxious_q4=values[3],
            anxious_q5=values[4],
            anxious_q6=values[5],
            anxious_q7=values[6],
            anxious_q8=values[7],
            anxious_q9=values[8],
            anxious_q10=values[9],
            anxious_q11=values[10],
            anxious_q12=values[11],
            anxious_q13=values[12],
            anxious_q14=values[13],
            anxious_q15=values[14],
            anxious_q16=values[15],
            anxious_q17=values[16],
            anxious_q18=values[17],
            avoidant_q1=values[0],
            avoidant_q2=values[1],
            avoidant_q3=values[2],
            avoidant_q4=values[3],
            avoidant_q5=values[4],
            avoidant_q6=values[5],
            avoidant_q7=values[6],
            avoidant_q8=values[7],
            avoidant_q9=values[8],
            avoidant_q10=values[9],
            avoidant_q11=values[10],
            avoidant_q12=values[11],
            avoidant_q13=values[12],
            avoidant_q14=values[13],
            avoidant_q15=values[14],
            avoidant_q16=values[15],
            avoidant_q17=values[16],
            avoidant_q18=values[17],
        )
    elif len(values) == 33:
        result_object = AssessOthers(
            timestamp=dt.now() + timedelta(hours=2),
            test=test,
            age=personal_answers["age"],
            relationship_status=personal_answers["relationship_status"],
            gender=personal_answers["gender"],
            therapy_experience=personal_answers["therapy_experience"],
            anxious_q1=values[0],
            anxious_q2=values[1],
            anxious_q3=values[2],
            anxious_q4=values[3],
            anxious_q5=values[4],
            anxious_q6=values[5],
            anxious_q7=values[6],
            anxious_q8=values[7],
            anxious_q9=values[8],
            anxious_q10=values[9],
            anxious_q11=values[10],
            secure_q1=values[11],
            secure_q2=values[12],
            secure_q3=values[13],
            secure_q4=values[14],
            secure_q5=values[15],
            secure_q6=values[16],
            secure_q7=values[17],
            secure_q8=values[18],
            secure_q9=values[19],
            secure_q10=values[20],
            secure_q11=values[21],
            avoidant_q1=values[22],
            avoidant_q2=values[23],
            avoidant_q3=values[24],
            avoidant_q4=values[25],
            avoidant_q5=values[26],
            avoidant_q6=values[27],
            avoidant_q7=values[28],
            avoidant_q8=values[29],
            avoidant_q9=values[30],
            avoidant_q10=values[31],
            avoidant_q11=values[32],
        )
    else:
        raise ValueError("The number of answers is not correct")

    with Session(engine) as session:
        session.add(result_object)
        session.commit()


def retrieve_scores_from_db():
    stmt_you = select(
        literal_column("'AssessYourself'").label("source"),
        AssessYourself.age,
        AssessYourself.gender,
        AssessYourself.relationship_status,
        AssessYourself.therapy_experience,
        AssessYourself.anxious_score,
        AssessYourself.avoidant_score,
        AssessYourself.secure_score,
        AssessYourself.test,
    )
    stmt_others = select(
        literal_column("'AssessOthers'").label("source"),
        AssessOthers.age,
        AssessOthers.gender,
        AssessOthers.relationship_status,
        AssessOthers.therapy_experience,
        AssessOthers.anxious_score,
        AssessOthers.avoidant_score,
        AssessOthers.secure_score,
        AssessOthers.test,
    )
    query = union_all(stmt_you, stmt_others)

    with Session(engine) as session:
        results = session.execute(query).all()
        if not results:
            raise ValueError("No entries in the database...")

        # this is a list of dictionaries each representing one db entry:
        results_records_dict = [row._asdict() for row in results]

        keys = results_records_dict[0].keys()
        # this is one dictionary with column names as keys - what we need for plots
        results_long_dict = {
            key: [row[key] for row in results_records_dict] for key in keys
        }

        if not results_long_dict:
            logger.error("No data was retrieved from the database")

        for score in ["secure_score", "avoidant_score", "anxious_score"]:
            if None in results_long_dict[score]:
                logger.critical(f"None values in column {score}!!!")

        logger.info("Successfully retrieved the data from the database")
        return results_long_dict

def upload_objects_to_db(objects: list[Base]):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
