class UnionFind:
    def __init__(self, N: int):
        """Union find data structure with N vertices. 

        Args:
            N (int): Number of vertices
        """
        self.parent_link = [i for i in range(N)]
        self.size_rooted_at = [1] * N
        self.N = N

    def _find_root(self, v: int) -> int:
        r = v
        while self.parent_link[r] != r:
            r = self.parent_link[r]

        # path compression
        u = v
        while self.parent_link[u] != u:
            old_parent = self.parent_link[u]
            self.parent_link[u] = r
            u = old_parent

        return r

    def union(self, v1: int, v2: int):
        """Puts v1 and v2 in the same set. 

        Args:
            v1 (int): Vertex 1
            v2 (int): Vertex 2
        """
        if v1 < 0 or v2 < 0 or v1 >= self.N or v2 >= self.N:
            raise ValueError("Vertex out of bounds")

        r1 = self._find_root(v1)
        r2 = self._find_root(v2)

        if self.size_rooted_at[r2] > self.size_rooted_at[r1]:
            self.parent_link[r1] = r2
        else:
            self.parent_link[r2] = r1

    def in_same_set(self, v1: int, v2: int) -> bool:
        if v1 < 0 or v2 < 0 or v1 >= self.N or v2 >= self.N:
            raise ValueError("Vertex out of bounds")

        return self._find_root(v1) == self._find_root(v2)
