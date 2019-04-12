class A():
    def gets(self):
        print('get')
    def ssss(self):
        if hasattr(self,'gets'):
            return self.gets()




a=A()
a.ssss()