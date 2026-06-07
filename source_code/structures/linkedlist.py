"""
Tự cài đặt Linked List.

Dùng để:
- Quản lý danh sách sinh viên
- Quản lý danh sách lớp

Các hàm:
- insert()
- delete()
- search()
- display()
"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next

        cur.next = new_node

    def delete(self, target):
        if not self.head:
            return False

        if self.head.data == target:
            self.head = self.head.next
            return True

        prev = self.head
        cur = self.head.next

        while cur:
            if cur.data == target:
                prev.next = cur.next
                return True

            prev = cur
            cur = cur.next

        return False

    def search(self, target):
        cur = self.head

        while cur:
            if cur.data == target:
                return cur.data

            cur = cur.next

        return None

    def display(self):
        result = []

        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next

        return result