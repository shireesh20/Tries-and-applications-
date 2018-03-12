class Trie:
	def __init__(self):
		self.root=TrieNode()

	def Index(self,ch):
		return ord(ch)-ord('a')

	def insert(self,key):
		t=self.root
		l=len(key)
		for c in key:
			i=self.Index(c)
			if not t.children[i]:
				t.children[i]=TrieNode()
				t.children[i].par=t
				t.children[i].ch=c
			t=t.children[i]
		t.isEnd=True

	def search(self,key):
		t=self.root
		l=len(key)
		for c in key:
			i=self.Index(c)
			if not t.children[i]:
				return False
			t=t.children[i]
		if t!=None and t.isEnd:
			return True
		else:
			return False

	def deleteHelper(self,temp,key,index,l):
		t=temp
		if not t:
			return False
		if (index==l):
			if t.isEnd:
				t.isEnd=False
			return self.isFree(t)
		else:
			i=self.Index(key[index])
			if self.deleteHelper(t.children[i],key,index+1,l):
				del t.children[i]
				return (not t.isEnd) and self.isFree(t)

	def delete(self,key):
		t=self.search(key)
		l=len(key)
		if key:
			self.deleteHelper(self.root,key,0,l)

	def isFree(self,node):
		if not node:
			return False
		for i in node.children:
			if i:
				return False
		return True

	def autocomplete(self,key):
		t=self.root
		L=[]
		for c in key:
			i=self.Index(c)
			if not t.children[i]:
				return
			t=t.children[i]
		if t.isEnd:
			k=t
			s=''
			while(k.par):
				s=s+k.ch
				k=k.par
			s=s[::-1]
			L.append(s)
		self.getWords(t,L)
		for s in L:
			print(s)
		print()

	def getWords(self,t,L):
		for i in range(26):
			if t.children[i]:
				if t.children[i].isEnd:
					s=''
					k=t.children[i]
					while(k.par):
						s=s+k.ch
						k=k.par
					s=s[::-1]
					L.append(s)
				self.getWords(t.children[i],L)
		return

class TrieNode:
	def __init__(self):
		self.children=[None]*26
		self.isEnd=False
		self.par=None
		self.ch=''

def main():
	T=Trie()
	with open('mini.dict','r') as f:
		S=[]
		for line in f:
			S.append(line.strip())
	for i in range(len(S)):
		T.insert(S[i])
	s=input("enter the key to search:")
	print(T.search(s))
	a=input("enter some prefix to find those words:")
	T.autocomplete(a)


if __name__ == '__main__':
	main()