# chat/consumers.py
import json

from asgiref.sync import async_to_sync                          # accesing async procedures in sync consumer
from channels.generic.websocket import WebsocketConsumer        # sync consumer
from channels.generic.websocket import AsyncWebsocketConsumer   # async consumer

from asgiref.sync import sync_to_async                         # accesing sync procedures in async consumer
from channels.db import database_sync_to_async

# This is a synchronous WebSocket consumer that accepts all connections, 
# receives messages from its client, and echos those messages back to the same client.

# Channels also supports writing asynchronous consumers for greater performance. 
# However any asynchronous consumer must be careful to avoid directly performing blocking operations, 
# such as accessing a Django model. 
# See the Consumers reference for more information about writing asynchronous consumers.
# https://channels.readthedocs.io/en/latest/topics/consumers.html

class TestWsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        message = "you said " + message

        self.send(text_data=json.dumps({"message": message}))

# Group names are restricted to ASCII alphanumerics, hyphens, and periods only 
# and are limited to a maximum length of 100

# The async_to_sync(...) wrapper is required because ChatConsumer is a synchronous WebsocketConsumer 
# but it is calling an asynchronous channel layer method. (All channel layer methods are asynchronous.)



# syncron consumer
# ----------------

# Synchronous consumers are convenient because they can call regular synchronous I/O functions 
# such as those that access Django models without writing special code

# Even if ChatConsumer did access Django models or other synchronous code it would still be possible 
# to rewrite it as asynchronous. 
# Utilities like asgiref.sync.sync_to_async and channels.db.database_sync_to_async can be used 
# to call synchronous code from an asynchronous consumer. 
# The performance gains however would be less than if it only used async-native libraries.

class ChatConsumer0(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
        
# A channel layer is a kind of communication system. It allows multiple consumer instances to talk with each other, and with other parts of Django.
# A channel layer provides the following abstractions:
#     A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.
#     A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.

# Every consumer instance has an automatically generated unique channel name, and so can be communicated with via a channel layer.
# In our chat application we want to have multiple instances of ChatConsumer in the same room communicate with each other. To do that we will have each ChatConsumer add its channel to a group whose name is based on the room name. That will allow ChatConsumers to transmit messages to all other ChatConsumers in the same room.
# We will use a channel layer that uses Redis as its backing store. To start a Redis server on port 6379, run the following command (press Control-C to stop it):
# $ docker run --rm -p 6379:6379 redis:7

# When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. 
# The ChatConsumer will receive that message and forward it to the group corresponding to the room name. 
# Every ChatConsumer in the same group (and thus in the same room) will then receive the message from the group and forward it over WebSocket back to JavaScript, where it will be appended to the chat log.        

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
        
        
# -----------------------------------------------------------------------------------------------------------


class ChatInterfonConsumer_sync(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))



online_users = []

# Dictionary to store user IDs and their connection status
online_users = {}


