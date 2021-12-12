"""
TODO: reverse linked list
"""

class Node():
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)

    __repr__ = __str__


class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, data):
        new_node = Node(data)
        if self.tail and self.head:
            self.tail.next = new_node
        else:
            self.head = new_node

        self.tail = new_node


    def printLL(self):
        current = self.head
        tot = []
        while current:
            tot.append(str(current))
            if current.next:
                current = current.next
            else:
                current = None
        print('LinkedList [{}]'.format(', '.join(tot)))


    def reverse(self):
        previous = None
        current = self.head
        if current:
            following = current.next

        while current:
            current.next = previous
            previous = current
            current = following
            if following:
                following = following.next

        self.head, self.tail = self.tail, self.head



def test1():
    ll = LinkedList()
    ll.insert(11)
    ll.insert(12)
    ll.insert(13)
    ll.insert('so many ways')
    ll.insert(14)
    ll.printLL()
    ll.reverse()
    ll.printLL()

def test2():
    ll = LinkedList()
    ll.printLL()
    ll.reverse()
    ll.printLL()


if __name__ == '__main__':
    test1()
    test2()
