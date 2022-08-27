import sqlite3
from pathlib import Path

from data.media import Media
from data.tag import Tag


class DataBase:

    def __init__(self, file_name):
        self.file_name = file_name
        parent = Path(self.file_name).parent
        if not parent.exists():
            parent.mkdir(parents=True)
        self.con = sqlite3.connect(self.file_name)

        self.init_tables()

    def init_tables(self):
        cur = self.con.cursor()
        if not self.exists_table("tags"):
            cur = cur.execute("CREATE TABLE tags (tag_id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT, tag_category TEXT);")

        if not self.exists_table("medias"):
            cur = cur.execute("CREATE TABLE medias (media_id INTEGER PRIMARY KEY AUTOINCREMENT, media_name TEXT, media_type TEXT, media_hash TEXT, media_file_path TEXT);")

        if not self.exists_table("media_tags"):
            cur = cur.execute(
                "CREATE TABLE media_tags (media_id INTEGER NOT NULL, tag_id INTEGER NOT NULL, PRIMARY KEY (media_id, tag_id), FOREIGN KEY (media_id) REFERENCES medias (media_id) ON DELETE CASCADE, FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE CASCADE);")

        if not self.exists_table("duplicates"):
            cur = cur.execute(
                "CREATE TABLE duplicates (original INTEGER NOT NULL, duplicate INTEGER NOT NULL, PRIMARY KEY (original, duplicate), FOREIGN KEY (original) REFERENCES medias (media_id) ON DELETE CASCADE, FOREIGN KEY (duplicate) REFERENCES medias (media_id) ON DELETE CASCADE);")

        if not self.exists_table("media_tag_counts"):
            cur = cur.execute(
                "CREATE TABLE media_tag_counts (media_id INTEGER NOT NULL, tag_ID INTEGER NOT NULL, count INTEGER DEFAULT 0, PRIMARY KEY (media_id, tag_id), FOREIGN KEY (media_id) REFERENCES medias (media_id) ON DELETE CASCADE, FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE CASCADE)")
        self.con.commit()

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()

    def close(self):
        self.con.close()

    def exists_table(self, table_name):
        cur = self.con.cursor()

        # check if table exists
        cur = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name;", {"table_name": table_name})
        return cur.fetchone()

    def add_tag(self, tag: Tag):
        self.con.execute("INSERT INTO tags (tag_name, tag_category) VALUES (?, ?)", (tag.name, tag.category))
        self.con.commit()

    def update_tag(self, tag: Tag):
        self.con.execute("UPDATE tags SET tag_name=:tag_name, tag_category=:tag_category WHERE tag_id=:tag_id;", {"tag_name": tag.name, "tag_category": tag.category, "tag_id": tag.id})
        self.con.commit()

    def get_tag(self, tag_id: int):
        cur = self.con.cursor()

        cur = cur.execute("SELECT * FROM tags WHERE tag_id=:tag_id;", {"tag_id": tag_id})
        res = cur.fetchone()
        return Tag(res[1], res[2], res[0])

    def get_all_tags(self):
        cur = self.con.cursor()

        cur = cur.execute("SELECT * FROM tags;")
        res = cur.fetchall()
        return [Tag(tup[1], tup[2], tup[0]) for tup in res]

    def get_tags(self, tag_category):
        cur = self.con.cursor()

        cur = cur.execute("SELECT * FROM tags WHERE tag_category=:category;", {"category": tag_category})
        res = cur.fetchall()
        return [Tag(tup[1], tup[2], tup[0]) for tup in res]

    def remove_tag(self, tag_id):
        self.con.execute("DELETE FROM tags WHERE tag_id=:tag_id;", {"tag_id": tag_id})

    def add_media(self, media: Media):
        self.con.execute("INSERT INTO medias (media_name, media_type, file_hash, media_file_path) VALUES (?,?,?,?)", (media.name, media.media_type, media.file_hash, media.file_path))
        self.con.commit()

    def update_media(self, media: Media):
        self.con.execute("UPDATE medias SET media_name=:media_name, media_type=:media_type, file_hash=:file_hash, media_file_path=:file_path WHERE media_id=:media_id;",
                         {"media_name": media.name, "media_type": media.media_type, "file_hash": media.file_hash, "file_path": media.file_path})
        self.con.commit()

    def fill_media(self, media: Media):
        tags = self.get_all_media_tags(media.media_id)
        media.tags = tags
        media.tag_categories = set([tag.category for tag in tags])

    def get_medias(self, media_type, fill: bool = False):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM medias WHERE media_type=:type", {"type": media_type})
        medias = [Media(tup[1], tup[2], tup[3], tup[4], media_id=tup[0]) for tup in res]
        if fill:
            for media in medias:
                self.fill_media(media)
        return medias

    def get_all_medias(self, fill: bool = False):
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM medias;")
        medias = [Media(tup[1], tup[2], tup[3], tup[4], media_id=tup[0]) for tup in res]
        if fill:
            for media in medias:
                self.fill_media(media)
        return medias

    def remove_media(self, media_id):
        self.con.execute("DELETE FROM medias WHERE media_id=:media_id", {"media_id": media_id})

    def add_media_tag(self, media_id, tag_id):
        self.con.execute("INSERT INTO media_tags (media_id, tag_id) VALUES (?, ?)", (media_id, tag_id))
        self.con.commit()

    def get_media_tags(self, media_id, tag_category):
        cur = self.con.cursor()

        cur = cur.execute("SELECT tags.tag_id, tags.tag_name, tags.tag_category FROM media_tags INNER JOIN tags ON media_tags.tag_id = tags.tag_id WHERE media_id=:id AND tag_category=:category",
                          {"id": media_id, "category": tag_category})
        res = cur.fetchall()
        return [Tag(tup[1], tup[2], tup[0]) for tup in res]

    def get_all_media_tags(self, media_id):
        cur = self.con.cursor()

        cur = cur.execute("SELECT tags.tag_id, tags.tag_name, tags.tag_category FROM media_tags INNER JOIN tags ON media_tags.tag_id = tags.tag_id WHERE media_id=:id", {"id": media_id})
        res = cur.fetchall()
        return [Tag(tup[1], tup[2], tup[0]) for tup in res]

    def remove_media_tag(self, media_id, tag_id):
        self.con.execute("DELETE FROM media_tags WHERE media_id=:media_id AND tag_id=:tag_id", {"media_id": media_id, "tag_id": tag_id})

    def add_tag_count(self, media_id, tag_id, count):
        self.con.execute("INSERT INTO media_tag_counts (media_id, tag_id, count) VALUES (?,?,?)", (media_id, tag_id, count))
        self.con.commit()

    def get_media_tag_count(self, media_id, tag_id):
        cur = self.con.cursor()

        cur = cur.execute("SELECT count from media_tag_counts WHERE media_id=:media_id AND tag_id=:tag_id", {"media_id": media_id, "tag_id": tag_id})
        res = cur.fetchone()
        return res[0]

    def get_media_tag_counts(self, media_id):
        cur = self.con.cursor()

        cur = cur.execute("SELECT count from media_tag_counts WHERE media_id=:media_id", {"media_id": media_id})
        res = cur.fetchall()
        return [tup[0] for tup in res]

    def update_tag_count(self, media_id, tag_id, count):
        self.con.execute("UPDATE media_tag_counts SET count=:count WHERE media_id=:media_id AND tag_ID=:tag_id", {"media_id": media_id, "tag_id": tag_id, "count": count})
        self.con.commit()

    def remove_tag_count(self, media_id, tag_id):
        self.con.execute("DELETE FROM media_tag_counts WHERE media_id=:media_id AND tag_id=:tag_id", {"media_id": media_id, "tag_id": tag_id})

    def add_duplicate(self, original_id, duplicate_id):
        self.con.execute("INSERT INTO duplicates (original, duplicate) VALUES (?, ?)", (original_id, duplicate_id))
        self.con.commit()

    def remove_duplicate(self, original_id, duplicate_id):
        self.con.execute("DELETE FROM duplicates WHERE original=:original_id AND duplicate=:duplicate_id", {"original_id": original_id, "duplicate_id": duplicate_id})
