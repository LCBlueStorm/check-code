# coding=utf-8

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


_letter_cases = "abcdefghjkmnpqrstuvwxy"
_upper_cases = _letter_cases.upper()
_numbers = ''.join(map(str, range(3, 10)))
init_chars = ''.join((_letter_cases, _numbers))

class CheckCode():
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 3)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''
    def __init__(self, size=(100, 30), chars=init_chars,
                 img_type="GIF", mode="RGB", bg_color=(255, 255, 255),
                 fg_color=(0, 0, 255), font_size=15,
                 font_type="/Library/Fonts/Arial Italic.ttf",
                 length=4, draw_lines=True, n_line=(1, 3), draw_points=True,
                 point_chance=2):
        self.size = size
        self.chars = chars
        self.img_type = img_type
        self.mode = mode
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font_size = font_size
        self.font_type = font_type
        self.length = length
        self.draw_lines = draw_lines
        self.n_line = n_line
        self.draw_points = draw_points
        self.point_chance = point_chance

    def create_check_code(self):
        img = Image.new(self.mode, self.size, self.bg_color)  # 创建图形
        draw = ImageDraw.Draw(img)   # 创建画笔
        if self.draw_lines:
            self._create_lines(draw)
        if self.draw_points:
            self._create_points(draw)
        strs = self._create_str(draw)

        params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
        img = img.transform(self.size, Image.PERSPECTIVE, params)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return img, strs

    def _get_chars(self):
        return random.sample(self.chars, self.length)

    def _create_lines(self, draw):
        line_num = random.randint(*self.n_line)
        for i in range(line_num):
            begin = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            end = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def _create_points(self, draw):
        width, height = self.size
        chance = min(100, max(0, int(self.point_chance)))
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def _create_str(self, draw):
        width, height = self.size
        c_chars = self._get_chars()
        str = ' %s ' % ' '.join(c_chars)

        font = ImageFont.truetype(self.font_type, self.font_size)
        font_width, font_height = font.getsize(str)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                    str, font=font, fill=self.fg_color)
        return ''.join(c_chars)

if __name__ == "__main__":
    check_code = CheckCode()
    code_img, code_str = check_code.create_check_code()
    print(code_img, code_str)
    code_img.save("static/images/%s.gif" % code_str, "jpeg")
    '''
    mstream = StringIO.StringIO()
    img = code_img
    img.save(mstream, "jpeg")
    '''