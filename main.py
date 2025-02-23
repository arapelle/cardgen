import logging
from textwrap import wrap

from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image
# https://docs.wand-py.org/en/0.6.11/guide/draw.html#word-wrapping

from display.display import eog_display
from util.program import Program
from util.pxconv import to_px


class Cardgen(Program):
    def __init__(self):
        super().__init__("cardgen")
        self.__card_width = to_px("56mm")
        self.__card_height = to_px("86mm")
        self.__bg_color = Color("white")
        self.__card_border_width = to_px("5")

    def run(self):
        card_img = self.generate_card("bibesba")
        path = "rsc/output/card_wip.bmp"
        card_img.save(filename=path)
        eog_display(path)

    def generate_card(self, title: str):
        card_img = self.create_empty_card()
        self.draw_borders(card_img)
        with Drawing() as draw:
            # draw.font_family = "DejaVu Sans Mono"
            draw.font_size = 12
            draw.text(self.__card_border_width * 2, self.__card_border_width * 2 + 10, title)
            # draw.font_family = "Arial"
            draw.draw(card_img)
            draw.font_size = 9.5
            text = "Quand des haricots sont utilisés, vous pouvez récupérer 1 des haricots.\nVous devez au préalable réussir à faire un jet de dé impair si vous n’êtes pas sur la même tuile que le joueur concerné."
            text = self.draw_framed_text(card_img, draw, text, self.__card_width - (self.__card_border_width * 4),
                                         to_px("30mm"))
            draw.text(self.__card_border_width * 2, 60, text)
            draw.draw(card_img)
        return card_img

    def create_empty_card(self):
        card_img = Image(width=self.__card_width, height=self.__card_height, background=self.__bg_color)
        return card_img

    def draw_borders(self, card_img: Image):
        border_width = self.__card_border_width
        with Drawing() as draw:
            draw.fill_color = Color("black")
            draw.rectangle(left=0, top=0,
                           width=border_width, height=card_img.height)
            draw.rectangle(left=card_img.width - border_width - 1, top=0,
                           width=border_width, height=card_img.height)
            draw.rectangle(left=border_width + 1, top=0,
                           width=card_img.width - ((border_width + 1) * 2) - 1, height=border_width)
            draw.rectangle(left=border_width + 1, top=card_img.height - border_width - 1,
                           width=card_img.width - ((border_width + 1) * 2) - 1, height=border_width)
            draw.draw(card_img)

    def draw_framed_text(self, image, ctx, text, roi_width, roi_height):
        """Break long text to multiple lines, and reduce point size
        until all text fits within a bounding box."""
        mutable_message = text
        iteration_attempts = 100
        logging.info(f"roi_width={roi_width} roi_height={roi_height}")

        def eval_metrics(txt):
            """Quick helper function to calculate width/height of text."""
            metrics = ctx.get_font_metrics(image, txt, True)
            return (metrics.text_width, metrics.text_height)

        while ctx.font_size > 0 and iteration_attempts:
            iteration_attempts -= 1
            width, height = eval_metrics(mutable_message)
            if height > roi_height:
                ctx.font_size -= 0.75  # Reduce pointsize
                mutable_message = text  # Restore original text
            elif width > roi_width:
                columns = len(mutable_message)
                while columns > 0:
                    columns -= 1
                    lines = mutable_message.splitlines()
                    wrapped_lines = ['\n'.join(wrap(line, columns, replace_whitespace=False)) for line in lines]
                    candidate_message = '\n'.join(wrapped_lines)
                    wrapped_width, _ = eval_metrics(candidate_message)
                    if wrapped_width <= roi_width:
                        mutable_message = candidate_message
                        break
                if columns <= 0:
                    ctx.font_size -= 0.75  # Reduce pointsize
                    mutable_message = text  # Restore original text
            else:
                break
        if iteration_attempts < 1:
            raise RuntimeError("Unable to calculate word_wrap for " + text)
        return mutable_message


def main():
    cardgen = Cardgen()
    cardgen.run()
    logging.info("EXIT SUCCESS")


if __name__ == '__main__':
    main()
