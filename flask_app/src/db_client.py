import mysql.connector

class DBClient:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='application',
            password='application',
            host='mysql',       # or your DB server IP
            database='quesiti'
    )

    def get_quiz_questions(self, table, number_of_questions=15):
        """
        Selects N random questions that haven't been used yet (used=0),
        marks them as used, and returns them.
        """
        cursor = self.conn.cursor()\
        
        # Select up to 15 random questions where used=0
        select_query = f"""
        SELECT *
        FROM {table}
        WHERE used = FALSE
        ORDER BY RAND()
        LIMIT {number_of_questions};
        """
        cursor.execute(select_query)
        quiz_questions = cursor.fetchall()

        if not quiz_questions:
            print(f"No unused questions left or fewer than {number_of_questions} available.")
            # Here you could either reset the 'used' field for all questions
            # or return fewer questions, or handle it another way.
            cursor.close()
            return []

        # Extract IDs from the fetched questions
        question_ids = [str(row[0]) for row in quiz_questions]

        # Mark the selected questions as used
        update_query = f"""
        UPDATE {table}
        SET used = TRUE
        WHERE id IN ({",".join(question_ids)});
        """
        # cursor.execute(update_query)
        self.conn.commit()

        cursor.close()

        return quiz_questions
    
    def mark_completed_question(self, ids, table):
        cursor = self.conn.cursor()
        update_query = f"""
        UPDATE {table}
        SET used = TRUE
        WHERE numer_quesito IN ({",".join(str(i) for i in ids)});
        """
        cursor.execute(update_query)
        self.conn.commit()
        cursor.close()