class ChatInterfonConsumer_async(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        # self.user_id = self.scope["user"].id  # Assuming user authentication is enabled
        self.name = self.scope["url_route"]["kwargs"]["name"]
        print("user name",self.name)

        # Check if user name is already connected
        if self.name in online_users:
            pass
            # user exist !
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user.exist", "name": self.name}
            )        
            
            # Reject connection
            #await self.close()
            #return            

        # Add user to online_users dictionary with connection status True
        #online_users.append(name)
        online_users[self.name] = self.channel_name     # True
        #print(online_users)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Add user to list of connected users
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user.join", "name": self.name}
        )

        await self.accept()


    
    # Handle user exist
    async def user_exist(self, event):
        name = event["name"]

        # Notify other users about the new user joining
        await self.send(text_data=json.dumps({"user_exist": {"name": name}}))


    # Handle user joining
    async def user_join(self, event):
        name = event["name"]
        #print("connect",name)

        # Notify other users about the new user joining
        await self.send(text_data=json.dumps({"user_join": {"name": name}}))
        
        # send all users list to socket   !!!
        #await self.channel_layer.group_send(
        #    self.room_group_name, {"type": "user.sendall", "online_users": online_users}
        #)          
        # send all users list to socket ?       
        await self.send(text_data=json.dumps({"user_sendall": {"online_users": json.dumps(online_users)}}))


    async def disconnect(self, close_code):
        print("diconnect")
        # Remove user from online_users dictionary
        #online_users.remove(self.name)
        online_users.pop(self.name, None)
        #print(online_users) 

        # send all users list to socket ?    !!!
        await self.channel_layer.group_send(
           self.room_group_name, {"type": "user.sendall", "online_users": online_users}
        )  
        # send all users list to socket
        #await self.send(text_data=json.dumps({"user_sendall": {"online_users": json.dumps(online_users)}}))        
        
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove user from list of connected users
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user.leave", "name": self.name}
        )

    # Handle send users
    async def user_sendall(self, event):
        online_users = event["online_users"]
        online_users = json.dumps(online_users)
        #print("user_sendall",online_users)

        # Notify other users about the new user joining
        await self.send(text_data=json.dumps({"user_sendall": {"online_users": online_users}}))        

    # Handle user leaving
    async def user_leave(self, event):
        name = event["name"]

        # Notify other users about the user leaving
        await self.send(text_data=json.dumps({"user_leave": {"name": name}}))



    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        recipient_name = text_data_json.get("recipient_name")
        prop = text_data_json.get("prop")
        #recipient_name = text_data_json["recipient_name"]
        #print(recipient_name)
        print(prop)

        # If recipient_name is provided, send the message to that specific user
        if recipient_name:
            #message["prop"] = prop
            #print(message)
            await self.send_message_to_user(recipient_name, message,prop)
        else:
            # Send message to room group if recipient_name is not provided
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message,"name": self.name,"prop":prop}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        name = event["name"]
        prop = event["prop"]
        #message  = f"[{name}] : {message}"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"name":name,"prop":prop}))        



    # adaugat ..............................................
    # Method to send message to a specific user
    # def send_message_to_user(self, user_id, message):
    #     # Get the channel name(s) associated with the given user ID
    #     user_channels = [channel_name for name, channels in online_users.items() if user_id in channels]

    #     # Send message to each channel associated with the user ID
    #     for channel_name in user_channels:
    #         async_to_sync(self.channel_layer.send)(channel_name, {"type": "send_to_user", "message": message})

    # # Receive message from send_message_to_user method
    # async def send_to_user(self, event):
    #     message = event["message"]

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({"message": message}))        
    # ............................................    


    async def chat_sendcandidate(self, event):
        
        message = event["message"]
        message = message
        name = event["name"]
        prop = event["prop"]
        #message  = f"[{name}] : {message}"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"sendcandidate": message,"name":name,"prop":prop}))   


    async def chat_sendoffer(self, event):
        
        message = event["message"]
        message = message
        name = event["name"]
        prop = event["prop"]
        #message  = f"[{name}] : {message}"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"sendoffer": message,"name":name,"prop":prop}))   

    async def chat_sendanswer(self, event):
        
        message = event["message"]
        message = message
        name = event["name"]
        prop = event["prop"]
        #message  = f"[{name}] : {message}"

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"sendanswer": message,"name":name,"prop":prop}))       
    
    
    # Method to send message to a specific user
    async def send_message_to_user(self, recipient_name, message,prop):
        #print("prop",prop)
        recipient_channel = online_users.get(recipient_name)
        if recipient_channel:
            # await self.channel_layer.send(recipient_channel, {
            #     #"type": "chat.message",      # merge
            #     "type": "chat.sendoffer",    # nou
            #     "prop": prop,
            #     "message": message,
            #     "name": self.name  # Include sender's name in the message
            # })    

            if prop == "offer":
                await self.channel_layer.send(recipient_channel, {
                    "type": "chat.sendoffer",
                    "prop": prop,
                    "message": message,
                    "name": self.name  # Include sender's name in the message
                })    
            

            if prop == "answer":
                await self.channel_layer.send(recipient_channel, {
                    "type": "chat.sendanswer",
                    "prop": prop,
                    "message": message,
                    "name": self.name  # Include sender's name in the message
                })  


            if prop == "candidate":
                await self.channel_layer.send(recipient_channel, {
                    "type": "chat.sendcandidate",
                    "prop": prop,
                    "message": message,
                    "name": self.name  # Include sender's name in the message
                })  

            
            #await self.send(text_data=json.dumps({"send_offer": {"name": name}}))

            
# ##########################################
# sendoffer => self.channel_name = "SENDER" #
# the other self.channel_name = "RECEIVER"  #
# ##########################################

users = []         

