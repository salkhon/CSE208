from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, cast, no_type_check


class BalancedBST(ABC):
    def __init__(self):
        self.root = None
        self.num_keys = 0

    @abstractmethod
    def insert(self, key: int):
        pass

    @abstractmethod
    def delete(self, key: int):
        pass

    @abstractmethod
    def find(self, key: int) -> bool:
        return False

    @dataclass
    class Node:
        key: int


class AVLTree(BalancedBST):
    def __init__(self):
        super().__init__()
        self._is_height_invar_violated = False

    def insert(self, key: int):
        self._is_height_invar_violated = False

        def insert_helper(node: Optional["AVLTree.Node"]) -> "AVLTree.Node":
            if not node:
                return AVLTree.Node(key, 0, None, None)

            if key > node.key:
                node.right_child = insert_helper(node.right_child)
            elif key < node.key:
                node.left_child = insert_helper(node.left_child)

            if abs(self.height_of(node.left_child) - self.height_of(node.right_child)) > 1:
                node = self.fix_height_imbalance(node)

                if not self._is_height_invar_violated:
                    print("Height invariant violated")
                    self._is_height_invar_violated = True

            node.height = max(self.height_of(node.left_child),
                              self.height_of(node.right_child)) + 1

            return node

        self.root = insert_helper(self.root)

        self.num_keys += 1

        if self._is_height_invar_violated:
            print("After rebalancing: ", end="")
        print(self)

    def fix_height_imbalance(self, node: "Node") -> "Node":
        if abs(self.height_of(node.left_child) - self.height_of(node.right_child)) <= 1:
            # no height imbalance
            raise ValueError("Node is not imbalanced")

        if self.height_of(node.left_child) > self.height_of(node.right_child):
            # doubly left heavy
            heavy_child = node.left_child
            assert heavy_child

            if self.height_of(heavy_child.left_child) >= self.height_of(heavy_child.right_child):
                # left zig zig imbalance
                node = self.right_rotate(node)
            else:
                # left zig zag imbalance
                node.left_child = self.left_rotate(heavy_child)
                node = self.right_rotate(node)
        else:
            # doubly right heavy
            heavy_child = node.right_child
            assert heavy_child

            if self.height_of(heavy_child.right_child) >= self.height_of(heavy_child.left_child):
                # right zig zig imbalance
                node = self.left_rotate(node)
            else:
                # right zig zag imbalance
                node.right_child = self.right_rotate(heavy_child)
                node = self.left_rotate(node)

        return node

    def get_minimum_child_node_from_subroot(self, subroot: Optional["Node"]) -> Optional["Node"]:
        if not subroot:
            return None

        minimum = subroot
        while minimum.left_child:
            minimum = minimum.left_child

        return minimum

    def _delete_min_from_subroot(self, subroot: "Node") -> Optional["Node"]:

        def del_min_helper(node: "AVLTree.Node") -> Optional["AVLTree.Node"]:
            if not node.left_child:
                return node.right_child

            node.left_child = del_min_helper(node.left_child)

            if abs(self.height_of(node.left_child) - self.height_of(node.right_child)) > 1:
                node = self.fix_height_imbalance(node)

                if not self._is_height_invar_violated:
                    print("Height invariant violated")
                    self._is_height_invar_violated = True

            node.height = max(self.height_of(node.left_child),
                              self.height_of(node.right_child)) + 1

            return node

        return del_min_helper(subroot)

    def delete(self, key: int):
        if not self.find(key):
            return

        self._is_height_invar_violated = False

        def del_helper(node: Optional["AVLTree.Node"]) -> Optional["AVLTree.Node"]:
            assert node

            if key < node.key:
                node.left_child = del_helper(node.left_child)
            elif key > node.key:
                node.right_child = del_helper(node.right_child)
            else:
                if not node.right_child:
                    node = node.left_child
                else:
                    minimum_right = self.get_minimum_child_node_from_subroot(
                        node.right_child)
                    assert minimum_right
                    node.right_child = self._delete_min_from_subroot(
                        node.right_child)
                    node.key = minimum_right.key

            if node and abs(self.height_of(node.left_child) - self.height_of(node.right_child)) > 1:
                node = self.fix_height_imbalance(node)

                if not self._is_height_invar_violated:
                    print("Height invariant violated")
                    self._is_height_invar_violated = True

            if node:
                node.height = max(self.height_of(node.left_child),
                                  self.height_of(node.right_child)) + 1

            return node

        self.root = del_helper(self.root)
        self.num_keys -= 1

        if self._is_height_invar_violated:
            print("After rebalancing: ", end="")
        print(self)

    def find(self, key: int) -> bool:
        current_node = cast(AVLTree.Node, self.root)

        is_found = False
        while current_node:
            if key < current_node.key:
                current_node = current_node.left_child
            elif key > current_node.key:
                current_node = current_node.right_child
            else:
                is_found = True
                break

        return is_found

    def left_rotate(self, node: "Node") -> "Node":
        right_child = node.right_child

        if not right_child:
            raise RuntimeError("Can't left rotate with no right child")

        node.right_child = right_child.left_child
        right_child.left_child = node
        node.height -= 1
        right_child.height += 1

        return right_child

    def right_rotate(self, node: "Node") -> "Node":
        left_child = node.left_child

        if not left_child:
            raise RuntimeError("Can't right rotate with no left child")

        node.left_child = left_child.right_child
        left_child.right_child = node

        node.height -= 1
        left_child.height += 1

        return left_child

    def __repr__(self) -> str:

        def get_parenthesized_str(node: Optional["AVLTree.Node"]) -> str:
            if not node:
                return ""

            paren_str = f"{node.key}"

            if node.left_child or node.right_child:
                paren_str += f"({get_parenthesized_str(node.left_child)})({get_parenthesized_str(node.right_child)})"

            return paren_str

        return get_parenthesized_str(self.root)

    def height_of(self, node: Optional["Node"]) -> int:
        return node.height if node else -1

    @dataclass
    class Node(BalancedBST.Node):
        height: int
        left_child: Optional["AVLTree.Node"]
        right_child: Optional["AVLTree.Node"]
        # not keeping parent pointer, so rotations need to return parent link for the caller


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
        avltree = AVLTree()
        for line in lines:
            op, input = line.split()

            if op == "F":
                print(avltree.find(int(input)))
            elif op == "I":
                avltree.insert(int(input))
            elif op == "D":
                avltree.delete(int(input))
