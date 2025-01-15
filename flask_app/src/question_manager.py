from db_client import DBClient
import random
from typing import Dict

class QuestionManager:
    def __init__(self):
        self.db_client = DBClient()
        self.__topics = ['diritto_civile','diritto_commerciale', 'diritto_procedura_civile', 'diritto_tributario']
        self.__number_of_question_per_topic = 15

    def get_questions(self):
        questions = []
        for topic in self.__topics:
            new_questions = self.db_client.get_quiz_questions(topic, self.__number_of_question_per_topic)
            new_questions_dict = [self.db_question_DTO(question) for question in new_questions]
            for question in new_questions_dict:
                questions.append(self.transform_and_randomize(question))
        return questions
    
    
    
    def db_question_DTO(self, db_question) -> Dict: 
        return {
            "question": db_question[1],
            "right_answer": db_question[2],
            "wrong_answers_1": db_question[3],
            "wrong_answers_2": db_question[4],
            "wrong_answers_3": db_question[5]
        }
    
    def transform_and_randomize(self, question):

        # Combine all answers in one list
        all_answers = [
            question["right_answer"],
            question["wrong_answers_1"],
            question["wrong_answers_2"],
            question["wrong_answers_3"]
        ]

        # Shuffle them
        random.shuffle(all_answers)

        # The correct answer_index is now wherever the right_answer ended up
        answer_index = all_answers.index(question["right_answer"])

        new_dict = {
            "question": question["question"],
            "options": all_answers,
            "answer_index": answer_index
        }
        return new_dict
            

if __name__ == "__main__":
    qm = QuestionManager()
    questions = qm.get_questions()