# [
    # {'specific.c1d599cd25d344d2915a0df137de2c05!5e94a73271ee4f31b8d76a109dd131be': {'identity': 'undefined'}}, 
    # {'specific.c1d599cd25d344d2915a0df137de2c05!3d24bdcd6c3d4142a79c0605f10a56b8': {'identity': 'undefined'}}
# ]

def remove_user(channel):
    for user in users:
        if channel in user:
            print("found",user)
            print(type(channel))
            key = list(user.keys())
            print(key)

            users.remove(user)
            #user.del()
            #users[user].delete()
            

def get_user_name(channel):
    pass
    for user in users:
        if channel in user:
            return user[channel]["user"]
    return "undefined"    

def reset_users():
    print(users)
    users.clear()
    #for user in users:
    #    print(user)
    #    users.remove(user)
        #print(users[user])
        #users.remove(user)
        #user.del()
        #users[user].delete()
    #users = []
    #print(id(users))
    print("after reset",users)


def reset_identities():
    pass
    for user in users:
        # get key
        key = list(user.keys())[0] 
        user[key]["identity"] = "undefined"

def set_sender_receceiver2(sender_channel,receiver_channel):
    pass
    for user in users:
        if sender_channel in user:
            user[sender_channel]["identity"] = "SENDER"
    for user in users:
        if receiver_channel in user:
            user[receiver_channel]["identity"] = "RECEIVER"
            


def set_sender_receiver(channel):
    pass
    for user in users:
        #print(">",user)
        if channel in user:
            user[channel]["identity"] = "SENDER"        
    for user in users:
        # get key
        key = list(user.keys())[0]
        if user[key]["identity"] != "SENDER":
            user[key]["identity"] = "RECEIVER"
            
    print(users)

def get_receiver():
    pass
    for user in users:
        # get key
        key = list(user.keys())[0]
        if user[key]["identity"] == "RECEIVER":        
            return key

def get_sender():
    pass
    for user in users:
        # get key
        key = list(user.keys())[0]
        if user[key]["identity"] == "SENDER":        
            return key

def get_the_other_channel(channel):
    for user in users:
        # get key
        key = list(user.keys())[0]        
        if key != channel:
            return key

# if sender return receiver
# if receiver return sender
def get_channel_identity(channel):
    pass
    # what is that channel?
    for user in users:
        if channel in user:
            identity = user[channel]["identity"]
    
    # if identity == "SENDER":
    #     theother = "RECEIVER"
    # else:
    #     theother = "SENDER"    
                
    return identity
    
    
    # for user in users:
    #     # get key
    #     key = list(user.keys())[0]        
    #     if key != channel:
    #         return key

            
# class ChatConsumer000(WebsocketConsumer):
#     def connect(self):
        
#         #print(self.scope)
#         #print(self.scope["url_route"])
#         #print(self.scope["url_route"]["kwargs"])
#         print(self.channel_name)
#         #print("client",self.scope["client"])
#         #print("user",self.scope["user"])

#         users.append(
#             {
#                 self.channel_name:{
#                     "identity": "undefined"
#                 }
#             }
#         )
#         print(users)
        
#         #self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
#         # Join room group
#         #async_to_sync(self.channel_layer.group_add)(
#         #    self.room_group_name, self.channel_name
#         #)

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             "test", self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         pass
#         print("diconnect")


#     def receive(self, text_data):
#         print("server receive ",text_data)
        
#         text_data_json = json.loads(text_data)
#         case = text_data_json["case"]
        
#         if(case == "test_message"):
#             test_message = text_data_json["message"]
#             print("test message: ", test_message, self.channel_name)
#             # Send message to room group
#             async_to_sync(self.channel_layer.group_send)(
#                "test", {"type": "chat.message", "message": test_message, "case": case}
#             )            
        
#         #if(case == "channel"):
#         #    pass
            

#         #if(case == "send_candidate"):
#         #    pass
       
#         # relay candidate (send candidate)
#         if(case == "store_candidate"):
#             pass
        
#             candidate = text_data_json["candidate"]         
#             async_to_sync(self.channel_layer.group_send)(
#                 "test", {"type": "chat.message", "message": candidate, "case": "candidate"}
#             ) 

       
#         # relay offer (send offer)
#         if(case == "store_offer"):
#             pass       
        
#             # set SENDER/RECEIVER  description          
#             set_sender_receiver(self.channel_name)
        
#             offer = text_data_json["offer"]   
                  
#             async_to_sync(self.channel_layer.group_send)(
#                 "test", {"type": "chat.message", "message": offer, "case": "offer"}
#             ) 


