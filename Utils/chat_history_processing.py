def get_historical_questions(chat_history):

    history = []

    if chat_history == {} or chat_history ==[]:
        return []

    for i in chat_history:
        if i['role'] == 'user':
            history.append(i['content'])
                           
    return history
