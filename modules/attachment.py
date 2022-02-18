"""EMAIL ATTACHMENT OBJECT

Class allowing to easily access the metadata of an attachment and to store the
file.

Last update: Feb 18, 2022
"""
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
        counter = 1

        # Save file to destination if destination file does not exist yet
        # Else append counter to the basename
        while file_path.is_file():
            # create a new basename for the file (add counter)
            if counter < 2:
                new_basename = f'{file_path.stem}_{counter}{file_path.suffix}'
            else:
                new_basename = f'{file_path.stem[:-2]}_{counter}' \
                    + file_path.suffix

            # increment the counter
            counter += 1

            # get all parts of the path and modify the last element
            path_parts = [i for i in file_path.parts]
            path_parts[-1] = new_basename

            # create a new path string
            new_destination = '/'.join(path_parts)

            # save new path string as Path object
            file_path = Path(new_destination)

        file_path.write_bytes(self.file_content)
        # with open(file_path, 'wb') as file:
        #     file.write(self.file_content)

        return file_path.name
