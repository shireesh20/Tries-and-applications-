class FileCompression:
	
	def __init__(self):
		self.root=None
		self.codes={}
		self.get_ch={}

	#sending the counter into insert function and forming the trie
	def insert(self,c):
		l=[]

		#storing all the leaf nodes in a list
		for (k,v) in c:
			n=Node()
			n.weight=v
			n.key=k
			l.append(n)

		#using min heap to get the desired code for a character	
		H=BinaryHeap(l)
		H.BuildHeap()
		

		#creating the required trie		
		for i in range(1,len(H.E)-1):
			mn=Node()
			mn.right=H.extractMin()
			mn.left=H.extractMin()
			mn.weight=mn.right.weight+mn.left.weight
			H.insert(mn)
		self.root=mn   #assigning the top most node to the root

	#this function is used to obtain the codes
	def codeformation(self,p,str1):
		if p==None:
			return
		if p.key!=None:
			self.codes[p.key]=str1
			self.get_ch[str1]=p.key
		self.codeformation(p.left,str1+'0')
		self.codeformation(p.right,str1+'1')

	#this function is used to encode the given text using the codes formed	
	def get_encodedData(self,text):
		encoded_text=""
		for ch in text:
			encoded_text+=self.codes[ch]
		return encoded_text

	#this function fills the extra bits required
	def get_padded_text(self,encoded_text):
		padded_text=encoded_text
		extra=8-len(encoded_text)%8
		for i in range(extra):
			padded_text+='0'
		pad_info="{0:08b}".format(extra)
		padded_text=pad_info+padded_text
		return padded_text

	#this function generates the bytes to be written 
	def get_ByteArray(self,text):
		if ((len(text)%8)!=0):
			print("some error in padding ,try again")
			exit(0)
		b=bytearray()
		for i in range(0,len(text),8):
			byte=text[i:i+8]
			b.append(int(byte,2))
		return b

	#this is the actual funtion that performs the compression
	def compress(self,f1):
		from collections import Counter
		outfile=f1[:-4]+'.bin'
		with open(f1,'r') as f ,open(outfile,'wb') as comp:
			data=f.read()
			data=data.rstrip()
			c = Counter(data)
			c=list(c.most_common())
			self.insert(c)
			self.codeformation(self.root,'')
			encoded_text=self.get_encodedData(data)
			padded_text=self.get_padded_text(encoded_text)
			b=self.get_ByteArray(padded_text)
			comp.write(bytes(b))
		print()
		print("file   ***",f1,"***   is compressed and stored in   ***",outfile,"***  ")
		print()

	#this function performs the decompression of the previous file compressed
	def decompress(self,f):
		outfile=f[:-4]+'_decomp.txt'
		with open(f,'rb') as f1 ,open(outfile,'w') as decomp:
			bit_string=""
			byte=f1.read(1)
			while(byte):
				byte=ord(byte)
				bit_string+=bin(byte)[2:].rjust(8,'0')
				byte=f1.read(1)
			encoded_text=self.rem_padding(bit_string)
			text=self.decode(encoded_text)
			decomp.write(text)
		print()
		print("file   ***",f,"***   is decompressed and stored as   ***",outfile,"***  ")
		print()

	#this function removes the padding done previously
	def rem_padding(self,bit_string):
		pad_info=bit_string[0:8]
		extra_pad=int(pad_info,2)
		encoded_text=bit_string[8:]
		encoded_text=encoded_text[:-1*extra_pad]
		return encoded_text

	#this function decodes using the codes obtained above 
	def decode(self,encoded_text):
		ch_code=''
		decoded_text=''
		for bit in encoded_text:
			ch_code+=bit
			if(ch_code in self.get_ch):
				decoded_text+=self.get_ch[ch_code]
				ch_code=''
		return decoded_text


class Node:		#the trienode we use
	def __init__(self):
		self.weight=None
		self.left=None
		self.right=None
		self.key=None

class BinaryHeap:		#this is used to obtain the desired codes
	def __init__(self,L):
		self.E=[None]+L
		self.l=len(self.E)
		self.BuildHeap()

	def heapify(self,i):
		if (i<=(self.l-1)/2) and (i>0):
			if(2*i+1<self.l):
				t2=self.E[2*i+1].weight
			t1=self.E[2*i].weight
			if (2*i+1<self.l) and (self.E[i].weight>t2) and (t1>t2):
				t=self.E[2*i+1]
				self.E[2*i+1]=self.E[i]
				self.E[i]=t
				k=i*2+1
			elif(self.E[i].weight>t1):
				t=self.E[2*i]
				self.E[2*i]=self.E[i]
				self.E[i]=t
				k=2*i
			else:
				k=-1
			self.heapify(k)


	def BuildHeap(self):
		for i in range(int((self.l-1)/2),0,-1):
			self.heapify(i)


	def extractMin(self):
		t=self.E[1]
		self.E[1]=self.E[self.l-1]
		self.E[self.l-1]=t
		t=self.E[self.l-1]
		del self.E[self.l-1]
		self.l-=1
		self.heapify(1)
		return t

	def insert(self,k):
		self.l+=1
		self.E.append(k)
		i=int((self.l-1)/2)
		while i>0:
			self.heapify(i)
			i=int(i/2)


def main():
	f1=input("enter the file_name (path):")
	FC=FileCompression()
	FC.compress(f1)
	FC.decompress(f1[:-3]+'bin')

if __name__ == '__main__':
	main()