import redis
import json
from ..entity.note import Note
import string
from ..exception.exception import InvalidChar,ToLongString
NOTE_COUNTER = "book_counter"
NOTE_ID_PREFIX = "book_"
class NoteService:
    def __init__(self):
        self.db = redis.Redis(host='client_redis', port=6381, decode_responses=True)
        if self.db.get(NOTE_COUNTER) == None:
            self.db.set(NOTE_COUNTER, 0)

    def saveNote(self, note_req,user_id,fid,access):
        print("Saving new note: {0}.".format(note_req))

        if len(note_req.shortcut)>18:
            raise ToLongString("Shortcat is to long \"{0}\". Maximum length is 18 characters".format(len(note_req.shortcut)))
        shortcut_check=self.string_verification(note_req.shortcut)
        if shortcut_check!=True:
            raise InvalidChar("Shortcat includes prohibited characters: \"{0}\"".format(shortcut_check))

        if len(note_req.note)>300:
            raise ToLongString("Note is to long \"{0}\". Maximum length is 300 characters".format(len(note_req.note)))
        note_check=self.string_verification(note_req.note)
        if note_check!=True:
            raise InvalidChar("Note includes prohibited characters: \"{0}\"".format(note_check))

        if access=="public":
            note = Note(self.db.incr(NOTE_COUNTER), user_id, note_req.shortcut, note_req.note,None)
        else:
            note=Note(self.db.incr(NOTE_COUNTER), user_id, note_req.shortcut, note_req.note,user_id)
        note_json = json.dumps(note.__dict__)
        self.db.set(fid, note_json)
        print("Saved new note: (id: {0}).".format(note.id))
        return note.shortcut

    def find_by_shortcut(self, shortcut):
        n = int(self.db.get(NOTE_COUNTER))

        for i in range(1, n + 1):
            note_id = NOTE_ID_PREFIX + str(i)

            if not self.db.exists(note_id):
                continue

            note_json = self.db.get(note_id)
            note = Note.from_json(json.loads(note_json))

            if note.shortcut == shortcut:
                return note

        return None

    def find_by_fid(self, fid):
        note_json=self.db.get(fid)
        note = Note.from_json(json.loads(note_json))
        return note

    def string_verification(self, string_value):
        allowed_characters = list(string.digits) + list(string.ascii_letters)
        letters = list(string_value)
        for letter in letters:
            if letter not in allowed_characters:
                return letter
        return True