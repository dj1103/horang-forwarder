# The MIT License
#
# Copyright (c) 2024 Dave Jang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import gzip
import shutil
import os


def get_uncompressed_size(filepath):
    """
        in order to get the correct file size using os.path.getsize

    Args:
        filepath (_str_): _filepath_

    Returns:
        _int_: _file size_
    """
    size = 0
    if not filepath:
        return size
    try:
        with gzip.open(filepath, 'rt') as f_in:
            with open('__temp__file', 'wt') as f_out:
                shutil.copyfileobj(f_in, f_out)
        size = os.path.getsize('__temp__file')
        os.remove('__temp__file')
    except Exception as err:
        size = 0
        print(f'[ERROR] File Size Calculation Error {err}\n')
        exit(1)
    return size