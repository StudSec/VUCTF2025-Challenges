import base64


def encode_all(flag: str):
    print(
        base64.b85encode(
            base64.b64encode(base64.b32encode(base64.b16encode(flag.encode())))
        ).decode()
    )


if __name__ == "__main__":
    encode_all(input("Enter flag: "))
