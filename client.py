#!/usr/bin/env python3
# Sys for error handling and taking parameters from command line
import sys
import json

from socket import *


def send_to_server(message):
    server_name = str(sys.argv[1])
    server_port = int(sys.argv[2])
    clientsocket = socket(AF_INET, SOCK_STREAM)
    # Set a timeout of 10 seconds for all requests
    clientsocket.settimeout(10)
    clientsocket.connect((server_name, server_port))
    # Convert the message to a JSON string
    message = json.dumps(message)
    # Send the message
    clientsocket.send(message.encode())
    # Get the whole response
    receive = clientsocket.recv(1024).decode()
    total_response = ""
    while receive:
        total_response = total_response + receive
        receive = clientsocket.recv(1024).decode()
    # Convert into a python dictionary
    total_response = json.loads(total_response)
    clientsocket.close()
    return total_response


def get_messages(board):
    message = {"command": "GET_MESSAGES", "board": board}
    response_get_messages = send_to_server(message)
    if response_get_messages["error"] != "none":
        print(response_get_messages["error"])
        return
    response_get_messages = response_get_messages["messages"]
    if response_get_messages == {}:
        print("There are no messages in this board")
    else:
        for title, message in response_get_messages.items():
            print("Title:" + title + " Message:" + message)


def post_message(board_number, title, content):
    sentence = {
        "command": "POST_MESSAGE",
        "board": board_number,
        "title": title,
        "content": content,
    }
    response = send_to_server(sentence)
    if response["error"] != "none":
        print(response["error"])


def quit_all():
    message = {"command": "QUIT"}
    response = send_to_server(message)
    if response["error"] == "none":
        sys.exit()


boards_request = {"command": "GET_BOARDS"}

get_boards = send_to_server(boards_request)
if get_boards["error"] != "none":
    print(get_boards["error"])
    sys.exit()

for counter, value in enumerate(get_boards["boards"]):
    print(str(counter + 1) + "." + str(value))


def main():
    global get_boards
    # Take the input from the user
    command = input("What do you want to do?")

    # If the command is a number and is from the list
    if command.isdigit():
        if 1 <= int(command) <= len(get_boards["boards"]):
            get_messages(get_boards["boards"][int(command) - 1])
        else:
            print("The specified board does not exist")
    elif command == "POST":
        board_number = input("What board do you want to post to?")
        title = input("What is the title of your message?")
        content = input("What is the content of your message?")
        post_message(board_number, title, content)
    elif command == "QUIT":
        quit_all()
    else:
        print("Not a command")


while True:
    main()
