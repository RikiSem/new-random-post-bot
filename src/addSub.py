from sys import argv
from app.Repositories.SubcsribersRepository import Subscribers

subscribers = Subscribers()

userId = argv[1]
subscribers.addNewSubscriber(userId)