class Keyboard:

    def __init__(self):
        self.shift = False
        self.control = False
        self.backspace = False
        self.backspaceTick = -1

        self.keys = {'a':'a', 'b':'b', 'c':'c', 'd':'d', 'e':'e', 'f':'f', 'g':'g', 'h':'h', 'i':'i', 'j':'j', \
                     'k':'k', 'l':'l', 'm':'m', 'n':'n', 'o':'o', 'p':'p', 'q':'q', 'r':'r', 's':'s', 't':'t', \
                     'u':'u', 'v':'v', 'w':'w', 'x':'x', 'y':'y', 'z':'z', '0':'0', '1':'1', '2':'2', '3':'3', \
                     '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '-':'-', '=':'=', ';':';', "'":"'", \
                     '.':'.', ',':',', '/':'/', 'space':' '}

        self.shiftKeys = {'a':'A', 'b':'B', 'c':'C', 'd':'D', 'e':'E', 'f':'F', 'g':'G', 'h':'H', 'i':'I', 'j':'J', \
                          'k':'K', 'l':'L', 'm':'M', 'n':'N', 'o':'O', 'p':'P', 'q':'Q', 'r':'R', 's':'S', 't':'T', \
                          'u':'U', 'v':'V', 'w':'W', 'x':'X', 'y':'Y', 'z':'Z', '0':')', '1':'!', '2':'@', '3':'#', \
                          '4':'$', '5':'%', '6':'^', '7':'&', '8':'*', '9':'(', '-':'_', '=':'+', ';':':', "'":'"', \
                          '.':'>', ',':'<', '/':'?', 'space':' '}

    def update(self):
        if self.backspace:
            self.backspaceTick += 1
            if self.backspaceTick >= 4:
                self.backspaceTick = -1
