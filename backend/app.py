from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

import sqlite3

from auth import encrypt_password, verify_password


app = Flask(__name__)

CORS(app)


app.config["JWT_SECRET_KEY"] = "ranjitha_secret_key"

jwt = JWTManager(app)



# Home Route

@app.route("/")
def home():

    return jsonify(
        {
            "message":"Task Management Backend Running"
        }
    )



# Register User

@app.route("/register", methods=["POST"])
def register():

    data = request.json


    username = data["username"]

    email = data["email"]

    password = encrypt_password(
        data["password"]
    )


    connection = sqlite3.connect(
        "task_manager.db"
    )

    cursor = connection.cursor()


    try:

        cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username,email,password)
        )


        connection.commit()


        return jsonify(
            {
                "message":"User registered successfully"
            }
        )


    except:

        return jsonify(
            {
                "message":"Email already exists"
            }
        )



    finally:

        connection.close()




# Login User

@app.route("/login", methods=["POST"])
def login():

    data=request.json


    email=data["email"]

    password=data["password"]



    connection=sqlite3.connect(
        "task_manager.db"
    )

    cursor=connection.cursor()



    cursor.execute(
    "SELECT * FROM users WHERE email=?",
    (email,)
    )


    user=cursor.fetchone()


    connection.close()



    if user and verify_password(password,user[3]):


        token=create_access_token(
            identity=user[0]
        )


        return jsonify(
            {
                "token":token
            }
        )



    return jsonify(
        {
            "message":"Invalid credentials"
        }
    )





# Create Task

@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():


    user_id=get_jwt_identity()


    data=request.json


    title=data["title"]

    description=data["description"]



    connection=sqlite3.connect(
        "task_manager.db"
    )

    cursor=connection.cursor()



    cursor.execute(
    """
    INSERT INTO tasks
    (user_id,title,description)
    VALUES(?,?,?)
    """,
    (user_id,title,description)
    )


    connection.commit()

    connection.close()



    return jsonify(
        {
            "message":"Task created"
        }
    )





# Get Tasks

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():


    user_id=get_jwt_identity()


    connection=sqlite3.connect(
        "task_manager.db"
    )

    cursor=connection.cursor()



    cursor.execute(
    """
    SELECT * FROM tasks
    WHERE user_id=?
    """,
    (user_id,)
    )


    tasks=cursor.fetchall()


    connection.close()



    return jsonify(tasks)





# Update Task

@app.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):


    data=request.json


    status=data["status"]



    connection=sqlite3.connect(
        "task_manager.db"
    )

    cursor=connection.cursor()



    cursor.execute(
    """
    UPDATE tasks
    SET status=?
    WHERE id=?
    """,
    (status,id)
    )


    connection.commit()

    connection.close()



    return jsonify(
        {
            "message":"Task updated"
        }
    )






# Delete Task

@app.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):


    connection=sqlite3.connect(
        "task_manager.db"
    )


    cursor=connection.cursor()



    cursor.execute(
    """
    DELETE FROM tasks
    WHERE id=?
    """,
    (id,)
    )


    connection.commit()

    connection.close()



    return jsonify(
        {
            "message":"Task deleted"
        }
    )





if __name__=="__main__":

    app.run(debug=True)
