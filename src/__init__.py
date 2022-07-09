from PIL import Image
from math import sqrt


class GifSeparate:
    def __init__(self, gif: Image.Image):
        self.gif = gif

    @property
    def _image_frames(self):  # return number of frames in gif
        try:
            while True:
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            return self.gif.tell()

    def separate(self):  # generator function, yield individual frames of gif
        for i in range(1, self._image_frames + 1):
            self.gif.seek(i)
            yield self.gif


class ImgFragment:
    def __init__(self, img: Image.Image):
        self.img = img

    def _nearest_square(self, limit: int):  # return  nearest square to limit
        i = 1
        while (i - 1) ** 2 < i ** 2 < limit:
            i += 1
        return (i - 1) ** 2

    def img_crop_to_square(self):  # crop the image into a square where sqrt(s) is not a decimal

        perfect_img = self.img.crop(  # crop images so that the square root of sides is perfect
            (0, 0, self._nearest_square(self.img.size[0]), self._nearest_square(self.img.size[1])))
        width, height = perfect_img.size

        if width >= height:  # if width is bigger than height, crop width to height
            dif = width - height
            return perfect_img.crop((dif // 2, 0, width - (dif // 2), height))
        elif height > width:
            dif = height - width
            return perfect_img.crop((0, dif // 2, width, height - (dif // 2)))

    def fragment(self):
        perfect_img = self.img_crop_to_square()
        result = []
        width, height = perfect_img.size
        s_sqrt = int(sqrt(width))
        for m in range(1, s_sqrt):
            for n in range(1, s_sqrt):
                result.append(((m, n), perfect_img.crop(((m - 1) * s_sqrt, (n - 1) * s_sqrt, m * s_sqrt, n * s_sqrt))))

        return result


class FragCombine:
    def __init__(self, imgs: list[Image.Image]):
        self.imgs = imgs

    def combine(self):
        pass



file = '../sample1.gif'

# with Image.open(file) as gif:
#     gifdivide = GifSeparate(gif)
#     img = next(gifdivide.separate())
#
#     frag = ImgFragment(img)
#     for i in frag.fragment():
#         print(i[0])
