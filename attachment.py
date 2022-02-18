from pathlib import Path


class Attachment:
    def __init__(self, file_name, file_content):
        self.file_name = file_name
        self.file_format = file_name.split('.')[-1]
        self.file_content = file_content

    def save_to(self, destination):
        """Save Attachment to destination. Return destination

        *param destination*:    STR - path containing file extension
        """
        file_path = Path(destination)

        # Save file to destination if destination file does not exist yet
        # Else append '_1' to the base name
        if Path.is_file():
            path_parts = [i for i in file_path.parts]
            new_basename = f'{file_path.stem}_1{file_path.suffix}'
            path_parts[-1] = new_basename
            new_destination = '/'.join(path_parts)
            file_path = Path(new_destination)

        file_path.write_bytes(self.file_content)
        # with open(file_path, 'wb') as file:
        #     file.write(self.file_content)

        return file_path.name
