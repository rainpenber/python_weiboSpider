import sys
import codecs
import importlib
importlib.reload(sys)
infofile = codecs.open('result/testfile.txt','a','utf-8')

text = 'expected text'
print(text)
infofile.write(text + '\r\n')