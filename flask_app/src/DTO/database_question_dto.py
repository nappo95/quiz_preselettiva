from marshmallow_dataclass import class_schema
from models.questions import Question


class DatabaseQuestionDTO:
    
    @staticmethod
    def database_to_question_dto(database_question) -> Question:
        return Question(
            id=database_question[0],
            question=database_question[1],
            right_answer=database_question[2],
            wrong_answer_1=database_question[3],
            wrong_answer_2=database_question[4],
            wrong_answer_3=database_question[5],
            used=database_question[6]
        )
