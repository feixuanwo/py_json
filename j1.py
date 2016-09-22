#!coding:utf-8
import json
data = [{'a':"A", 'b':(2, 4), 'c':3.0}]
print "DATA:", repr(data)
data_string=json.dumps(data)
print "JSON:", data_string

data_string = json.dumps(data)
print "ENCODED:", data_string

decoded = json.loads(data_string)
print "DECODED:", decoded

print "ORIGINAL:", type(data[0]['b'])
print "DECODED:", type(decoded[0]['b'])


data = [{'a':'A', 'b':(2, 4), 'c':3.0}]
print 'DATA:', repr(data)

unsorted = json.dumps(data)
print 'JSON:', json.dumps(data)
print 'SORT:', json.dumps(data, sort_keys=True)


print 'NORMAL:', json.dumps(data, sort_keys = True)
print 'INDENT:', json.dumps(data, sort_keys = True, indent = 2)

#支持自定义数据类型
class MyObj(object):
    def __init__(self, s):
        self.s = s
    def __repr__(self):
        return '<MyObj(%s)>' % self.s

obj = MyObj('helloworld')

try:
    print json.dumps(obj)
except TypeError, err:
    print 'ERROR:', err

def convert_to_builtin_type(obj):
    print 'default(', repr(obj), ')'
    d = { '__class__':obj.__class__.__name__,
          '__module__':obj.__module__,
        }
    d.update(obj.__dict__)
    return d

print json.dumps(obj, default=convert_to_builtin_type)


#把json decode 成python对象
print 'json to decode'
import json

class MyObj(object):
    def __init__(self,s):
        self.s = s
    def __repr__(self):
        return "<MyObj(%s)>" % self.s

def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')   #移除元素
        print 'CLASS_NAME:', class_name
        module_name = d.pop('__module__')
        print 'MODULE_NAME:', module_name
        module = __import__(module_name)  #导入模块

        print "MODULE:",module

        class_ = getattr(module,class_name)

        print "CLASS",class_

        args = dict((key.encode('ascii'),value) for key,value in d.items())

        print 'INSTANCE ARGS:',args

        inst = class_(**args)
    else:
        inst = d
    return inst

encoded_object = '[{"s":"helloworld","__module__":"j1","__class__":"MyObj"}]'

myobj_instance = json.loads(encoded_object,object_hook=dict_to_object)
print myobj_instance


#使用Encoder与Decoder类实现json编码的转换
#JSONEncoder有一个迭代接口iterencode(data)，返回一系列编码的数据，他的好处是可以方便的把逐个数据写到文件或网络流中，而不需要一次性就把数据读入内存.

encoder = json.JSONEncoder()
data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

for part in encoder.iterencode(data):
    print 'PART:', part


#encode方法等价于''.join(encoder.iterencode()，而且预先会做些错误检查（比如非字符串作为dict的key），
#对于自定义的对象，我们只需重写JSONEncoder的default()方法，其实现方式与上面提及的函数convet_to_builtin_type()是类似的。

#import json_myobj

class MyObj(object):
    def __init__(self,s):
        self.s = s
    def __repr__(self):
        return "<MyObj(%s)>" % self.s

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        print 'default(', repr(obj), ')'
        # Convert objects to a dictionary of their representation
        d = { '__class__':obj.__class__.__name__,
              '__module__':obj.__module__,
              }
        d.update(obj.__dict__)
        return d

#obj = json_myobj.MyObj('helloworld')
obj = MyObj('helloworld')
print obj
print MyEncoder().encode(obj)


print "+++++++++++++++++++++++++++++"
#从json对Python对象的转换:

class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            print 'MODULE:', module
            class_ = getattr(module, class_name)
            print 'CLASS:', class_
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            print 'INSTANCE ARGS:', args
            inst = class_(**args)
        else:
            inst = d
        return inst

encoded_object = '[{"s": "helloworld", "__module__": "j1", "__class__": "MyObj"}]'

myobj_instance = MyDecoder().decode(encoded_object)
print myobj_instance


#json格式字符串写入到文件流中
#上面的例子都是在内存中操作的，如果对于大数据，把他编码到一个类文件(file-like)中更合适，load()和dump()方法就可以实现这样的功能。

import json
import tempfile

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

f = tempfile.NamedTemporaryFile(mode='w+')
json.dump(data, f)
f.flush()

print open(f.name, 'r').read()


import json
import tempfile

f = tempfile.NamedTemporaryFile(mode='w+')
f.write('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
f.flush()
f.seek(0)

print json.load(f)
