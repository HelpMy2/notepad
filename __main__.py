import GUI.notepad as notepad

import sys
import json


ssd = {"reset":False,"font":["consolas",10,"normal"],"bg":"black","fg":"#ffffff","bd":2.5,"image":"image.png","geometry":"350x500+100+100","find_color":"#ff0000"}
try:
    with open('settings.json') as sf:
        settings = json.loads(sf.read())
        if settings['reset']:
            sf.write(json.dumps(ssd,separators=(',\n    ',':')))
except Exception as error:
    with open('settings.json','w') as sf:
        settings = ssd
        sf.write(json.dumps(ssd,separators=(',\n    ',':')))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            root = notepad.notepad(sys.argv[1],settings=settings)
        else:
            root = notepad.notepad(settings=settings)
        root.window.mainloop()

    except Exception as error:
        print('ERROR\n',error)
        with open('settings.json','w') as sf:
            settings = ssd
            sf.write(json.dumps(ssd, separators=(',\n    ', ':')))
