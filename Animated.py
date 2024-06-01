class Animated:
    def __init__(self, name, sprite_seq, frametime=10, loop=0, x=-100, y=-100, visible=True):
        self.name = name
        self.x = x
        self.y = y
        self.visible = visible
        self.sprite = sprite_seq[0]
        self.frame_index = 0
        self.frame_list = sprite_seq
        self.frametime = frametime
        self.frame_counter = 0
        self.destroy = False
        self.playing = True
        self.loop = loop
        self.loop_no = 0
        self.x_offset = 0
        self.y_offset = 0

    def advance(self):
        changed = False
        if self.playing:
            self.frame_counter += 1

        if self.frame_counter >= self.frametime:
            self.frame_index += 1
            self.frame_counter = 0
            changed = True

        if self.frame_index >= len(self.frame_list):
            self.frame_index = 0
            self.loop_no += 1

        if self.loop and self.loop_no == self.loop:
            self.destroy = True

        if changed:
            self.sprite = self.frame_list[self.frame_index]
