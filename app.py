from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

from chat.chat_session import ChatSession

URL = "https://www.thegoodgood.co/"
NAME = 'The Good Good co'

app = Flask(__name__)
CORS(app)
chat_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    # Get user ID from Shopify session ID cookie
    session_id = request.cookies.get('session_id')
    request_data = request.get_json()
    print(request_data)
    # Check if user has an active session
    if session_id in chat_sessions.keys():
        chat_session = chat_sessions[session_id]
        if not chat_session.is_active():
            # If the session is inactive, delete it from the dictionary
            del chat_sessions[session_id]
            chat_session = None
    else:
        # If user does not have an active session, create a new one
        chat_session = ChatSession(session_id=session_id)
        chat_sessions[session_id] = chat_session

    if chat_session:
        # Update last activity time for the session
        chat_session.last_activity_time = datetime.now()

    # Process the chat message and return the response
    user_response = chat_session.query(request_data['data'])

    response = {
        'status': 'success',
        'data': {"chat_response": user_response}
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
