import winsound


class Letter:
    soundpath = "C:\\LearnArabic331\\alphabet\\Sound\\Bracket0\\"

    def __init__(self, file_name, file_extension=".wav"):
        self.file_path = Letter.soundpath + file_name + file_extension
        self.name = file_name

    def play_sound(self):
        winsound.PlaySound(self.file_path, winsound.SND_FILENAME)


def listen_arabic():
    alif = Letter("alif")
    ba = Letter("ba")

    # screen = pygame.display.set_mode((640, 480), 0, 32)
    # 
    # OLD WAY
    # funcs = {"Alif": Alif, "Ba": Ba}
    # 
    # NEW WAY #1
    # funcs = {alif.name: alif.play_sound, ba.name: ba.play_sound}
    # 
    # NEW WAY #2 (and the better way in my opinion)

    letters = [alif, ba]
    funcs = {}
    for letter in letters:
        funcs[letter.name] = letter.play_sound
    print(funcs)

    # ListenTextDisplay = "Listen to the Arabic Alphabet"
    # pygame.display.set_caption(ListenTextDisplay)
    # gm = GameMenu(screen, funcs.keys(), funcs)
    # 
    # gm.run()


listen_arabic()
