
## SQL
user_query = """
select user_id from user_table where email={email}
"""

chat_query = """
select conversation_id, conversation_name from chat_table where user_id = {user_id}
"""

conversation_query = """
select messages from chat_table where user_id = {user_id} and conversation_id = {conversation_id}
"""

