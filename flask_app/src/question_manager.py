from db_client import DBClient
from typing import List
from models.questions import Question

class QuestionManager:
    def __init__(self):
        self.__db_client = DBClient()
        self.__topics = ['diritto_civile']#,'diritto_commerciale', 'diritto_procedura_civile', 'diritto_tributario']
        self.__number_of_question_per_topic = 15

    def get_questions(self):
        questions = []
        for topic in self.__topics:
            db_questions = self.__db_client.get_quiz_questions(topic, self.__number_of_question_per_topic)
            for element in db_questions:
                questions.append(Question(*element, topic))
            # new_questions_dict = [self.db_question_DTO(question) for question in db_questions]
            # for question in new_questions_dict:
            #     questions.append(self.transform_and_randomize(question))
        return questions
    

    def mark_completed_questions(self, questions: List[Question]):
        questions_id_by_topic =  {}
        for topic in self.__topics:
            questions_id_by_topic[topic] = []
        for question in questions:
            questions_id_by_topic[question.topic].append(question.id)
            
        for topic in questions_id_by_topic:
            if questions_id_by_topic[topic]:
                self.__db_client.mark_completed_question(questions_id_by_topic[topic], topic)
    
            

if __name__ == "__main__":
    qm = QuestionManager()
    questions = qm.get_questions()
