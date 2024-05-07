import colorsys
import math
import random
import cv2

from sender import Sender


class BadApple:
    def __init__(self, video_path):
        self.vidcap = cv2.VideoCapture(video_path)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        self.h = int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.w = int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h_in_chars = 11
        self.w_in_chars = int(self.h_in_chars * self.w / self.h * 2)
        self.show_every = 1

        self.chars2x2 = [' ', '▗', '▖', '▄', '▝', '▐', '▞', '▟', '▘', '▚', '▙', '▌', '▀', '▜', '▛', '█']
        self.chars1x2 = [' ', '▄', '▀', '█']

    def mainloop(self, debug_mode=True, start_frame=0):
        i = -1
        while True:
            success, image = self.vidcap.read()
            i += 1

            if not success: break

            if i < start_frame: continue
            if i % self.show_every != 0: continue

            text = self.image_to_ascii_1x2(image)
            text += f'\nframe #{i}, {i / self.fps:.2f}s'

            if debug_mode:
                Sender.log(text)
            else:
                Sender.send(text)

    def image_to_ascii_1x2(self, image_pixels):
        text = ''
        block_w, block_h = self.w / self.w_in_chars, self.h / self.h_in_chars
        for y in range(self.h_in_chars):
            for x in range(self.w_in_chars):
                sc_y0 = int(block_h * y)
                sc_y1 = int(block_h * (y + 1))
                sc_x0 = int(block_w * x)
                sc_x1 = int(block_w * (x + 1))

                pixels = image_pixels[sc_y0:sc_y1, sc_x0:sc_x1]

                t = pixels[:int(block_h // 2), :]
                b = pixels[int(block_h // 2):, :]

                t_brightness = self.count_averange_brightness(t) / 255
                b_brightness = self.count_averange_brightness(b) / 255

                t_bool = 0 if t_brightness < 0.5 else 1
                b_bool = 0 if b_brightness < 0.5 else 1

                index = (t_bool * 2 ** 1 +
                         b_bool * 2 ** 0)
                char = self.chars1x2[index]
                text += char

            text += '\n'
        text = text[:-1]
        return text

    def count_averange_brightness(self, pixels):
        """считает среднюю яркость чб картинки (смотрит только красный канал)"""
        s = 0
        count = 0
        for line in pixels:
            for color in line:
                s += color[0]
                count += 1
        return s / count

    def find_largest_size(self):
        for i in range(9, 15):
            h = i
            w = int(i * self.w / self.h * 2)
            text = ('█' * w + '\n') * h
            text = text[:-1]
            Sender.send(text)


def main():
    # BadApple('sources/bad_apple.mp4').find_largest_size()
    BadApple('sources/bad_apple.mp4').mainloop(debug_mode=False)


if __name__ == '__main__':
    main()
