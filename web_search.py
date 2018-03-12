from shutil import move
from os import remove
class Trie:
    def __init__(self):
        self.root=TrieNode()
        self.H=BinaryMaxHeap()

    def Index(self,ch):
        if ch in ['0','1','2','3','4','5','6','7','8','9']:
            return int(ch)+36
        if ch=='.':
            return 26
        if ch==':':
            return 27
        if ch=='/':
            return 28
        if ch=='\\':
            return 29
        if ch=='-':
            return 30
        if ch=='_':
            return 31
        if ch=='>':
            return 32
        if ch==';':
            return 33
        if ch=='=':
            return 34
        if ch=='@':
            return 35      
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
        k=t
        s=''
        while(k.par):
            s=s+k.ch
            k=k.par
        s=s[::-1]
        t.pri=int(s[len(s)-1])
        t.webpage=s

    def search(self,key):
        t=self.root
        l=len(key)
        for c in key:
            i=self.Index(c)
            if not t.children[i]:
                return False
            t=t.children[i]
        if t!=None and t.isEnd:
            return t
        else:
            return False

    def inserturl(self,url):
        f= open("browse.txt","a+")
        f.write(url+"\n")
        f.close()

    def webautocomplete(self,key):
        t=self.root
        L=[]
        for c in key:
            i=self.Index(c)
            if not t.children[i]:
                print('Sorry no such results from your browser history !! ')
                print()
                self.addnew()
                return 
            t=t.children[i]
        if t.isEnd:
            L.append(t)
        self.getWords(t,L)
        print('Results from browser history : ')
        print()
        for i in L:
            self.H.insert(i)
        for i in range(1,len(self.H.E)):
            t=self.H.extractMax()
            L[i-1]=t
            print("\t"+str(i)+"."+t.webpage[:-2])
            print()
        print()
        print("Did you find the desired link (1/0) ? ",end='')
        ch=int(input())
        if ch==0:
            print("\033c")
            self.addnew()
            return
        elif ch==1:
            print()
            print('Select a webpage from the list : ',end='')
            ch=int(input())
            print()
            while ch>len(L) or ch<1:
                print("Invalid entry ! Please try again (0 to exit) : ",end='')
                ch=int(input())
                print()
            if ch==0:
                return
            st=L[ch-1].webpage
            L[ch-1].pri+=1
            with open('browse.txt','r') as actual, open('update.txt','w') as dup:
                for line in actual:
                    dup.write(line.replace(st,st[:-1]+str(L[ch-1].pri)))
            remove('browse.txt')
            move('update.txt','browse.txt')
            self.openurl(L,ch-1)
        else:
            print("invalid choice!!!!")
            print("bye bye!!")

    def openurl(self,L,k):
        import webbrowser
        new = 2
        url = 'http://' + L[k].webpage[:-2]
        webbrowser.open(url,new=new)   

    def getWords(self, t, L):
        for i in range(45):
            if t.children[i]:
                if t.children[i].isEnd:
                    L.append(t.children[i])
                self.getWords(t.children[i], L)
        return

    def addnew(self):
        print("Enter the desired link to open it now : ",end='')
        u=input()
        with open('browse.txt','a+') as f:
            f.write(u+'|1\n')
        import webbrowser
        new = 2
        url = 'http://' + u
        webbrowser.open(url,new=new)

    def getCount(self):
        with open('browse.txt','r') as f:
            for line in f:
                print("\t"+line[:-3]+" - "+line[len(line)-2])
                print()

    def remlink(self):
        flag=0
        s=input("Enter the link to remove : ")
        print()
        with open('browse.txt','r') as actual, open('update.txt','w') as dup:
            for line in actual:
                if line[:-3]==s:
                    flag=1
                    continue
                else:
                    dup.write(line)
        remove('browse.txt')
        move('update.txt','browse.txt')
        if not flag :
            print('Sorry,no such link found in your history !! ')
            print()
        else:
            print()
            print('Link removed sucessfully')
        print()

class BinaryMaxHeap:
    def __init__(self):
        self.E=[]
        self.E.append(-999)
        self.l=len(self.E)
    
    def heapify(self,i):
        if (i<=(self.l-1)/2) and (i>0):
            if(2*i+1<self.l):
                t2=self.E[2*i+1].pri
            t1=self.E[2*i].pri
            if (2*i+1<self.l) and (self.E[i].pri<t2) and (t1<t2):
                t=self.E[2*i+1]
                self.E[2*i+1]=self.E[i]
                self.E[i]=t
                k=i*2+1
            elif(self.E[i].pri<t1):
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

    def extractMax(self):
        t=self.E[1]
        self.E[1]=self.E[self.l-1]
        self.E[self.l-1]=t
        t=self.E[self.l-1]
        del self.E[self.l-1]
        self.l-=1
        self.heapify(1)
        return t

    def maximum(self):
        return self.E[1]

    def insert(self,k):
        self.l+=1
        self.E.append(k)
        i=int((self.l-1)/2)
        while i>0:
            self.heapify(i)
            i=int(i/2)

    def isEmpty(self):
        if len(self.E)==1:
            return True
        return False

class TrieNode:
    def __init__(self):
        self.children=[None]*45
        self.isEnd=False
        self.webpage=''
        self.par=None
        self.ch=''
        self.pri=-1

def main():
    print("\033c")
    T=Trie()
    f = open('browse.txt', "r")
    lines = f.readlines()
    for i in range(len(lines)):
        st=lines[i][:-1]
        T.insert(st)
    f.close()
    print('\t\t\t\t _________________________________________________________________')
    print('\t\t\t\t|                                                                 |')
    print('\t\t\t\t|                  SIMPLE      URL    SEARCH                      |')
    print('\t\t\t\t|_________________________________________________________________|')
    print()
    print()
    print()
    print('Enter prefix to complete your web search : ',end='')
    url=input()
    print("\033c")
    T.webautocomplete(url)
    print("\033c")
    ch=int(input('would you like to check your history count (1/0) : '))
    print()
    if ch:
        T.getCount()
        c=int(input('would you like to remove any link (1/0) : '))
        if c:
            print()
            T.remlink()
        else:
            print("\033c")
    else:
        print("\033c")

if __name__ == '__main__':
    main() 