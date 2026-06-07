"""
Thuật toán Heap Sort.

Dùng để:
- Sắp xếp sinh viên theo số buổi vắng

Độ phức tạp:
O(n log n)
"""
from structures.heap import MaxHeap


def heap_sort(data):
    heap = MaxHeap()

    for item in data:
        heap.insert(item)

    result = []

    while heap.heap:
        result.append(heap.extract_max())

    return result