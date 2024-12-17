class ChatHistory():

    def __init__(self, llm_class):
        self.llm = llm_class
        self.prompt = """
        Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.   

        Note:
        If no chat history is present, do not change the question. 
        Do not convert company ticker to company name.
        """

        # If ticker or year or quarter is missing from the question, utilize chat history to poplulate that data in the question.

    async def query_rewriter(self, chat_history, query):

        prompts = self.prompt + f"""\n 
        chat_history: 
        {chat_history}

        user question:
        {query} """

        return await self.llm.acall_llm(prompts)
    
    def query_rewriter(self, chat_history, query):

        prompts = self.prompt + f"""\n 
        chat_history: 
        {chat_history}

        user question:
        {query} """

        return self.llm.call_llm(prompts)
    


    