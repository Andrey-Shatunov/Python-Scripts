import dominate
from dominate.tags import *


def html_table_from_list(my_list):
    doc = dominate.document(title='Report')
    with doc.add(body()).add(div(id='content')):
        with table(width="100%",border="0",cellpadding="0",bgcolor="black"):
            for i in my_list:
                if isinstance(i[0], str) and i[0].find("Progect name - ")>=0:
                    l = tr(align="left",bgcolor="#CCCCCC")
                else:
                    l = tr(align="left",bgcolor="#ffffff")
                for j in i:
                        l.add(td(j,align="left"))
						
    return str(doc)
	
