from pathlib import Path

from data.media import Media
from data.naming_node import NamingNode


class NameGenerator:

    def __int__(self, root_node: NamingNode, root_folder: str):
        self.folder_map = {}
        self.global_count = 1
        self.root_node = root_node

    def generate_name(self, media: Media):
        name_parts = []

        old_path = Path(media.file_path)
        old_name = old_path.stem
        ext = old_path.suffix

        node = self.root_node
        while node:
            path_str = "/".join(name_parts)
            path = Path(path_str)
            folder_path = path.as_posix()
            if folder_path not in self.folder_map:
                self.folder_map[folder_path] = []
            action, res = node.info.generate_name(media, old_name, len(self.folder_map[folder_path]) + 1, self.global_count)
            if action:
                name_parts += [res]
                node = node.next

                path_str = "/".join(name_parts)
                path = Path(path_str)
                folder_path = path.as_posix()
                if folder_path not in self.folder_map:
                    self.folder_map[folder_path] = []
                if path.name not in self.folder_map[folder_path]:
                    self.folder_map[folder_path] = self.folder_map[folder_path] + [path.name]
            else:
                node = node.alternative

        path_str = "/".join(name_parts) + ext
        self.global_count += 1
        return path_str
