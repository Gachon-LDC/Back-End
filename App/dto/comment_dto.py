class CommentUpdateDTO:
    def __init__(self, uid, writer_id, body):
        self.uid = uid
        self.content = body.get("content", None)
        self.writer_id = writer_id
