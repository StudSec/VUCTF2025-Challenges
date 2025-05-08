import base64


def decode_all(encoded: str):
    print(
        base64.b16decode(
            base64.b32decode(base64.b64decode(base64.b85decode(encoded)))
        ).decode()
    )


if __name__ == "__main__":
    decode_all(input("Enter encoded: "))
