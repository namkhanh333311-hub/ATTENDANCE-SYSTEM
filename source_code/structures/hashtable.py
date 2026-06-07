"""
Tự cài đặt Hash Table.

Mục đích:
Tra cứu sinh viên theo MSSV.

Key:
- MSSV

Value:
- Student

Các hàm:
- insert()
- search()
- delete()
"""
class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def insert(self, key, value):
        index = self._hash(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))

    def search(self, key):
        index = self._hash(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        return None

    def delete(self, key):
        index = self._hash(key)

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True

        return False