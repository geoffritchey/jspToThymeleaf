from pathlib import Path
from bs4 import BeautifulSoup
import fnmatch
import sys
import re
import os
import glob
import lxml


def make_errors(root, formPath):
    h3 = root.find('span', class_="fieldError")
    if h3:
        field = path.replace(formPath + ".", "")
        h3["th:if"] = "${#fields.hasErrors('" + field + "')}"
        h3["th:errors"] = "*{" + field + "}"
        h3.string = ""


def findBind(root, formPath):
    while True:
        h2 = root.find("spring:bind")
        if not h2:
            break
        h2.name = 'div'
        print("h2 path = ", h2['path'])
        path = re.sub(r"([.\w]*?)(?:\.\*)?", r"\1", h2['path'])
        print(path)
        del h2['path']
        while True:
            h3 = h2.find('c:if')
            if not h3:
                break;
            h3.name = 'div'
            source = h3['test']
            source = re.sub(r"\bnot\b", "!", source)
            print("1", source)
            source = re.sub(r"\bstatus(.value)?\b", path, source)
            print("2", source)
            source = re.sub(r"\bempty\b\s*([.\w]*)", r"#arrays.isEmpty(\1)", source)
            print("3", source)
            h3['th:if'] = source
            del h3['test']
        while True:
            h3 = h2.find('input')
            if not h3:
                break
            if h3.has_attr("name"):
                del h3['name']
            h3["th:field"] = "*{" + path.replace(formPath + ".", "") + "}"
            if h3.has_attr("value"):
                del h3["value"]
            h3.name = "inputa"
            make_errors(h3.find_parent("div"), formPath)
        while True:
            h3 = h2.find('select')
            if not h3:
                break
            h3.name = "selecta"
            if h3.has_attr("name"):
                del h3['name']
            h3["th:field"] = "*{" + path.replace(formPath + ".", "") + "}"
            if h3.has_attr("value"):
                del h3["value"]
            while True:
                h4 = h3.find('c:foreach')
                if not h4:
                    break
                h4.name = "option"
                var = h4['var']
                items = h4['items']
                del h4['var']
                del h4['items']
                h4['th:each'] = var + " : " + items
                h5 = h4.find('option')
                h4['th:value'] = h5["value"]
                h4['th:text'] = h5.text.strip()
                h5.extract()
                make_errors(h3.find_parent("div"), formPath)


if __name__ == '__main__':
    path = 'C:/Users/geoff.ritchey/Documents/GitHub/new/src/main/webapp/WEB-INF/view/'

    for infile in glob.glob(os.path.join(path, "*.jsp")):
        markup = (infile)
        lines = '<!DOCTYPE html>\r<html xmlns:th="http://www.thymeleaf.org">\r' + open(markup, "r").read();
        print(markup)
        if (not markup.endswith("payPeriodForm.jsp")):
            continue
        lines = re.sub(r"(.*\n)*</head>", """
        <!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<!-- payPeriodForm.jsp, PayPeriodFormController.java -->
<head>
<meta http-equiv="X-UA-Compatible" content="IE=8" />
<title>term List</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link th:href="@{zengarden-sample.css}" type="text/css" rel="stylesheet" />
<link href="@{favicon.ico}" rel="SHORTCUT ICON" />

</head>
<body>

	<a name="top"></a>
	<div id="container">
		<div id="intro">
			<header th:insert="fragments/header.html :: header"> </header>

			<div id="content">

				<div th:insert="fragments/bread.html :: bread"></div>
        """, lines, re.MULTILINE) + """
        			</div>
		</div>
		<footer th:insert="fragments/footer.html :: footer"> </footer>
	</div>
	</body>
</html>
        """

        lines = re.sub(r'<c:url\s*value="([^"]*)"[^>]*>', r"\1", lines)
        lines = re.sub(r'<c:if.*?selected.*?c:if>', r"", lines)

        mainPath = None
        soup = BeautifulSoup(lines, "lxml")
        while True:
            h2 = soup.find("spring:bind")
            if not h2:
                break
            h2.name = 'div'
            print("h2 path = ", h2['path'])
            path = re.sub(r"([.\w]*?)(?:\.\*)?", r"\1", h2['path'])
            if mainPath is None:
                mainPath = path
            print(path)
            del h2['path']
            while True:
                h3 = h2.find('c:if')
                if not h3:
                    break;
                h3.name = 'div'
                source = h3['test']
                source = re.sub(r"\bnot\b", "!", source)
                print("1",source)
                source = re.sub(r"\bstatus(.value)?\b", path, source)
                print("2",source)
                source = re.sub(r"\bempty\b\s*([.\w]*)", r"#arrays.isEmpty(\1)", source)
                print("3",source)
                h3['th:if']  = source
                del h3['test']
            break;

        while True:
            h2 = soup.find("form")
            if not h2:
                break;
            h2['th:object'] = mainPath
            oldAction = h2['action']
            h2['action'] = '#'
            if h2.has_attr('value'):
                value = h2['value']
                h2['th:action'] = re.sub(r"(.*\))", r"@{/\1}", value)
                del h2['value']
            h2.name = "forma"
            findBind(h2, mainPath)

        while True:
            h2 = soup.find('c:if')
            if not h2:
                break
            h2.name = 'div'
            h2['th:if'] = h2['test']
            del h2['test']
            print(h2['th:if'])

        ''' <p th:text="${#messages.msg('day.notes')}"></p>  '''

        while True:
            h2 = soup.find('fmt:message')
            if not h2:
                break
            parent = h2.parent
            if h2.has_attr('key'):
                h2['th:text'] = "${#messages.msg('" + h2['key'] + "')}"
                del h2['key']
                if parent.name == 'label':
                    parent['th:text'] = h2['th:text']
                    h2.extract()
                else:
                    h2.name = 'span'


        while True:
            h2 = soup.find('forma')
            if not h2:
                break
            h2.name = "form"
        while True:
            h2 = soup.find('inputa')
            if not h2:
                break
            h2.name = "input"
        while True:
            h2 = soup.find('selecta')
            if not h2:
                break
            h2.name = "select"

        with open("C:/Users/geoff.ritchey/Documents/soup/" + Path(infile).stem + ".html", 'w') as f:
            print(soup.prettify(), file=f)
