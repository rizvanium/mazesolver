class UnionFind:
    def __init__(self, size):

        if size <= 0:
            print("size must be gt zero")
            return

        self.component_count = size
        self.size = size
        self.ids = []
        self.sizes = []

        for i in range(size):
            self.ids.append(i)
            self.sizes.append(1)


    def find(self, p: int) -> int:
        '''return a set to whom the element 'p' belongs to'''
        root = p
        while root != self.ids[p]:
            root = self.ids[root]
        
        # kelio apkirpimas
        while p != root:
            next = self.ids[p]
            self.ids[p] = root
            p = next

        return root

    def check_if_connected(self, p: int, q: int) -> bool:
        '''returns whether or not elements belong to the same set'''
        return self.find(p) == self.find(q)

    def get_set_size(self, p: int) -> int:
        '''returns the size of the component to whom the element p belongs'''
        return self.sizes[self.find(p)]

    def unify(self, p, q) -> None:
        '''combines two sets to whom elements p and q belong'''
        root1 = self.find(p)
        root2 = self.find(q)

        if root1 == root2:
            return

        if self.sizes[root1] < self.sizes[root2]:
            self.sizes[root2] += self.sizes[root1]
            self.ids[root1] = root2
        else:
            self.sizes[root1] += self.sizes[root2]
            self.ids[root2] = root1

        self.component_count -= 1
