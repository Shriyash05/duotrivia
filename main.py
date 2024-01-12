from tkinter.messagebox import QUESTION
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)


questions = [
"Bra/Dick size",
"Pubic Hair: Natural, trimmed, shaved, none",
"Do you have any body hair",
"(Guys Only) Are you Circumcised",
"How often you Masturbate",
"Have you ever watched porn",
"Ideal Sexual/Physical attributes",
"Favorite Sexual Fantasy",
"Turn Ons/Turn Offs",
"Any Kinks",
"Ideal Sexual Position",
"How do you masturbate",
"Do you own a toy",
"Have you ever been caught Masturbating",
"Have you ever walked in when someone was having sex"
,"Biggest fears of Sex"
,"Do you have any STDs"
,"How often are you horny"
,"Most embarrassing sexual story"
,"Are you currently horny",
"What do you expect in a sexual relationship",
"Are you a virgin",
"Have you ever seen anyone naked",
"Do you have piercing/tattoos",
"Have you ever had same-sex expirence",
"Have you ever sent a nude",
"Have you ever sexted",
"Have you ever kissed anyone"
,"Am I attractive"
,"Have you ever slept together"
,"Do you want to have sex"
]

rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code



@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/options/", methods=["POST", "GET"])
def options():
    return render_template("options.html")

@app.route("/home", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": [name], "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        rooms[room]["members"].append(name)
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"].append(name)
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"].remove(name)
        if not rooms[room]["members"]:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


current_question_index = 0

def get_random_question():
    random_question = random.choice(questions)
    return random_question


@socketio.on('next_question')
def next_question():
    room = session.get("room")
    if room not in rooms:
            return 

    current_user = session.get("name")
    other_users = [name for name in rooms[room]["members"] if name != current_user]
    unique_users = set(other_users)
    global user_turn_message
    
    # Emit the question individually to each unique user with the user's name followed by "'s turn"
    for user in unique_users:
        user_turn_message = f"{user}'s turn"
    question = get_random_question()
    emit('new_question', {'question': question, 'user': user_turn_message}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)