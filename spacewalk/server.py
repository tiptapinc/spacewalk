import zerog


class Server(zerog.Server):
    def __init__(self, structure, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)

        self.structure = structure
