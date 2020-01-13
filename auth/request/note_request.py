class NoteRequest:
    def __init__(self, request):
        self.shortcut = request.form.get('shortcut')
        self.note=request.form.get('note')

    def __str__(self):
        return "shortcut: {0}, note: {1}".format(self.shortcut,self.note)