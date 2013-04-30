""" Functions that read snzip files """

import os, io, __builtin__
from struct import unpack as struct_unpack
from snappy import _uncompress as snappy_uncompress

__all__ = ["SnappyJavaFile", "open"]

READ, WRITE = 1, 2
SNAPPY_JAVA_MAGIC = '\x82SNAPPY\x00\x00\x00\x00\x01'

def open(filename, mode="rb"):
    """Shorthand for SnappyJavaFile(filename, mode).

    The filename argument is required; mode defaults to 'rb'

    """
    return SnappyJavaFile(filename, mode)

class SnappyJavaFile(io.BufferedIOBase):
    """ 
    The SnappyJavaFile class simulates few of the methods of a file object.
    """
    myfileobj = None
    max_read_chunk = 10 * 1024 * 1024 # 10Mb

    def __init__(self, filename=None, mode=None, fileobj=None):
        """Constructor for the SnappyJavaFile class.

        At least one of fileobje and filename must be given
        a non-tirvial value.

        The new class instance is based on fileobj, which can be a regular
        file, a StringIO object, or any other object which simulates a file.

        It defaults to None, in which case filename is opened to provide
        a file object.

        """

        if fileobj is None:
            fileobj = self.myfileobj = __builtin__.open(filename, mode or 'rb')

        if filename is None:
            if hasattr(fileobj, 'name') and fileobje.name != '<fdopen>':
                filename = fileobj.name
            else:
                filename = ''
        if mode is None:
            if hasattr(fileobj, 'mode'):
                mode = fileobj.mode
            else:
                mode = 'rb'

        if mode[0:1] == 'r':
            self.mode = READ
            self._new_member = True
            self.extrabuf = ""
            self.extrasize = 0
            self.extrastart = 0
            self.name = filename
            self.min_readsize = 100

        else:
            raise IOError, "mode " + mode + " not supported"

        self.fileobj = fileobj
        self.offset = 0

        
    @property
    def filename(self):
        import warnings
        warnings.warn("use the name attribute", DeprecationWarning, 2)
        return self.name

    def __repr__(self):
        s = repr(self.fileobj)
        return '<snappy ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    def _check_closed(self):
        """Raises a ValueError if the underlying file object has been closed.

        """
        if self.closed:
            raise ValueError('I/O operation on closed file.')

    def _init_read(self):
        self.size = 0

    def _read_exact(self, n):
        data = self.fileobj.read(n)
        while len(data) < n:
            b = self.fileobj.read(n - len(data))
            if not b:
                raise EOFError("Compressed file ended before the "
                               "end-of-stream marker was reached")
            data += b
        return data

    def _read_snappy_java_header(self):
        magic = self.fileobj.read(len(SNAPPY_JAVA_MAGIC))
        if magic != SNAPPY_JAVA_MAGIC:
            raise IOError, 'Not a snappy-java file'

        version = struct_unpack("<H", self._read_exact(2))
        compatible_version = struct_unpack("<H", self._read_exact(2))

    def read(self, size=-1):
        self.check_closed()

        if self.extrasize <= 0 and self.fileobj is None:
            return ''

        self._read()
        
        if len(self.extrabuf) > size:
            tmp_buf = self.extrabuf[0:size]
            self.extrabuf = self.extrabuf[size:]
        else:
            tmp_buf = self.extrabuf
            self.extrabuf = ""
        
        return tmp_buf

    def _read(self, size=1024*30):
        if self._new_member:
            self._read_snappy_java_header()
            self._new_member = False

        raw_chunk_size = self.fileobj.read(4)
        if not raw_chunk_size:
            return False
        chunk_size = struct_unpack(">L", raw_chunk_size)[0]
        chunk = snappy_uncompress(self._read_exact(chunk_size))

        if self.extrabuf:
            self.extrabuf += chunk
        else:
            self.extrabuf = chunk

        return True
        

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        if self.fileobj is None:
            return

        if self.mode == READ:
            self.fileobj = None

        if self.myfileobj:
            self.myfileobj.close()
            self.myfileobj = None
                

    def fileno(self):
        return self.fileobj.fileno()

    def readable(self):
        return self.mode == READ
    
    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        return self.fileobj.seek(offset, whence)

    def tell(self):
        return self.fileobj.tell()

    def readline(self, size=-1):
        while(True):
            i = self.extrabuf.find("\n") + 1
            if i > 0:
                tmp_buf = self.extrabuf[0:i]
                self.extrabuf = self.extrabuf[i:]
                return tmp_buf

            if not self._read():
                return ""

            


        
