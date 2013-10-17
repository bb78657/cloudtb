#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#    http://opensource.org/licenses/MIT
# -*- coding: utf-8 -*-

import pdb
import sys, os
import itertools
import re
import commands

from guitools import get_color_from_index, get_color_str

from richtext import (HEADER, FOOTER, html_span_std, get_html_span_tags, 
                      text_format_html, HtmlPart)

try:
    from .. import iteration, textools
except ValueError:
    try:
        import iteration, textools
    except ImportError:
        import sys
        sys.path.insert(1, '..')
        import iteration, textools

def re_search_format_html(data_list, show_tags_on_replace = False):
    html_list = [HtmlPart(HEADER, '', '')]

    for data in data_list:
        if type(data) == str:
            text_html = text_format_html(data, html_span_std)
            for tp in text_html:
                tp.regpart = None
            html_list.extend(text_html)
        else:
            regpart_html = _regpart_format_html(data,
                show_tags_on_replace = show_tags_on_replace)
            html_list.extend(regpart_html)
    html_list.append(HtmlPart(FOOTER, '', ''))
    html_list = tuple(n for n in html_list if bool(n))
    return html_list

def _reduce_match_paths(folder_path,
                        file_regexp, text_regexp,
                        recurse,
                        max_len_searched):
    '''Uses standard operating system tools to reduce the number of files
    we need to search as much as possible'''
    # first we are going to break the file_regexp up into text parts 
    

IGNORE = '.git, '
def get_match_paths(folder_path, 
                    file_regexp = None, text_regexp = None, 
                    recurse = True, 
                    max_len_searched = None,
                    watchers = None,
                    ignore = None):
    '''
    get the file paths in a folder that have text which matches
    the regular expression. Returns [(full_file_path, iter(re_searched_data), 
        incomplete_matches), ...]
    To actually get the data and matches, convert to tuple.
    
    Watchers should be a list of watchers to be called on each new file name
    '''
    if ignore == None: ignore = IGNORE
    if (file_regexp, text_regexp) == (None, None):
        raise ValueError('Must specify at least one regex!')
    if file_regexp != None:
        if type(file_regexp) in (str, unicode):
            file_regexp = re.compile(file_regexp)
        file_fnd = file_regexp.finditer
    if text_regexp != None:
        if type(text_regexp) in (str, unicode):
            text_regexp = re.compile(text_regexp)
        text_fnd = text_regexp.finditer
    
    folder_path = os.path.abspath(folder_path)
    fpaths = []
    for fname in os.listdir(folder_path):
        if fname in ignore: continue
        path = os.path.join(folder_path, fname)
        del fname
        if watchers:
            [w(path) for w in watchers]

        if os.path.isdir(path):
            fpaths.extend(get_match_paths(path,
                file_regexp, text_regexp, recurse, 
                max_len_searched))

        if file_regexp:
            try:
                # find any match to file name
                next(file_fnd(path))
            except StopIteration:
                continue
        
        if text_regexp:
            with open(path) as f:
                # Ok, what I think I am going to do is break up the regexp
                    # and then grep the result.
                #TODO: check if file is a text file
                text = f.read()
                try:
                    # find any match to text name
                    next(text_fnd(text, 0, max_len_searched))
                except StopIteration:
                    continue
                else:
                    matches = []
                    researched = textools.re_search(file_regexp, 
                        text, start = 0, end = max_len_searched, 
                        return_matches = matches, 
                        return_type = iter)
                    fpaths.append((path, researched, matches))
        else:
            fpaths.append(path)
    return fpaths

def format_html_new_regpart(html_list, regpart, show_tags_on_replace = False):
    '''Given the regpart that you changed, reformat the html_list with
    the new regpart replaced.'''
    assert(regpart != None)
    hiter = (n.regpart for n in html_list)
    
    index_start = iteration.first_index_is(hiter, regpart)
    if index_start == None:
        raise ValueError("regpart not found")
    index_end = iteration.first_index_isn(hiter, regpart)
    if index_end == None:
        index_end = index_start
    else:
        index_end = index_start + index_end
    
    new_html_section = _regpart_format_html(regpart, show_tags_on_replace=
            show_tags_on_replace)
            
    return tuple(itertools.chain(html_list[:index_start], new_html_section,
                html_list[index_end:]))
    
def _regpart_format_html(regpart, show_tags_on_replace = False):
    '''Formats a reg_part'''
    data_list, indexes, groups, match_data = (regpart.data_list, regpart.indexes,
        regpart.groups, regpart.match_data)

    if match_data:
        replace = regpart.replace_str
        if replace:
            repl_color = get_color_str(0,0,0)
            std_color = get_color_str(255, 0, 0)
        else:
            std_color = get_color_str(0,0,0)
    else:
        replace = None
        std_color = get_color_str(0,0,0)
    
    colors = [get_color_from_index(i, len(groups)) for i in indexes]

    html_list = []
    # front formatting
    if (match_data != None and 
            (show_tags_on_replace == True or replace == None)):
        html_span_tags = get_html_span_tags(bold = True, underlined = True, 
                                            lower = True)
        match = match_data[0]
        
        html_list.extend(text_format_html('{0}:'.format(match), html_span_tags,
                                          not_plain = True))

    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(text_format_html(
                '(', get_html_span_tags(bold = True, color = colors[i]),
                not_plain = True))
    if replace:
        html_list.extend(text_format_html(regpart.text, 
            get_html_span_tags(bold = True, color = std_color), 
            not_plain = False)) # want to clearly mark that this IS plain
            
    else:
        for data in data_list:
            if type(data) == str:
                html_list.extend(text_format_html(data, 
                    get_html_span_tags(bold = True, color = std_color), 
                    not_plain = False))
            else:
                html_list.extend(_regpart_format_html(data, 
                                                     show_tags_on_replace))
    
    if show_tags_on_replace == True or replace == None:
        for i in range(len(indexes)):
            html_list.extend(text_format_html(')', 
                get_html_span_tags(bold = True, color = colors[i]), 
                not_plain = True))
            html_list.extend(text_format_html('{0}'.format(indexes[i]),
                get_html_span_tags(bold = True, color = colors[i], 
                                   lower = True), not_plain = True))
    
    if replace:
        html_list.extend(text_format_html(replace,
            get_html_span_tags(bold = True, color = repl_color,
            underlined = True), not_plain = True))
    
    for rp in regpart_html:
        rp.regpart = data
    return html_list

    
class RegExpBuilder(object):
    '''This class is meant to make it simple to build regular expressions by
    just setting single variables
    Right now it's super simple and can just match the start, end,
    and any text in the middle of a word or phrase'''
    MatchType = dict((n[1],n[0]) for n in enumerate(
        ('word', 'phrase', 'text body')))
    def __init__(self):
        s = self        
        s.start = None
        s.end = None
        s.middle = None



if __name__ == '__main__':
    import dbe
    from pprint import pprint
    from PyQt import treeview
    
    out = get_match_paths('/home/user/Projects/Learning/LearningQt', '.*')
    print '\n\n\nOUTPUT'
    for n in out:
        print n
    fnodes = treeview.get_filelist_nodes(out)
    treeview.dev_show_file_list(fnodes)