"""
TODO: invert binary tree
"""


class Node():
    def __init__(self, data, left = None, right = None):
        if left:
            self.__left = left if isinstance(left, Node) else Node(left)
        else:
            self.__left = None
        if right:
            self.__right = right if isinstance(right, Node) else Node(right)
        else:
            self.__right = None
        self.__data = data


    def __str__(self):
        return 'Node: {}'.format(str(self.__data))
    __repr__ = __str__


    def printTree(self, level=0):
        hang = '  ' * level
        print("{0}{1}".format(hang, self.__data))
        if self.__left:
            self.__left.printTree(level=level+1)
        if self.__right:
            self.__right.printTree(level=level+1)


    def left(self, *args):
        """
        set | get left
        """
        if len(args) > 0:
            if isinstance(args[0], Node):
                self.__left = args[0]
            else:
                self.__left = Node(args[0])
        else:
            return self.__left


    def right(self, *args):
        """
        set | get right
        """
        if len(args) > 0:
            if isinstance(args[0], Node):
                self.__right = args[0]
            else:
                self.__right = Node(args[0])
        else:
            return self.__left


    def invert(self, root = None):
        if root == None:
            root = self
        stack = [root]

        while stack:
            node = stack.pop()
            node.__left, node.__right = node.__right, node.__left
            if node.__left:
                stack.append(node.__left)
            if node.__right:
                stack.append(node.__right)

        return root

class Node2(Node):
    pass


def test1():
    print('-----')
    n1 = Node2(11)
    n2 = Node(22)
    n3 = Node(23)
    n4 = Node(24)
    n5 = Node(25)
    n1.left(n2)
    n1.right(n3)
    n2.left(n4)
    n2.right(n5)
    n1.printTree()
    # n1.invert(n1)
    print('inverted:')
    n1.invert()
    n1.printTree()


def test2():
    print('-----')
    n1 = Node('1')
    n1.printTree()
    print('inverted:')
    n1.invert()
    n1.printTree()


def test3():
    print('-----')
    n1 = Node2(1)
    n1.printTree()
    Node.invert(n1)
    print('inverted:')
    n1.printTree()

def test4():
    print('-----')
    n1 = Node2(1, Node2(2, Node2(3), Node2(4)), Node2(5, 6, 7))
    n1.printTree()
    Node.invert(n1)
    print('inverted:')
    n1.printTree()


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
