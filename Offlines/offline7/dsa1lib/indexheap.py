import random
from typing import Any


class IndexedMinPQ:
    """Stores keys identified by indices. Rather than storing the keys in the heap, we store
    the index, which allows the client to decrease keys based on the provided index.  
    """

    def __init__(self, max_len: int):
        self.max_len = max_len
        self.index_to_key: list = [None] * self.max_len
        self.index_to_heapidx: list[int] = [0] * self.max_len
        # index 0 unused, heaps contain lookup_idx
        self.heap: list[int] = [-1] * (self.max_len + 1)
        self.heap_tail_idx = 1  # heapidx to be inserted next

    def _swim(self, heap_idx: int):
        i = heap_idx
        while i > 1 and self._key_at_heapidx(i) < self._key_at_heapidx(i // 2):
            self._exchange_keys(i, i // 2)
            i //= 2

    def _sink(self, heap_idx: int):
        i = heap_idx
        while 2 * i < self.heap_tail_idx:
            min_child_idx = 2 * i
            if 2 * i + 1 < self.heap_tail_idx and self.index_to_key[self.heap[2 * i + 1]] < self.index_to_key[self.heap[2 * i]]:
                min_child_idx = 2 * i + 1

            if self.index_to_key[self.heap[min_child_idx]] < self.index_to_key[self.heap[i]]:
                self._exchange_keys(i, min_child_idx)

            i = min_child_idx

    def _key_at_heapidx(self, heapidx: int):
        return self.index_to_key[self.heap[heapidx]]

    def _exchange_keys(self, heap_idx1: int, heap_idx2: int):
        index1, index2 = self.heap[heap_idx1], self.heap[heap_idx2]

        self.heap[heap_idx1], self.heap[heap_idx2] = index2, index1

        self.index_to_heapidx[index1], self.index_to_heapidx[index2] = heap_idx2, heap_idx1

    def insert(self, index: int, key):
        if self.heap_tail_idx > self.max_len:
            raise IndexError("Heap full")

        if self.index_to_key[index]:
            raise KeyError("Value at provided index already exists")

        self.index_to_key[index] = key
        self.index_to_heapidx[index] = self.heap_tail_idx
        self.heap[self.heap_tail_idx] = index

        self.heap_tail_idx += 1
        self._swim(self.heap_tail_idx - 1)

    def key_of_index(self, index: int):
        return self.index_to_key[index]

    def min(self):
        return self.heap[1]

    def del_min(self) -> tuple:
        return self._del_key_at_heapidx(1)

    def decrease_key(self, index: int, key) -> None | ValueError:
        if self.index_to_key[index] < key:
            raise ValueError("Keys can only decrease")

        self.index_to_key[index] = key
        self._swim(self.index_to_heapidx[index])

    def del_key(self, index: int) -> tuple | IndexError:
        if index >= self.max_len:
            return IndexError("Out of bounds")

        return self._del_key_at_heapidx(self.index_to_heapidx[index])

    def __len__(self):
        return self.heap_tail_idx - 1

    def _del_key_at_heapidx(self, heap_idx: int) -> tuple[int, Any]:
        self.heap_tail_idx -= 1  # tail was at the position to be inserted next
        self._exchange_keys(heap_idx, self.heap_tail_idx)

        index_to_delete = self.heap[self.heap_tail_idx]
        deleted_key = self.index_to_key[index_to_delete]
        self.index_to_key[index_to_delete] = None

        self._sink(heap_idx)

        return index_to_delete, deleted_key

    def __repr__(self):
        return f"\nindex_to_key: {[(i, val) for i, val in enumerate(self.index_to_key)]}\
            \nheap: {[(i, val) for i, val in enumerate(self.heap)]}\
            \nindex_to_heapidx: {[(i, val) for i, val in enumerate(self.index_to_heapidx)]}"


if __name__ == "__main__":
    ipq = IndexedMinPQ(10)

    print("---------------------------------")

    ipq.insert(0, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(4, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(5, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(8, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(7, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(9, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(1, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(3, random.random())
    print(ipq)

    print("---------------------------------")

    ipq.insert(2, random.random())
    print(ipq)

    print("INSERTION COMPLETE---------------------------------")

    print([(i, index, ipq.index_to_key[index])
          for i, index in enumerate(ipq.heap) 
          if index != -1])  # -1 index means heap does not contain anything at that heapidx

    print("----------------------------------------------")

    print("Heap order")

    order = []
    while len(ipq):
        order.append(ipq.del_min())
    
    print(order)

    for i, key in enumerate(order):
        if i < len(order) - 1 and key > order[i+1]:
            break
    else:
        print("Order maintained")
