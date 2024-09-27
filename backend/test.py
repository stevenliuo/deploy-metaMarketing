from pptx import Presentation


try:
    presentation = Presentation('/home/renui/template_content.pptx')
except Exception as e:
    print(e)
