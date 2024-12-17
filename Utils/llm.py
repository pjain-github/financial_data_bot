from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini:
    """
    A class to interact with the Gemini model using Google Generative AI services.

    Attributes:
        api_key (str): The API key required to access the Gemini model.
        model (str): The specific model used, default is "models/gemini-1.5-flash".
        llm (ChatGoogleGenerativeAI): An instance of the ChatGoogleGenerativeAI model.

    Methods:
        stream_llm(messages: list, stream: bool = False) -> generator:
            Streams the response from the LLM in chunks if streaming is enabled.

        call_llm(messages: list, stream: bool = False) -> str:
            Invokes the LLM with the given messages and returns the full response.
    """

    def __init__(self, api_key, model="models/gemini-1.5-flash"):
        """
        Initializes the Gemini class with an API key and model, and sets up the LLM instance.

        Args:
            api_key (str): Your API key for accessing the Gemini model.
            model (str): The model identifier, default is "models/gemini-1.5-flash".
        """
        self.model = model
        self.api_key = api_key

        # Initialize the ChatGoogleGenerativeAI with specified parameters
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0,         # Controls the creativity of the response
            max_tokens=None,       # No limit on the number of tokens in the response
            timeout=None,          # No timeout is set for the response
            max_retries=2,         # Number of retries in case of failure
            # Other optional parameters can be added here...
        )

    def stream_llm(self, messages, stream=True):
        """
        Streams the response from the LLM in chunks if streaming is enabled.

        Args:
            messages (list): A list of messages to be sent to the LLM.
            stream (bool): If True, enables streaming of the response.

        Yields:
            str: Chunks of content from the LLM as they are received.
        """
        if stream:
            response = ""
            for chunk in self.llm.stream(messages):
                response += chunk.content
                yield chunk.content  # Stream each chunk as it is received

    def call_llm(self, messages, stream=False):
        """
        Invokes the LLM with the given messages and returns the full response.

        Args:
            messages (list): A list of messages to be sent to the LLM.
            stream (bool): If True, streaming is enabled, but it is not used in this function.

        Returns:
            str: The full response content from the LLM.
        """
        response = self.llm.invoke(messages).content
        return response
    
    async def acall_llm(self, messages, stream=False):
        """
        Invokes the async LLM with the given messages and returns the full response.

        Args:
            messages (list): A list of messages to be sent to the LLM.
            stream (bool): If True, streaming is enabled, but it is not used in this function.

        Returns:
            str: The full response content from the LLM.
        """
        return await self.llm.ainvoke(messages)
    
    async def astream_llm(self, messages, stream=True):
        """
        Async streams the response from the LLM in chunks if streaming is enabled.

        Args:
            messages (list): A list of messages to be sent to the LLM.
            stream (bool): If True, enables streaming of the response.

        Yields:
            str: Chunks of content from the LLM as they are received.
        """
        if stream:
            response = ""
            async for chunk in self.llm.astream(messages):
                response += chunk.content
                yield chunk.content  # Stream each chunk as it is received
        

# class Gemini:
#     def __init__(self, api_key, model="gemini-1.5-flash"):
#         self.model = model
#         self.api_key = api_key

#         self.llm = ChatGoogleGenerativeAI(
#             model=self.model,
#             api_key=self.api_key,
#             temperature=0,
#             max_tokens=None,
#             timeout=None,
#             max_retries=2,
#             # other params...
#             )

#     def call_gemini(self, messages):
#         return self.llm.invoke(messages)

