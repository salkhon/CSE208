from typing import Generic, TypeVar, Union


T = TypeVar("T")
S = TypeVar("S")


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.root = None
        self.size = 0

    def prepend(self, val: T):
        new_root = LinkedList.Node(val, self.root)
        self.root = new_root
        self.size += 1

    def _find_first_node_with_val(self, val: T) -> Union["LinkedList.Node", None]:
        current_node = self.root

        while current_node and current_node.val != val:
            current_node = current_node.next

        return current_node

    def delete(self, val: T):
        pass

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> "LLIter[T]":
        return LinkedList.LLIter[T](self)

    class LLIter(Generic[S]):
        def __init__(self, linkedlist: "LinkedList") -> None:
            self.linkedlist = linkedlist
            self.current_idx = 0

        def __next__(self) -> S:
            current_node = self.linkedlist.root

            idx = 0
            while current_node and idx != self.current_idx:
                idx += 1
                current_node = current_node.next

            self.current_idx += 1

            if current_node is None:
                raise StopIteration

            return current_node.val

    class Node:
        def __init__(self, val, next=None) -> None:
            self.val = val
            self.next = next


if __name__ == "__main__":
    linkedlist = LinkedList[int]()
    linkedlist.prepend(1)
    linkedlist.prepend(2)
    linkedlist.prepend(3)
    linkedlist.prepend(4)

    for val in linkedlist:
        print(val)