#         if(case == "send_answer"):
#             pass           
       
#             answer = text_data_json["answer"] 
#             async_to_sync(self.channel_layer.group_send)(
#                 "test", {"type": "chat.message", "message": answer, "case": "answer"}
#             )             
            



#     # # Receive message from room group
#     def chat_message(self, event):
#         case = event["case"]
#         message = event["message"]
#         print("send===>",case)
        
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"case":case,"message": message}))
#         #self.send(text_data=json.dumps({"type":arg_type,arg_type:message}))
        
        
        










# class ChatConsumer001(WebsocketConsumer):
#     def connect(self):
        
#         #print(self.scope)
#         #print(self.scope["url_route"])
#         #print(self.scope["url_route"]["kwargs"])
#         print(self.channel_name)
#         #print("client",self.scope["client"])
#         #print("user",self.scope["user"])

#         users.append(
#             {
#                 self.channel_name:{
#                     "identity": "undefined"
#                 }
#             }
#         )
#         print(users)
        
#         #self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
#         # Join room group
#         #async_to_sync(self.channel_layer.group_add)(
#         #    self.room_group_name, self.channel_name
#         #)

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             "test", self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         print("server receive ",text_data)
        
#         text_data_json = json.loads(text_data)
#         case = text_data_json["case"]
        
#         if(case == "test_message"):
#             test_message = text_data_json["message"]
#             print("test message: ", test_message, self.channel_name)
#             # Send message to room group
#             async_to_sync(self.channel_layer.group_send)(
#                "test", {"type": "chat.message", "message": test_message, "case": case}
#             )            
        
#         #if(case == "store_user"):
#         #    pass
            

#         # if(case == "send_candidate"):
#         #     pass
       
#         # # relay candidate (send candidate)
#         # if(case == "store_candidate"):
#         #     pass
        
#         #     candidate = text_data_json["candidate"]         
#         #     async_to_sync(self.channel_layer.group_send)(
#         #         "test", {"type": "chat.message", "message": candidate, "case": "candidate"}
#         #     ) 

       
#         # relay offer (send offer)
#         if(case == "offer"):
#             pass       
        
#             # set SENDER/RECEIVER  description          
#             set_sender_receiver(self.channel_name)
        
#             offer = text_data_json["message"]         
#             async_to_sync(self.channel_layer.group_send)(
#                 "test", {"type": "chat.message", "message": offer, "case": "offer"}
#             ) 


#         # if(case == "send_answer"):
#         #     pass           
       
#         #     answer = text_data_json["answer"] 
#         #     async_to_sync(self.channel_layer.group_send)(
#         #         "test", {"type": "chat.message", "message": answer, "case": "answer"}
#         #     )             
            



#     # # Receive message from room group
#     def chat_message(self, event):
#         case = event["case"]
#         message = event["message"]
#         print("send===>",case)
        
#         if case == "test_message":
        
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({"case":case,"message": message}))
#             #self.send(text_data=json.dumps({"type":arg_type,arg_type:message}))        
        
        
#         if case == "offer":
#             pass
#             receiver_channel = get_receiver()
#             print("send offer only to receiver channel",receiver_channel)
#             async_to_sync(self.channel_layer.send(receiver_channel, {
#                 "case": "offer",
#                 "message": message,
#             }))         
            
            
            
# class ChatInterfonConsumer_async3(AsyncWebsocketConsumer):
#     global users
    
#     async def connect(self):
#         pass            
    
#         #print(self.scope)
#         #print(self.scope["url_route"])
#         #print(self.scope["url_route"]["kwargs"])
#         print(self.channel_name)
#         #print("client",self.scope["client"])
#         #print("user",self.scope["user"])

#         users.append(
#             {
#                 self.channel_name:{
#                     "identity": "undefined"
#                 }
#             }
#         )
#         print(id(users),users)
        
#         # Join room group
#         await self.channel_layer.group_add(
#             "test", self.channel_name
#         )

#         await self.accept()        
        
#     async def disconnect(self, close_code):
#         pass
#         print("disconnect")
#         print(users)
        
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         pass        
#         print("server receive ",text_data)
        
#         text_data_json = json.loads(text_data)
#         case = text_data_json["case"]    
        
#         if(case == "reset"):
#             pass
#             reset_users()
        
