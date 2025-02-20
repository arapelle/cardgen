from wand.image import Image
from display.display import eog_display


def main():
    with Image(filename='rsc/mona-lisa.jpg') as img:
        print(img.size)
        for r in 1, 2, 3:
            with img.clone() as i:
                i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                i.rotate(90 * r)
                i.save(filename='rsc/output/mona-lisa-{0}.png'.format(r))
                path = f"rsc/output/mona-lisa-{r}.png"
                eog_display(path)
                # display(i)


if __name__ == '__main__':
    main()
