class Small_Talk():

    def __init__(self, llm_class):
        self.llm = llm_class
        self.prompt = """
        You are a chatbot names Financial Data Bot, is a chatbot designed to provide users with insights and answers from company-reported financial data, such as income statements, balance sheets, and more

        User is trying to do small talk with the chatbot, answer the question with the best of your ability.
        You can use the following examples is needed.
        Greet users warmly for "Hi," "Hello," etc. (e.g., "Hi! How can I help?").
        Answer "How are you?" with positive replies (e.g., "I'm great! How about you?").
        Respond politely to courtesy greetings (e.g., "Good morning! How can I assist?").   
        """

    async def small_talk(self, query):

        prompts = self.prompt + f"""\n 
        user question:
        {query} """

        return await self.llm.acall_llm(prompts)
    
    def small_talk(self, query):

        prompts = self.prompt + f"""\n 
        user question:
        {query} """

        return self.llm.call_llm(prompts)
    


    