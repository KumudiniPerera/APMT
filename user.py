class User ():

    count = 1

    def __init__(self, username, email, password, id):
        self.username = username
        self.email= email
        self.password = password
        self.id = User.count
        User.count +=1
 
