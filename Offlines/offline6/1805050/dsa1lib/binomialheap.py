from dataclasses import dataclass
from math import floor, log
from typing import Generic, TypeVar, Union

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    key: T
    parent: Union["Node[T]", None]
    left_child: Union["Node[T]", None]
    right_sibling: Union["Node[T]", None]
    degree: int


class MaxBinomialHeap(Generic[T]):
    def __init__(self) -> None:
        self.maximum: Node[T] | None = None
        self.left_root: Node[T] | None = None
        self.key_node_map: dict[T, Node[T]] = {}
        self.n = 0

    def insert(self, key: T):
        node = Node[T](key, None, None, None, 0)
        self.key_node_map[key] = node
        self._append_to_rootlist(node)
        self.n += 1
        self._consolidate()

    def increase_key(self, key: T, newkey: T):
        node = self.key_node_map[key]

        if node is None:
            raise KeyError("Provided key does not exist")

        node.key = newkey

        def swim(node: Node[T]):
            while node.parent and node.key > node.parent.key:  # type: ignore
                temp = node.parent.key
                node.parent.key = node.key
                node.key = temp

                self.key_node_map[node.key] = node.parent
                self.key_node_map[node.parent.key] = node

                node = node.parent

        swim(node)

    def extract_max(self) -> T | None:
        if self.maximum:
            self._del_max_from_rootlist()

            maxim = self.maximum
            for child in self._get_children(self.maximum):
                self._append_to_rootlist(child)
            self._consolidate()

            return maxim.key
        else:
            return None

    def find_max(self) -> T | None:
        return self.maximum.key if self.maximum else None

    def __repr__(self) -> str:
        rep = "Printing Binomial Heap...\n"
        rep += "------------------------------------------\n"

        revrootlist = self._get_rootlist()
        revrootlist.reverse()

        for root_node in revrootlist:
            rep += f"\nBinomial Tree, B{root_node.degree}"
            rep += f"\nLevel 0 : {root_node.key}"

            descendents = self._get_children(root_node)
            level = 1
            while descendents:
                rep += f"\nLevel {level} : " + \
                    " ".join([str(node.key) for node in descendents])

                nextgen = []
                for descendent in descendents:
                    nextgen.extend(self._get_children(descendent))

                descendents = nextgen
                level += 1

        rep += "\n------------------------------------------"
        return rep

    def _get_rootlist(self) -> list[Node[T]]:
        rootlist = []
        root_node = self.left_root
        while root_node:
            rootlist.append(root_node)
            root_node = root_node.right_sibling

        return rootlist

    def _get_children(self, node: Node[T]) -> list[Node[T]]:
        children = []
        child = node.left_child
        while child:
            children.append(child)
            child = child.right_sibling
        return children

    def _append_to_rootlist(self, node: Node[T]):
        if self.left_root is None:
            self.left_root = node
            node.parent = None
            node.right_sibling = None
        else:
            node.right_sibling = self.left_root
            node.parent = None
            self.left_root = node

    def _consolidate(self):
        if self.n == 0:
            self.left_root = None
            self.maximum = None
            return
        elif self.n == 1:
            self.maximum = self.left_root
            return
        

        degree_trees: list[Node[T] | None] = [
            None] * (floor(log(self.n, 2)) + 2)

        def make_degree_tree_table():
            node = self.left_root

            for node in self._get_rootlist():
                while degree_trees[node.degree]:
                    tree_with_equal_degree = degree_trees[node.degree]
                    degree_trees[node.degree] = None
                    node = self._link(
                        node, tree_with_equal_degree)

                degree_trees[node.degree] = node

        def add_degree_trees_to_rootlist():
            self.left_root = None
            self.maximum = None

            for node in degree_trees:
                if node is None:
                    continue

                self._append_to_rootlist(node)

                if self.maximum is None:
                    self.maximum = node
                elif node.key > self.maximum.key:  # type: ignore
                    self.maximum = node

        make_degree_tree_table()
        add_degree_trees_to_rootlist()

    def _link(self, tree1, tree2) -> "Node[T]":
        smaller_node, larger_node = tree1, tree2
        if tree2.key < tree1.key:
            smaller_node = tree2
            larger_node = tree1

        smaller_node.parent = larger_node
        smaller_node.right_sibling = larger_node.left_child
        larger_node.left_child = smaller_node
        larger_node.degree += 1

        return larger_node

    def _del_max_from_rootlist(self):
        if self.left_root is None:
            return
        elif self.left_root == self.maximum:
            self.left_root = self.left_root.right_sibling
        else:
            root_node = self.left_root
            while root_node and root_node.right_sibling != self.maximum:
                root_node = root_node.right_sibling

            root_node.right_sibling = self.maximum.right_sibling  # type: ignore

        self.n -= 1


if __name__ == "__main__":
    for i in range(11):
        binomial_heap = MaxBinomialHeap[int]()
        print("***************************************************\n\n")
        with open(f"testcases/in{i}.txt") as file:
            lines = file.readlines()
            for line in lines:
                inputs = line.split()
                operation = inputs[0]
                args = [int(i) for i in inputs[1:]]

                if operation == "I":
                    binomial_heap.insert(-args[0])
                    print("Inserted", args[0])
                elif operation == "P":
                    print(binomial_heap)
                elif operation == "U":
                    for a in args:
                        binomial_heap.insert(-a)
                        print(f"Inserted {a}")
                elif operation == "F":
                    mini = binomial_heap.find_max()
                    if mini:
                        mini = -mini
                    print("FindMin returned", mini)  # type: ignore
                elif operation == "E":
                    mini = binomial_heap.extract_max()
                    if mini:
                        mini = -mini
                    print("ExtractMin returned", mini)  # type: ignore
            
            input()
