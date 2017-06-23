import sys
import struct as st
import ctypes

if st == sys.modules[__name__]:
    del sys.modules['struct']
    st = __import__('struct')


qword = lambda d, off=0: st.unpack_from('<Q',d,off)[0]
dword = lambda d, off=0: st.unpack_from('<I',d,off)[0]
word  = lambda d, off=0: st.unpack_from('<H',d,off)[0]
byte  = lambda d ,off=0: st.unpack_from('<B',d,off)[0]

class Structure(ctypes.Structure):

    _blacklist_ = []

    @classmethod
    def parse(self,data):
        return self.from_buffer_copy(data)
    
    def as_dict(self):
        ret = {}
        for field, _ in self._fields_:
            if field in self._blacklist_:
                continue
            
            value = getattr(self, field)
            if isinstance(value, Structure):
                ret[field] = value.as_dict()
            elif hasattr(value, "value"):
                ret[field] = value.value
            elif hasattr(value, "__getitem__"):
                ret[field] = value[:]
            else:
                ret[field] = value
        return ret
