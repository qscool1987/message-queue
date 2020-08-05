class LinkNode():
	def __init__(self, data=None):
		self.data = data
		self.next = None
		self.prev = None


class LinkTable():
	def __init__(self):
		self.head = LinkNode()
		self.tail = LinkNode()
		self.head.next = self.tail
		self.tail.prev = self.head
		self._size = 0

	def pushBack(self, data):
		node = LinkNode(data)
		return self.addNodeBack(node)

	def popBack(self):
		if self._size > 0:
			obj = self.tail.prev
			self.tail.prev.prev.next = self.tail
			self.tail.prev = self.tail.prev.prev
			self._size -= 1
			return obj
		return None

	def removeNode(self, node):
		node.prev.next = node.next
		node.next.prev = node.prev
		self._size -= 1

	def addNodeBack(self, node):
		self.tail.prev.next = node
		node.prev = self.tail.prev
		self.tail.prev = node
		node.next = self.tail
		self._size += 1
		return node

	def size(self):
		return self._size

	def begin(self):
		return self.head.next

	def end(self):
		return self.tail

	def popFront(self):
		if self._size > 0:
			obj = self.head.next
			self.head.next.next.prev = self.head
			self.head.next = self.head.next.next
			self._size -= 1
			return obj
		return None

	def pushFront(self, data):
		node = LinkNode(data)
		return self.addNodeFront(node)


	def addNodeFront(self, node):
		node.next = self.head.next
		node.prev = self.head
		self.head.next.prev = node
		self.head.next = node
		self._size += 1
		return node

	def empty(self):
		return self._size == 0

	def toString(self):
		beg = self.begin()
		end = self.end()
		valList = []
		while beg is not end:
			valList.append(str(beg.data))
			beg = beg.next
		line = '\t'.join(valList)
		print (line)
	


if __name__ == '__main__':
	obj = LinkTable()
	end = obj.end()
	for i in range(0,10):
		obj.pushBack(i)
	obj.toString()
	node = end.prev.prev.prev
	obj.removeNode(node)
	beg = obj.begin()
	end = obj.end()
	obj.toString()
	obj.popFront()
	obj.toString()
	obj.popBack()
	obj.toString()
	obj.pushFront(1000)
	obj.toString()
	print (str(obj.size()))
	print (obj.empty())
		
