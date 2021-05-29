from market import app


if __name__ == '__main__':
    app.run(debug=True)


'''
pyinstaller -F --add-data "E:/Testing/loginsite/dbase.db;." --add-data "E:/Testing/loginsite/templates;templates" --hidden-import "flask" --hidden-import "flask_sqlalchemy" --hidden-import "jinja2"  "E:/Testing/loginsite/run.py"
'''
'''pyinstaller -F 
--add-data "E:/Testing/loginsite/dbase.db;." 
--add-data "E:/Testing/loginsite/templates;templates" 
--hidden-import "flask" 
--hidden-import "flask_sqlalchemy" 
--hidden-import "jinja2"  
"E:/Testing/loginsite/run.py"
'''
"""
Login with api
relation product and user
"""