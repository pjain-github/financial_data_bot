from Model.synthesizer.prompts import synthesizer_prompt, graph_prompt
from datetime import datetime
import os
import tempfile

class Synthesizer:
    def __init__(self, llm):
        """
        Initializes the Synthesizer with a Gemini LLM instance.
        :param gemini_api_key: API key for the Gemini model.
        """
        self.llm = llm
        self.synthesizer_prompt = synthesizer_prompt
        self.graph_prompt = graph_prompt

    def synthesize_answer(self, user_question, data):
        """
        Synthesize the answer to user question based on data.
        :param user_question: The question asked by the user.
        :data: Raw data to answer user question
        return: Text answer to user question.
        """

        date = datetime.today()
        prompt = self.synthesizer_prompt.format(
            date = date,
            question = user_question,
            data = data
        )
        
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        
        try:
            return response
        except Exception as e:
            return "Sorry no answer found"
        
    def create_chart(self, user_question, answer):
        """
        Categorizes the user question into predefined categories and identifies if a chart is requested.
        :param user_question: The question asked by the user.
        :answer : answer genreated from text
        :return: Python code to genreate chart
        """
        prompt = self.graph_prompt.format(
            question = user_question,
            answer = answer
        )
        
        graph_code = self.llm.call_llm([{"role": "user", "content": prompt}])

        return graph_code
        
        # with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        #     temp_file_name = temp_file.name
        #     temp_file.write(graph_code.encode())

        # try:
        #     # Execute the generated code
        #     exec(open(temp_file_name).read(), globals())
        # except Exception as e:
        #     print("Error executing graph code:", e)
        # finally:
        #     # Clean up the temporary file
        #     if os.path.exists(temp_file_name):
        #         os.remove(temp_file_name)
        #         return response
                