#         if(case == "test_message"):
#             test_message = text_data_json["message"]
#             print("test message: ", test_message, self.channel_name)
#             # Send message to room group
#             await self.channel_layer.group_send(
#                "test", {"type": "chat.message", "message": test_message, "case": case}
#             )          
            

#         if(case == "offer"):
#             pass       
        
#             # set SENDER/RECEIVER  description          
#             set_sender_receiver(self.channel_name)

#             receiver_channel = get_receiver()
        
#             offer = text_data_json["message"]         

#             await self.channel_layer.send(receiver_channel, {
#                 "type": "chat.sendoffer",
#                 "case": "offer",
#                 "message": offer,
#             }) 


#         if(case == "answer"):
#             pass       
        
#             sender_channel = get_sender()
        
#             answer = text_data_json["message"]         

#             await self.channel_layer.send(sender_channel, {
#                 "type": "chat.sendanswer",
#                 "case": "answer",
#                 "message": answer,
#             }) 


#         if(case == "candidate"):
#             pass 
#             candidate = text_data_json["message"]
#             sender_candidate = self.channel_name
#             destination_candidate = get_the_other_channel(sender_candidate)
            
#             print(f"candidate from {self.channel_name} {sender_candidate}")
#             print(f"sending to {destination_candidate}")
            
#             await self.channel_layer.send(destination_candidate, {
#                 "type": "chat.sendcandidate",
#                 "case": "candidate",
#                 "message": candidate,
#             })             
            
            
#     # # Receive message from room group
#     async def chat_message(self, event):
#         case = event["case"]
#         message = event["message"]
#         print("send===>",case)
        
#         if case == "test_message":
        
#             # Send message to WebSocket
#             await self.send(text_data=json.dumps({"case":case,"message": message}))


   
#     async def chat_sendoffer(self, event):
        
#         offer = event["message"]
#         case = event["case"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": offer,"case":case}))        
        


#     async def chat_sendanswer(self, event):
        
#         answer = event["message"]
#         case = event["case"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": answer,"case":case})) 
        

#     async def chat_sendcandidate(self, event):
        
#         candidate = event["message"]
#         case = event["case"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": candidate,"case":case}))         
        




        
from django.contrib.auth.models import User


