

#from Utils.chat_query import chat_query, conversation_query
from supabase import create_client
import ast

class ChatHistory:

    def __init__(self, user_id, SUPABASE_API_KEY):
        self.user_id = user_id
        self.url = "https://oinibrntdkrgcegmltai.supabase.co"
        self.key = SUPABASE_API_KEY
        self.client = create_client(self.url, self.key)

    def get_chat_history(self, user_id, last_n=5):
        output = self.client.table("chat_table").select("conversation_name", "conversation_id").eq("user_id", user_id).execute()
        output = sorted(output.data, key=lambda x: x['conversation_id'], reverse=True)
        output = output[:last_n]
        return output
        
    def get_conversation_history(self, user_id, conversation_id):
        output = self.client.table("chat_table").select("messages").eq("user_id", user_id).eq("conversation_id", conversation_id).execute()
        output = output.data[0]['messages']
        messages = ast.literal_eval(output)
        return messages

    def create_new_messages(self, user_id, chat_name, messages):
        output = self.client.table("chat_table").insert({"user_id": user_id, "conversation_name":chat_name , "messages":messages}).execute()
        return output.data[0]['conversation_id']

    def append_messages(self, user_id, conversation_id, messages):
        output = self.client.table("chat_table").update({"messages":messages}).eq("user_id", user_id).eq("conversation_id", conversation_id).execute()

    # def create_table(self, table_name, columns):
    #     # Construct the SQL statement for table creation
    #     columns_sql = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
    #     create_table_sql = f"""
    #     CREATE TABLE IF NOT EXISTS public.{table_name} (
    #         id SERIAL PRIMARY KEY,
    #         {columns_sql}
    #     );
    #     """

    #     # Execute the SQL statement using Supabase RPC
    #     response = self.client.rpc("execute_sql", {"sql": create_table_sql}).execute()
    #     return response


        