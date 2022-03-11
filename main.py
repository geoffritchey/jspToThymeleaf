from pathlib import Path
from bs4 import BeautifulSoup
import fnmatch
import sys
import re
import os
import glob
import lxml


if __name__ == '__main__':
    path = 'C:/Users/geoff.ritchey/Documents/GitHub/new/src/main/webapp/WEB-INF/view/'

    for infile in glob.glob(os.path.join(path, "*.jsp")):
        markup = (infile)
        soup = BeautifulSoup('<!DOCTYPE html>\r<html xmlns:th="http://www.thymeleaf.org">\r' + open(markup, "r").read().replace("</head>", "</head>\r<body>\r") + "</body>\r</html>\r"
                             , "lxml")

        ''' <div th:if="${access}">'''
        while True:
            h2 = soup.find('c:if')
            if not h2:
                break
            h2.name = 'div'
            h2['th:if'] = h2['test']
            del h2['test']

        ''' <p th:text="${#messages.msg('day.notes')}"></p>  '''
        while True:
            h2 = soup.find('fmt:message')
            if not h2:
                break
            h2.name = 'p'
            if h2.has_attr('key'):
                h2['th:text'] = "${#messages.msg('" + h2['key'] + "')}"
                del h2['key']

        with open("C:/Users/geoff.ritchey/Documents/soup/" + Path(infile).stem + ".html", 'w') as f:
            print(soup, file=f)
