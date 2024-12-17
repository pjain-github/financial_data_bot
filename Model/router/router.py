from Model.router.prompts import router_prompt

class Router:
    def __init__(self, llm):
        """
        Initializes the Router with a Gemini LLM instance.
        :param gemini_api_key: API key for the Gemini model.
        """
        self.llm = llm
        self.prompt = router_prompt

    def categorize_question(self, user_question):
        """
        Categorizes the user question into predefined categories and identifies if a chart is requested.
        :param user_question: The question asked by the user.
        :return: A JSON object with the type of question and graph preference.
        """
        prompt = self.prompt + f"""{user_question}
            Follow the steps above and return a structured JSON response in the required format."""
        
        response = self.llm.call_llm([{"role": "user", "content": prompt}])
        
        try:
            response = response[3:-4].split("json")[1]

            result = eval(response)
            return result
        except Exception as e:
            return {'type': 'unknown', 'graph': False, 'error': str(e)}
        