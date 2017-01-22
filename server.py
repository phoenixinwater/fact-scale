import web
import time
from serverScript import *

def MakeString(string):
    return string

urls = ('/', 'index')
render = web.template.render('templates/')
app = web.application(urls, globals())
my_form = web.form.Form( web.form.Textbox('', class_='textfield', id='textfield'))

class index:
    def GET(self):
        form = my_form()
        return render.index(form, "Your text goes here.")

    def POST(self):
        form = my_form()
        form.validates()
        s = form.value['textfield']
        connected = MakeString(s)
        if connected == "true":
            return "I like watermelons@@I don't like watermelons"
        else:
            result = RunEvaluation(connected)
            return MakeString(result)
        return MakeString(s)

if __name__ == '__main__':
    app.run()
