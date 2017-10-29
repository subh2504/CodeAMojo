#!/usr/bin/env python
import os
import os.path
import json
import sys
from urllib.parse import unquote
import string
import pytesseract
import re
import difflib
import csv
from .crop_morphology import cm
from dateutil.parser import parse
try:
    from PIL import Image, ImageEnhance, ImageFilter
except:
    print("please install PIL")
    sys.exit()




class extract(object):

    def validate_pan_number(self,value):
        """
        Validates if the given value is a valid PAN number or not, if not raise ValidationError
        """
        if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
            return True
        else:
            return False


    def extract_pandata_individual(self,img_p,type):
        t=""


        path= unquote(img_p[1:])
        print(img_p)
        #cm([pa])
        img = Image.open(path)
        fill_color = '#ffffff'
        if img.mode in ('RGBA', 'LA'):
            background = Image.new(img.mode[:-1], img.size, fill_color)
            background.paste(img, img.split()[-1])
            img = background
        #img = img.convert('RGBA')
        pix = img.load()
        img.save('temp1.jpg')
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)

        img.save('temp.jpg')

        text = pytesseract.image_to_string(Image.open('temp.jpg'))

        text = ''.join([i if ord(i) < 128 else ' ' for i in text])
        #print(" OCr Text")
        print(text)
        # Initializing data variable
        name = ""
        fname = ""
        dob = ""
        pan = ""
        nameline = []
        dobline = []
        panline = []
        text0 = []
        text1 = []
        text2 = []

        # Searching for PAN
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)
        #print("text1")
        #print(text1)
        text1 = list(filter(None,text1))
        print(text1)
        lineno = 0
        for wordline in text1:
            xx = wordline.split()
            if ([w for w in xx if re.search('(Incorporati|ncorporat|corporati)$', w)]):
                type = 2
                break

        for wordline in text1:
            xx = wordline.split()
            if ([w for w in xx if re.search('(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
                lineno = text1.index(wordline)
                break


        text0 = text1[lineno + 0:]


        for wordline in text0:
            xx = wordline.split()
            if ([w for w in xx if re.search('(INDIA|NDIA)$', w)]):
                lineno = text0.index(wordline)
                break


        text0 = text1[lineno + 0:]
        #print("text0")
        #print(text0)

        #-----------Read Database

        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, '../namedb.csv')
        f=open(filename)
        #print(f.read())

        #f=open(r'test', 'rb')
        reader = csv.reader(f)
        newlist = list(reader)
        newlist = sum(newlist, [])

        #Searching for Name and finding closest name in database
        try:
            for x in text0:
                xx = x.split()
                if ([w for w in xx if re.search('(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$', w)]):
                    #print(xx)
                    break
                for y in x.split():

                    if (difflib.get_close_matches(y.upper(), newlist)):
                        nameline.append(x)
                        break
        except:
             pass

        #print("Name Line")
        #print(nameline)
        try:
            name = nameline[0]
            fname = nameline[1]
        except:
            pass
        #print(name,fname)

        try:
            dobline = [item for item in text0 if item not in nameline]
            #print("dobline")
            #print (dobline)
            for x in dobline:
                z = x.split()
                #print("z")
                #print(z)
                z = [s for s in z if len(s) > 3]
                #print(z)
                for y in z:
                    if (parse(y, fuzzy=True)):
                        dob = str(parse(y, fuzzy=True).day)+"/"+str(parse(y, fuzzy=True).month)+"/"+str(parse(y, fuzzy=True).year)
                        panline = dobline[dobline.index(x) + 1:]
                        break

        except Exception as e:
            pass
            #print(e)

        #print("DOB "+str(dob))

        try:
            #print(panline)
            for wordline in panline:
                xx = wordline.split()
                if ([w for w in xx if re.search('(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$', w)]):
                    pan = panline[panline.index(wordline) + 1]
                    break
            pan = pan.replace(" ", "")
        except:
            pass

        # Making tuples of data

        data = {}
        data['Name'] = name
        data['Father_Name'] = fname
        data['Date_of_Birth'] = dob
        data['PAN'] = pan
        data['type']=str(type)

        print(data)

        print(data['Name'])

        print(data['Father_Name'])
        print(data['Date_of_Birth'])
        print(data['PAN'])
        error="N"
        msg=""
        if(data['PAN'] == "" and data['Date_of_Birth'] == "" and data['Name'] ==""):
            print("Image Uploaded Is Not Readable")
            error="Y"
            msg="Image Uploaded Is Not Readable"
        elif(self.validate_pan_number(data['PAN'])):
            print("Not A Valid PAn Card")
            error="Y"
            msg="Not A Valid PAn Card"
        #Removing dummy files
        #os.remove('temp.jpg')

        return {"error":error,"msg":msg,"data":data}

#e = extract()
#print(e.extract_pandata_individual('/extractor/images.jpg'))




