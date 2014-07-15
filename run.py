from eve import Eve
app = Eve(settings='conf/settings.py')

if __name__ == '__main__':
    app.run()
