#!/usr/bin/python
# -*- coding: utf-8 -*-
#    ******  The Cloud Toolbox v0.1.2******
#    This is the cloud toolbox -- a single module used in several packages
#    found at <https://github.com/cloudformdesign>
#    For more information see <cloudformdesign.com>
#
#    This module may be a part of a python package, and may be out of date.
#    This behavior is intentional, do NOT update it.
#    
#    You are encouraged to use this pacakge, or any code snippets in it, in
#    your own projects. Hopefully they will be helpful to you!
#        
#    This project is Licenced under The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    <https://github.com/cloudformdesign/cloudtb>
#    
#    Permission is hereby granted, free of charge, to any person obtaining a 
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#    DEALINGS IN THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT

from distutils.core import setup
import publish
ctb_packages = ['cloudtb', 'cloudtb.extra', 'cloudtb.extra.PyQt', 
                  'cloudtb.tests', 'cloudtb.external',]

setup(name='cloudtb',
      version=publish.VERSION,
      description='toolbox for cloudformdesign.com',
      author='Garrett Berg',
      author_email='garrett@cloudformdesign.com',
      url='https://github.com/cloudformdesign/cloudtb',
#          modules = ['wordtex', 'wp_formatting', 'texlib'],
      packages = ctb_packages,
      package_dir = {'': '_publish'}
#      packages=['wordtex', 'wordtex.cloudtb'],
     )