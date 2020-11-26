# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 19:45:17 2018

@author: User
"""

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print("Content-type: text/html")
print()

print("""
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
""")

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

print("""

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="index.cgi">
    <p>message: <input type="text" name="message"/></p>
  </form>

</body>

</html>
""" % cgi.escape(message))