from dataclasses import dataclass
import random
from marshmallow import Schema, fields

class Question:
    def __init__(self, id, question, right_answer, wrong_answers_1, wrong_answers_2, wrong_answers_3, used, topic):            
        self.id = id
        self.question = question
        self.__right_answer = right_answer
        self.__wrong_answers_1 = wrong_answers_1
        self.__wrong_answers_2 = wrong_answers_2
        self.__wrong_answers_3 = wrong_answers_3
        self.used = used
        self.topic = topic
        self.options = []
        self.answer_index = None
        self.__transform_and_randomize()
    
    
    def __transform_and_randomize(self):

        # Combine all answers in one list
        all_answers = [            
            self.__right_answer,
            self.__wrong_answers_1,
            self.__wrong_answers_2,
            self.__wrong_answers_3
        ]

        # Shuffle them
        random.shuffle(all_answers)

        # The correct answer_index is now wherever the right_answer ended up
        answer_index = all_answers.index(self.__right_answer)
        self.options = all_answers
        self.answer_index = answer_index
    
class QuestionSchema(Schema):
    id = fields.Int()
    question = fields.Str()
    options = fields.List(fields.Str())
    answer_index = fields.Int()
    