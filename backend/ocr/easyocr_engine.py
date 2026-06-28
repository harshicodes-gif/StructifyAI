import easyocr

reader = easyocr.Reader(
    ["en"],
    gpu=False,
)


def extract_text(image_path):

    result = reader.readtext(image_path)

    text = []

    for _, value, _ in result:

        text.append(value)

    return "\n".join(text)