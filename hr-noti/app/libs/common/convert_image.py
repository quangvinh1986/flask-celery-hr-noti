import base64


class ImageBase64:

    def __init__(self, full_file_name=""):
        self.full_file_name = full_file_name

    def encode_to_string(self, full_file_name=""):
        try:
            if not full_file_name:
                full_file_name = self.full_file_name
            base64_str = ""
            with open(full_file_name, "rb") as image_file:
                base64_str = base64.b64encode(image_file.read()).decode()
            return base64_str
        except Exception:
            return ""

    def decode_to_string(self, base64_str, full_file_name):
        try:
            fh = open(full_file_name, "wb")
            fh.write(base64_str.decode('base64'))
            fh.close()
            return full_file_name
        except Exception:
            return None
