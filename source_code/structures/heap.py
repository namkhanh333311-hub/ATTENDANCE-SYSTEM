"""
Tự cài đặt Max Heap.

Dùng cho:
- Top sinh viên vắng nhiều nhất

Node lưu:
(absent_count, student)

Các hàm:
- insert()
- extract_max()
- heapify()
"""
class MaxHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def insert(self, item):
        self.heap.append(item)

        i = len(self.heap) - 1

        while i > 0:
            p = self._parent(i)

            if self.heap[p][0] < self.heap[i][0]:
                self.heap[p], self.heap[i] = self.heap[i], self.heap[p]
                i = p
            else:
                break

    def heapify(self, i):
        largest = i

        left = self._left(i)
        right = self._right(i)

        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left

        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify(largest)

    def extract_max(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]

        self.heap[0] = self.heap.pop()

        self.heapify(0)

        return root