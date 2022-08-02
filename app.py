from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://sareha:arman@cluster0.hteyi.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bakery"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)

@app.route("/",methods = ["get","post"])

def reply():
    res = MessagingResponse()
#    msg1 = response.message("I am Haram Emaan!")
#    msg2 = response.message("")
#    msg3 = response.message("")
#    msg2.media("https://images.unsplash.com/photo-1562176564-0280c730d87c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80")
#    msg3.media("http://www.africau.edu/images/default/sample.pdf")

    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    #msg = response.message(f"Thanks for contacting me. you have sent '{text}' from {number}")

    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message("Thanks for contacting, \n you can choose one of the following options: \n\n*Type*\n\n 1️⃣ To contact ue \n 2️⃣ To order *snaks* \n 3️⃣working hours. \n4️⃣ *address*")
        users.insert_one({"number": number, "status": "main", "messages":[]})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid option")
            return str(res)
        if option == 1:
            res.message("email: *rehanchoudhry@gmail.com*")
        elif option == 2:
            res.message("you have entered ordering mode :) ")
            users.update_one({"number" : number}, {"$set": {"status": "ordering"}})
            res.message("1. cake 1, \n cake 2 \n cake 3")
        elif option == 3:
            res.message("timing : *9am - 9pm*")
        elif option == 4:
            res.message("we have multiple stores: our main is in liberty")
        else:
            res.message("Please enter a valid option")
            return str(res)
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid option")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message("Thanks for contacting, \n you can choose one of the following options: \n\n*Type*\n\n 1️⃣ To contact ue \n 2️⃣ To order *snaks* \n 3️⃣working hours. \n4️⃣ *address*")
        elif 1<=option<=9:
            cakes = ["red velvet", "dark forest", "angel cake"]
            selected = cakes[option - 1]
            users.update_one({"number": number}, {"$set": {"status": "adress"}})
            users.update_one({"number": number}, {"$set": {"item": selected}})
            res.message("Excellent choince 😀")
            res.message("Please order your address to confirm your order")
        else:
            res.message("Please enter a valid option")


    users.update_one({"number": number},{"$push":{"messages": {"text": text, "date": datetime.now()}}})



    #if text == "Hi" or "Hi" in text:
    #    response.message("Hello")
    #else:
    #    response.message("I dont knot what to say")

    return str(res)

if __name__ == "__main__":
    app.run()
