import redis
import json
from ..entity.note import Note
NOTE_COUNTER = "book_counter"
NOTE_ID_PREFIX = "book_"
class NoteService:
    def __init__(self):
        self.db = redis.Redis(host='client_redis', port=6381, decode_responses=True)
        if self.db.get(NOTE_COUNTER) == None:
            self.db.set(NOTE_COUNTER, 0)

    def saveNote(self, note_req,user_id,fid,access):
        print("Saving new note: {0}.".format(note_req))
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