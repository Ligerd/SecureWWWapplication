class UserRequest:
    def __init__(self, request):
        self.login = request.form.get("login")
        self.password = request.form.get("password")

    def __str__(self):
        return "login: {0}, password: {1}".format(self.login, self.password)