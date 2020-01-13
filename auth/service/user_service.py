import redis
import json
from ..entity.user import User
USER_COUNTER = "author_counter"
USER_ID_PREFIX = "author_"
from ..chipter import password_verification
class UserService:
    def __init__(self):
        self.db = redis.Redis(host='client_redis', port=6381, decode_responses=True)
        if self.db.get(USER_COUNTER) == None:
            self.db.set(USER_COUNTER, 0)

    def save(self, user_req):
        print("Saving new author: {0}.".format(user_req))

        user = User(self.db.incr(USER_COUNTER), user_req.login, user_req.password)

        author_id = USER_ID_PREFIX + str(user.id)
        author_json = json.dumps(user.__dict__)

        self.db.set(author_id, author_json)

        print("Saved new author: (id: {0}).".format(user.id))
        return user.id

    def addTestUser(self,login,password):
        user = User(self.db.incr(USER_COUNTER), login, password)

        author_id = USER_ID_PREFIX + str(user.id)
        author_json = json.dumps(user.__dict__)

        self.db.set(author_id, author_json)

        print("Saved new author: (id: {0}).".format(user.id))
        return user.id

    def find_by_login(self, login):
        n = int(self.db.get(USER_COUNTER))

        for i in range(1, n + 1):
            user_id = USER_ID_PREFIX + str(i)

            if not self.db.exists(user_id):
                continue

            user_json = self.db.get(user_id)
            user = User.from_json(json.loads(user_json))

            if user.login == login:
                return user

        return None


