class StoryState:
    def __init__(self):
        self.characters = []
        self.chapters = []
        self.memory = []

    def add_characters(self, characters):
        self.characters = characters

    def add_chapter(self, text):
        self.chapters.append(text)

    def add_memory(self, summary):
        self.memory.append(summary)

    def get_state(self):
        return {
            "characters": self.characters,
            "chapters": self.chapters,
            "memory": self.memory
        }


story_state = StoryState()