class ChatInterfonConsumer_async4(AsyncWebsocketConsumer):
    global users

    @database_sync_to_async
    #@sync_to_async
    def get_user(self, user_name):
        try:
            return User.objects.get(username=user_name)
        except User.DoesNotExist:
            return None
    
    async def connect(self):
        pass            

        #other_username = self.scope['url_route']['kwargs']['username']
        #self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #self.room_group_name = f"chat_{self.room_name}"
        self.room_group_name = "test"
    
        print(self.scope)
        #print(self.scope["url_route"])
        #print(self.scope["url_route"]["kwargs"])
        print(self.channel_name)
        #print("client",self.scope["client"])
        print("user",self.scope["user"])
                
        #use a thread or sync_to_async
        u = await self.get_user(self.scope["user"])
        self.name = u.username

        users.append(
            {
                self.channel_name:{
                    "identity": "undefined",
                    "user": self.name
                }
            }
        )
        print(id(users),users)
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        # Add user to list of connected users
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user.join", "name": self.name}
        )

        await self.accept()        



    # Handle user joining
    async def user_join(self, event):
        pass
        name = event["name"]
        print("connect",self.name)

        # Notify other users about the new user joining
        await self.send(text_data=json.dumps({"user_join": {"name": name}}))
        
        # send all users list to socket
        await self.send(text_data=json.dumps({
            "user_sendall": {"users": json.dumps(users)}
        }))
        
        #await self.send(text_data=json.dumps({
        #    "case":"user_sendall",
        #    "message": {"online_users": json.dumps(users)}
        #}))  

        
    async def disconnect(self, close_code):
        pass
        print("disconnect")
        #print(users)
        # Remove user from online_users dictionary
        #online_users.remove(self.name)
        #print(self.channel_name)
        #users.pop(str(self.channel_name))
        #print(online_users) 

        remove_user(self.channel_name)

        print("after removing")

        # send all users list to socket
        await self.channel_layer.group_send(
           self.room_group_name, {"type": "user.sendall", "users": users}
        )  

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # # Remove user from list of connected users
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user.leave", "name": self.name}
        )

        print("end")



    # Handle user disconecting
    async def user_leave(self, event):
        name = event["name"]

        # Notify other users about the user leaving
        await self.send(text_data=json.dumps({"user_leave": {"name": name}}))


    # Receive message from WebSocket
    async def receive(self, text_data):
        pass        
        print("server receive ",text_data, self.channel_name)
        
        sender_channel = self.channel_name
        
        text_data_json = json.loads(text_data)
        case = text_data_json["case"]    
        
        if(case == "reset"):
            pass
            #reset_users()
            reset_identities()
            print("after succesful connection",users)
        
        
        
        if(case == "chat_all"):
            pass
            message_to_all = text_data_json["message"]
            # Send message to room group
            await self.channel_layer.group_send(
               "test", {"type": "chat.message", "message": message_to_all, "case": case,"sender":sender_channel}
            )             
        
        
        if(case == "test_message"):
            test_message = text_data_json["message"]
            print("test message: ", test_message, self.channel_name)
            # Send message to room group
            await self.channel_layer.group_send(
               "test", {"type": "chat.message", "message": test_message, "case": case,"sender":sender_channel}
            )          
            

        if(case == "offer"):
            pass       
        
            # set SENDER/RECEIVER  description          
            #set_sender_receiver(self.channel_name)
            #receiver_channel = get_receiver()
        
            #offer = text_data_json["message"]         

            data = text_data_json["message"]
            receiver_channel = data["channel_dest"]        # this is the receiver
            offer = data["offer"]

            # sender_channel                                # this is the sender  (defined above)
            
            set_sender_receceiver2(sender_channel,receiver_channel)

            await self.channel_layer.send(receiver_channel, {
                "type": "chat.sendoffer",
                "case": "offer",
                "message": offer,
            }) 


        if(case == "answer"):
            pass       
        
            sender_channel = get_sender()
        
            answer = text_data_json["message"]         

            await self.channel_layer.send(sender_channel, {
                "type": "chat.sendanswer",
                "case": "answer",
                "message": answer,
            }) 


        if(case == "candidate"):
            pass 
            candidate = text_data_json["message"]
            sender_candidate = self.channel_name
            #print("-> candidate sender: ",sender_candidate)
            #destination_candidate = get_the_other_channel(sender_candidate)
            
            # modification in progress...
            identity = get_channel_identity(sender_candidate)
            if identity == "SENDER":
                theother = "RECEIVER"
                destination_candidate = get_receiver()
            else:
                theother = "SENDER"              
                destination_candidate = get_sender()
            # --------------------------    
            
            print(f"candidate from {self.channel_name} {sender_candidate}")
            print(f"sending to {destination_candidate}")
            
            await self.channel_layer.send(destination_candidate, {
                "type": "chat.sendcandidate",
                "case": "candidate",
                "message": candidate,
            })             
            
            
    # # Receive message from room group
    async def chat_message(self, event):
        case = event["case"]
        sender = event["sender"]
        message = event["message"]
        print("send===>",case)
        
        if case == "test_message":
        
            # Send message to WebSocket
            #await self.send(text_data=json.dumps({"case":case,"message": message}))
            print("test message")
            await self.send(text_data=json.dumps({case: message}))
            
        if case == "chat_all":
        
            # Send message to WebSocket
            #await self.send(text_data=json.dumps({"case":case,"message": message}))
            print("chat all ",self.channel_name)
            username = get_user_name(sender)
            await self.send(text_data=json.dumps({case:  f"[{username}] {message}"}))
            

   
    async def chat_sendoffer(self, event):
        
        offer = event["message"]
        case = event["case"]

        # Send message to WebSocket
        #await self.send(text_data=json.dumps({"message": offer,"case":case}))        
        await self.send(text_data=json.dumps({case: offer}))


    async def chat_sendanswer(self, event):
        
        answer = event["message"]
        case = event["case"]

        # Send message to WebSocket
        #await self.send(text_data=json.dumps({"message": answer,"case":case})) 
        await self.send(text_data=json.dumps({case: answer}))

    async def chat_sendcandidate(self, event):
        
        candidate = event["message"]
        case = event["case"]

        # Send message to WebSocket
        #await self.send(text_data=json.dumps({"message": candidate,"case":case}))
        await self.send(text_data=json.dumps({case: candidate}))                    # Handle send users
        
                
   # Handle send users for disconnectig case
    async def user_sendall(self, event):
        users = event["users"]
        users = json.dumps(users)
        #print("user_sendall",online_users)

        # Notify other users about the new user joining
        await self.send(text_data=json.dumps({"user_sendall": {"users": users}}))           