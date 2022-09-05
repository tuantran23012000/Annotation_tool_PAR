from __future__ import division
from PIL import Image as PImage, ImageTk
import os
import sys
import glob
import random
import shutil
import tkinter as tk
if(sys.version_info[0] == 2):
    from Tkinter import *
    import tkMessageBox
elif(sys.version_info[0] == 3):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox

binary_label = ['No', 'Yes']    
binary_value = ['0','1']        # No/Yes
age_value = ['0','1','2']       # Short / Tall / More than 50
age_text = ['Short','Tall','More than 50']

# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.curimg_h = 0
        self.curimg_w = 0

        self.cur_gender_id = 0
        self.cur_age = 1
        self.cur_long_hair = 0
        self.cur_glasses = 0
        self.cur_hat = 0
        self.cur_ssleeves = 0
        self.cur_trouser = 0
        self.cur_jean = 0
        self.cur_short = 0
        self.cur_skirt = 0
        self.cur_shorts = 0
        self.cur_backpack = 0
        self.cur_bag = 0
        self.cur_attOther = 0
        self.ub_black = 0
        self.ub_white = 0
        self.ub_gray = 0
        self.ub_red = 0
        self.ub_green = 0
        self.ub_blue = 0
        self.ub_yellow = 0
        self.ub_brown = 0
        self.ub_purple = 0
        self.ub_pink = 0
        self.ub_orange = 0
        self.ub_mix = 0
        self.ub_other = 0
        self.lb_black = 0
        self.lb_white = 0
        self.lb_gray = 0
        self.lb_red = 0
        self.lb_green = 0
        self.lb_blue = 0
        self.lb_yellow = 0
        self.lb_brown = 0
        self.lb_purple = 0
        self.lb_pink = 0
        self.lb_orange = 0
        self.lb_mix = 0
        self.lb_other = 0
        
        self.parent = master
        self.parent.title("Annotation Tool")
        self.frame = Frame(self.parent, bg='LightBlue')
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)
        #self.parent.resizable(0,0)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0


        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.loadEntry)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 3, sticky = W+E)
        
        #yes/no label:
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 1, column = i+3, sticky = W+N)

        #   Gender:
        self.tkvar_gender = StringVar(self.parent)
        self.cur_gender_id = 0
        self.tkvar_gender.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Female", bg='LightBlue')
        self.chooselbl.grid(row = 2, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_gender, value = binary_value[i], command = self.gender_click)
            self.rdbtn.grid(row = 2, column = i+3, sticky = W+N)

        self.chooselbl = Label(self.frame, text = "Head", bg='LightBlue', anchor = CENTER)
        self.chooselbl.grid(row = 3, column = 3, sticky=W+N)

        #   Long Hair:
        self.tkvar_lHair = StringVar(self.parent)
        self.cur_long_hair = 0
        self.tkvar_lHair.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Long Hair", bg='LightBlue')
        self.chooselbl.grid(row = 4, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lHair, 
            value = binary_value[i], command = self.hair_click)
            self.rdbtn.grid(row = 4, column = i+3, sticky = W+N)
        
        #   Glasses:
        self.tkvar_glasses = StringVar(self.parent)
        self.cur_glasses = 0
        self.tkvar_glasses.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Glasses", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_glasses, 
            value = binary_value[i], command = self.glasses_click)
            self.rdbtn.grid(row = 5, column = i+3, sticky = W+N)

        self.chooselbl = Label(self.frame, text = "        ", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 5, sticky=W+N)
        #   Appearance:
        self.chooselbl = Label(self.frame, text = "Appearance", bg='LightBlue')
        self.chooselbl.grid(row = 1, column = 7, sticky=W+N)
        self.tkvar_age = StringVar(self.parent)
        self.cur_age = 1
        self.tkvar_age.set(age_value[1])
        for i in range(len(age_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_age, 
            value = age_value[i], command = self.age_click, text = age_text[i])
            self.rdbtn.grid(row = i+2, column = 7, sticky = W+N)
        
        #   Hat:
        self.tkvar_hat = StringVar(self.parent)
        self.cur_hat = 0
        self.tkvar_hat.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Hat", bg='LightBlue')
        self.chooselbl.grid(row = 6, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_hat, 
            value = binary_value[i], command = self.hat_click)
            self.rdbtn.grid(row = 6, column = i+3, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "Upper Body", bg='LightBlue', anchor = CENTER)
        self.chooselbl.grid(row = 7, column = 3, sticky=W+N)

        #   Short sleeves:
        self.tkvar_ss = StringVar(self.parent)
        self.cur_ssleeves = 0
        self.tkvar_ss.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Short sleeves", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ss, 
            value = binary_value[i], command = self.ss_click)
            self.rdbtn.grid(row = 8, column = i+3, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "Lower Body", bg='LightBlue', anchor = CENTER)
        self.chooselbl.grid(row = 9, column = 3, sticky=W+N)

        #   Trouser:
        self.tkvar_trouser = StringVar(self.parent)
        self.cur_trouser = 0
        self.tkvar_trouser.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Trousers", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_trouser, 
            value = binary_value[i], command = self.trouser_click)
            self.rdbtn.grid(row = 10, column = i+3, sticky = W+N)
        
        #   Jean:
        self.tkvar_jean = StringVar(self.parent)
        self.cur_jean = 0
        self.tkvar_jean.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Jeans", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_jean, 
            value = binary_value[i], command = self.jean_click)
            self.rdbtn.grid(row = 11, column = i+3, sticky = W+N)
        
        #   Skirt:
        self.tkvar_skirt = StringVar(self.parent)
        self.cur_skirt = 0
        self.tkvar_skirt.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Skirt", bg='LightBlue')
        self.chooselbl.grid(row = 12, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_skirt, 
            value = binary_value[i], command = self.skirt_click)
            self.rdbtn.grid(row = 12, column = i+3, sticky = W+N)
        
        #   Short:
        self.tkvar_short = StringVar(self.parent)
        self.cur_short = 0
        self.tkvar_short.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Short", bg='LightBlue')
        self.chooselbl.grid(row = 13, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_short, 
            value = binary_value[i], command = self.short_click)
            self.rdbtn.grid(row = 13, column = i+3, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "Attachment", bg='LightBlue', anchor = CENTER)
        self.chooselbl.grid(row = 14, column = 3, sticky=W+N)

        #   Back pack:
        self.tkvar_backpack = StringVar(self.parent)
        self.cur_backpack = 0
        self.tkvar_backpack.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Back pack", bg='LightBlue')
        self.chooselbl.grid(row = 15, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_backpack, 
            value = binary_value[i], command = self.backpack_click)
            self.rdbtn.grid(row = 15, column = i+3, sticky = W+N)
        
        #   Bag:
        self.tkvar_bag = StringVar(self.parent)
        self.cur_bag = 0
        self.tkvar_bag.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Bag", bg='LightBlue')
        self.chooselbl.grid(row = 16, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_bag, 
            value = binary_value[i], command = self.bag_click)
            self.rdbtn.grid(row = 16, column = i+3, sticky = W+N)
        
        #   att Other:
        self.tkvar_attOther = StringVar(self.parent)
        self.cur_attOther = 0
        self.tkvar_attOther.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Other att", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_attOther, 
            value = binary_value[i], command = self.attOther_click)
            self.rdbtn.grid(row = 17, column = i+3, sticky = W+N)
        

        self.chooselbl = Label(self.frame, text = "  ", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 7, sticky=W+N)
        self.chooselbl = Label(self.frame, text = "Upper Color", bg='LightBlue')
        self.chooselbl.grid(row = 7, column = 7, sticky=W+N)

        #yes/no label:
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 6, column = 2*i+8, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "  ", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 9, sticky=W+N)

        #   ub-Black:
        self.tkvar_ub_black = StringVar(self.parent)
        self.ub_black = 0
        self.tkvar_ub_black.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Black", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_black, 
            value = binary_value[i], command = self.ubblack_click)
            self.rdbtn.grid(row = 8, column = 2*i+8, sticky = W+N)

        #   ub-White:
        self.tkvar_ub_white = StringVar(self.parent)
        self.ub_white = 0
        self.tkvar_ub_white.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "White", bg='LightBlue')
        self.chooselbl.grid(row = 9, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_white, 
            value = binary_value[i], command = self.ubwhite_click)
            self.rdbtn.grid(row = 9, column = 2*i+8, sticky = W+N)
        
        #   ub-Gray:
        self.tkvar_ub_gray = StringVar(self.parent)
        self.ub_gray = 0
        self.tkvar_ub_gray.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Gray", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_gray, 
            value = binary_value[i], command = self.ubgray_click)
            self.rdbtn.grid(row = 10, column = 2*i+8, sticky = W+N)
        
        #   ub-Red:
        self.tkvar_ub_red = StringVar(self.parent)
        self.ub_red = 0
        self.tkvar_ub_red.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Red", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_red, 
            value = binary_value[i], command = self.ubred_click)
            self.rdbtn.grid(row = 11, column = 2*i+8, sticky = W+N)
        
        #   ub-Green:
        self.tkvar_ub_green = StringVar(self.parent)
        self.ub_green = 0
        self.tkvar_ub_green.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Green", bg='LightBlue')
        self.chooselbl.grid(row = 12, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_green, 
            value = binary_value[i], command = self.ubgreen_click)
            self.rdbtn.grid(row = 12, column = 2*i+8, sticky = W+N)
        
        #   ub-Blue:
        self.tkvar_ub_blue = StringVar(self.parent)
        self.ub_blue = 0
        self.tkvar_ub_blue.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Blue", bg='LightBlue')
        self.chooselbl.grid(row = 13, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_blue, 
            value = binary_value[i], command = self.ubblue_click)
            self.rdbtn.grid(row = 13, column = 2*i+8, sticky = W+N)
        
        #   ub-Yellow:
        self.tkvar_ub_yellow = StringVar(self.parent)
        self.ub_yellow = 0
        self.tkvar_ub_yellow.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Yellow", bg='LightBlue')
        self.chooselbl.grid(row = 14, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_yellow, 
            value = binary_value[i], command = self.ubyellow_click)
            self.rdbtn.grid(row = 14, column = 2*i+8, sticky = W+N)
        
        #   ub-Brown:
        self.tkvar_ub_brown = StringVar(self.parent)
        self.ub_brown = 0
        self.tkvar_ub_brown.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Brown", bg='LightBlue')
        self.chooselbl.grid(row = 15, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_brown, 
            value = binary_value[i], command = self.ubbrown_click)
            self.rdbtn.grid(row = 15, column = 2*i+8, sticky = W+N)
        
        #   ub-Purple:
        self.tkvar_ub_purple = StringVar(self.parent)
        self.ub_purple = 0
        self.tkvar_ub_purple.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Purple", bg='LightBlue')
        self.chooselbl.grid(row = 16, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_purple, 
            value = binary_value[i], command = self.ubpurple_click)
            self.rdbtn.grid(row = 16, column = 2*i+8, sticky = W+N)
        
        #   ub-Pink:
        self.tkvar_ub_pink = StringVar(self.parent)
        self.ub_pink = 0
        self.tkvar_ub_pink.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Pink", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_pink, 
            value = binary_value[i], command = self.ubpink_click)
            self.rdbtn.grid(row = 17, column = 2*i+8, sticky = W+N)
        
        #   ub-Orange:
        self.tkvar_ub_orange = StringVar(self.parent)
        self.ub_orange = 0
        self.tkvar_ub_orange.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Orange", bg='LightBlue')
        self.chooselbl.grid(row = 18, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_orange, 
            value = binary_value[i], command = self.uborange_click)
            self.rdbtn.grid(row = 18, column = 2*i+8, sticky = W+N)
        
        #   ub-Mix:
        self.tkvar_ub_mix = StringVar(self.parent)
        self.ub_mix = 0
        self.tkvar_ub_mix.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mixture", bg='LightBlue')
        self.chooselbl.grid(row = 19, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_mix, 
            value = binary_value[i], command = self.ubmix_click)
            self.rdbtn.grid(row = 19, column = 2*i+8, sticky = W+N)
        
        #   ub-Other:
        self.tkvar_ub_other = StringVar(self.parent)
        self.ub_other = 0
        self.tkvar_ub_other.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Other", bg='LightBlue')
        self.chooselbl.grid(row = 20, column = 7, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_ub_other, 
            value = binary_value[i], command = self.ubother_click)
            self.rdbtn.grid(row = 20, column = 2*i+8, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "  ", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 11, sticky=W+N)
        self.chooselbl = Label(self.frame, text = "Lower Color", bg='LightBlue')
        self.chooselbl.grid(row = 7, column = 11, sticky=W+N)

        #yes/no label:
        for i in range(len(binary_label)):
            self.chooselbl = Label(self.frame, text = binary_label[i], bg='LightBlue')
            self.chooselbl.grid(row = 6, column = 2*i+12, sticky = W+N)
        
        self.chooselbl = Label(self.frame, text = "  ", bg='LightBlue')
        self.chooselbl.grid(row = 5, column = 13, sticky=W+N)


        #   lb-Black:
        self.tkvar_lb_black = StringVar(self.parent)
        self.lb_black = 0
        self.tkvar_lb_black.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Black", bg='LightBlue')
        self.chooselbl.grid(row = 8, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_black, 
            value = binary_value[i], command = self.lbblack_click)
            self.rdbtn.grid(row = 8, column = 2*i+12, sticky = W+N)

        #   lb-White:
        self.tkvar_lb_white = StringVar(self.parent)
        self.lb_white = 0
        self.tkvar_lb_white.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "White", bg='LightBlue')
        self.chooselbl.grid(row = 9, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_white, 
            value = binary_value[i], command = self.lbwhite_click)
            self.rdbtn.grid(row = 9, column = 2*i+12, sticky = W+N)
        
        #   lb-Gray:
        self.tkvar_lb_gray = StringVar(self.parent)
        self.lb_gray = 0
        self.tkvar_lb_gray.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Gray", bg='LightBlue')
        self.chooselbl.grid(row = 10, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_gray, 
            value = binary_value[i], command = self.lbgray_click)
            self.rdbtn.grid(row = 10, column = 2*i+12, sticky = W+N)
        
        #   lb-Red:
        self.tkvar_lb_red = StringVar(self.parent)
        self.lb_red = 0
        self.tkvar_lb_red.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Red", bg='LightBlue')
        self.chooselbl.grid(row = 11, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_red, 
            value = binary_value[i], command = self.lbred_click)
            self.rdbtn.grid(row = 11, column = 2*i+12, sticky = W+N)
        
        #   lb-Green:
        self.tkvar_lb_green = StringVar(self.parent)
        self.lb_green = 0
        self.tkvar_lb_green.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Green", bg='LightBlue')
        self.chooselbl.grid(row = 12, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_green, 
            value = binary_value[i], command = self.lbgreen_click)
            self.rdbtn.grid(row = 12, column = 2*i+12, sticky = W+N)
        
        #   lb-Blue:
        self.tkvar_lb_blue = StringVar(self.parent)
        self.lb_blue = 0
        self.tkvar_lb_blue.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Blue", bg='LightBlue')
        self.chooselbl.grid(row = 13, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_blue, 
            value = binary_value[i], command = self.lbblue_click)
            self.rdbtn.grid(row = 13, column = 2*i+12, sticky = W+N)
        
        #   lb-Yellow:
        self.tkvar_lb_yellow = StringVar(self.parent)
        self.lb_yellow = 0
        self.tkvar_lb_yellow.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Yellow", bg='LightBlue')
        self.chooselbl.grid(row = 14, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_yellow, 
            value = binary_value[i], command = self.lbyellow_click)
            self.rdbtn.grid(row = 14, column = 2*i+12, sticky = W+N)
        
        #   lb-Brown:
        self.tkvar_lb_brown = StringVar(self.parent)
        self.lb_brown = 0
        self.tkvar_lb_brown.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Brown", bg='LightBlue')
        self.chooselbl.grid(row = 15, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_brown, 
            value = binary_value[i], command = self.lbbrown_click)
            self.rdbtn.grid(row = 15, column = 2*i+12, sticky = W+N)
        
        #   lb-Purple:
        self.tkvar_lb_purple = StringVar(self.parent)
        self.lb_purple = 0
        self.tkvar_lb_purple.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Purple", bg='LightBlue')
        self.chooselbl.grid(row = 16, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_purple, 
            value = binary_value[i], command = self.lbpurple_click)
            self.rdbtn.grid(row = 16, column = 2*i+12, sticky = W+N)
        
        #   lb-Pink:
        self.tkvar_lb_pink = StringVar(self.parent)
        self.lb_pink = 0
        self.tkvar_lb_pink.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Pink", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_pink, 
            value = binary_value[i], command = self.lbpink_click)
            self.rdbtn.grid(row = 17, column = 2*i+12, sticky = W+N)
        
        #   lb-Orange:
        self.tkvar_lb_orange = StringVar(self.parent)
        self.lb_orange = 0
        self.tkvar_lb_orange.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Orange", bg='LightBlue')
        self.chooselbl.grid(row = 18, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_orange, 
            value = binary_value[i], command = self.lborange_click)
            self.rdbtn.grid(row = 18, column = 2*i+12, sticky = W+N)
        
        #   lb-Mix:
        self.tkvar_lb_mix = StringVar(self.parent)
        self.lb_mix = 0
        self.tkvar_lb_mix.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Mixture", bg='LightBlue')
        self.chooselbl.grid(row = 19, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_mix, 
            value = binary_value[i], command = self.lbmix_click)
            self.rdbtn.grid(row = 19, column = 2*i+12, sticky = W+N)
        
        #   lb-Other:
        self.tkvar_lb_other = StringVar(self.parent)
        self.lb_other = 0
        self.tkvar_lb_other.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Other", bg='LightBlue')
        self.chooselbl.grid(row = 20, column = 11, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_lb_other, 
            value = binary_value[i], command = self.lbother_click)
            self.rdbtn.grid(row = 20, column = 2*i+12, sticky = W+N)

        #   att Other:
        self.tkvar_attOther = StringVar(self.parent)
        self.cur_attOther = 0
        self.tkvar_attOther.set(binary_value[0])
        self.chooselbl = Label(self.frame, text = "Other att", bg='LightBlue')
        self.chooselbl.grid(row = 17, column = 2, sticky=W+N)
        for i in range(len(binary_value)):
            self.rdbtn = Radiobutton(self.frame,variable = self.tkvar_attOther, 
            value = binary_value[i], command = self.attOther_click)
            self.rdbtn.grid(row = 17, column = i+3, sticky = W+N)
        
        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.parent.bind("<Left>", self.prevImage) # press 'a' to go backward
        self.parent.bind("<Right>", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 10, sticky = W+N)

        # control panel for image navigation
        #self.ctrPanel = Frame(self.frame)
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 30, column = 1, columnspan = 2, sticky = W+S)
        #self.ctrPanel.pack(padx = 30, pady = 1)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = tk.Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.v = StringVar(self.ctrPanel)
        self.idxEntry = Entry(self.ctrPanel, width = 5,textvariable=self.v)
        self.idxEntry.pack(side = LEFT)
        # self.idxEntry = Text(self.ctrPanel, height = 5,width = 5)
        # self.idxEntry.grid(row=0, column=5)
        
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)
        self.delBtn = Button(self.ctrPanel, text = 'Delete', command = self.deleteImage)
        self.delBtn.pack(side = LEFT)

        self.frame.columnconfigure(1, weight = 1)
        #self.frame.rowconfigure(4, weight = 1)

    def loadEntry(self,event):
        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            try:
                s = self.entry.get()
                self.parent.focus()
                self.category = s
            except ValueError as ve:
                tkMessageBox.showerror("Error!", message = "The folder should be numbers")
                return
        if not os.path.isdir('./Images/%s' % self.category):
           tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
           return
        # get image list
        self.imageDir = os.path.join(r'./Images', '%s' %(self.category))
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            tkMessageBox.showerror("Error!", message = "No .jpg images found in the specified dir!")
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        if not os.path.exists('./Labels'):
            os.mkdir('./Labels')
        self.outDir = os.path.join(r'./Labels', '%s' %(self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = PImage.open(imagepath)
        self.curimg_w, self.curimg_h = self.img.size
        aspect_h = int(self.curimg_h/300)
        if self.curimg_h>300:
            aspect_w = int(self.curimg_w/aspect_h)         
            self.img = self.img.resize((aspect_w, 300))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 300), height = max(self.tkimg.height(), 300))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor="nw")
        #print(self.tkimg)
        #print(self.img)

        # load labels
        # self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        self.imagename = os.path.splitext(os.path.basename(imagepath))[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                temp_data_str=f.read().replace("\n","")
            temp_data=temp_data_str.split(",")
            print(temp_data)

            self.cur_gender_id = binary_value.index(temp_data[0])
            self.tkvar_gender.set(temp_data[0])

            if temp_data[1] == '1':
                self.cur_age = age_value.index('0')
                self.tkvar_age.set('0')
            if temp_data[2] == '1':
                self.cur_age = age_value.index('1')
                self.tkvar_age.set('1')
            if temp_data[3] == '1':
                self.cur_age = age_value.index('2')
                self.tkvar_age.set('2')

            self.cur_long_hair = binary_value.index(temp_data[4])
            self.tkvar_lHair.set(temp_data[4])

            self.cur_glasses = binary_value.index(temp_data[5])
            self.tkvar_glasses.set(temp_data[5])

            self.cur_hat = binary_value.index(temp_data[6])
            self.tkvar_hat.set(temp_data[6])
            
            self.cur_ssleeves = binary_value.index(temp_data[7])
            self.tkvar_ss.set(temp_data[7])
            
            self.cur_trouser = binary_value.index(temp_data[8])
            self.tkvar_trouser.set(temp_data[8])
            
            self.cur_jean = binary_value.index(temp_data[9])
            self.tkvar_jean.set(temp_data[9])
            
            self.cur_skirt = binary_value.index(temp_data[10])
            self.tkvar_skirt.set(temp_data[10])
            
            self.cur_short = binary_value.index(temp_data[11])
            self.tkvar_short.set(temp_data[11])
            
            self.cur_backpack = binary_value.index(temp_data[12])
            self.tkvar_backpack.set(temp_data[12])
            
            self.cur_bag = binary_value.index(temp_data[13])
            self.tkvar_bag.set(temp_data[13])
            
            self.cur_attOther = binary_value.index(temp_data[14])
            self.tkvar_attOther.set(temp_data[14])
            
            self.ub_black = binary_value.index(temp_data[15])
            self.tkvar_ub_black.set(temp_data[15])
            
            self.ub_white = binary_value.index(temp_data[16])
            self.tkvar_ub_white.set(temp_data[16])
            
            self.ub_gray = binary_value.index(temp_data[17])
            self.tkvar_ub_gray.set(temp_data[17])
            
            self.ub_red = binary_value.index(temp_data[18])
            self.tkvar_ub_red.set(temp_data[18])
            
            self.ub_green = binary_value.index(temp_data[19])
            self.tkvar_ub_green.set(temp_data[19])
            
            self.ub_blue = binary_value.index(temp_data[20])
            self.tkvar_ub_blue.set(temp_data[20])
            
            self.ub_yellow = binary_value.index(temp_data[21])
            self.tkvar_ub_yellow.set(temp_data[21])
            
            self.ub_brown = binary_value.index(temp_data[22])
            self.tkvar_ub_brown.set(temp_data[22])
            
            self.ub_purple = binary_value.index(temp_data[23])
            self.tkvar_ub_purple.set(temp_data[23])
            
            self.ub_pink = binary_value.index(temp_data[24])
            self.tkvar_ub_pink.set(temp_data[24])
            
            self.ub_orange = binary_value.index(temp_data[25])
            self.tkvar_ub_orange.set(temp_data[25])
            
            self.ub_mix = binary_value.index(temp_data[26])
            self.tkvar_ub_mix.set(temp_data[26])
            
            self.ub_other = binary_value.index(temp_data[27])
            self.tkvar_ub_other.set(temp_data[27])
            
            self.lb_black = binary_value.index(temp_data[28])
            self.tkvar_lb_black.set(temp_data[28])
            
            self.lb_white = binary_value.index(temp_data[29])
            self.tkvar_lb_white.set(temp_data[29])
            
            self.lb_gray = binary_value.index(temp_data[30])
            self.tkvar_lb_gray.set(temp_data[30])
            
            self.lb_red = binary_value.index(temp_data[31])
            self.tkvar_lb_red.set(temp_data[31])
            
            self.lb_green = binary_value.index(temp_data[32])
            self.tkvar_lb_green.set(temp_data[32])
            
            self.lb_blue = binary_value.index(temp_data[33])
            self.tkvar_lb_blue.set(temp_data[33])
            
            self.lb_yellow = binary_value.index(temp_data[34])
            self.tkvar_lb_yellow.set(temp_data[34])
            
            self.lb_brown = binary_value.index(temp_data[35])
            self.tkvar_lb_brown.set(temp_data[35])
            
            self.lb_purple = binary_value.index(temp_data[36])
            self.tkvar_lb_purple.set(temp_data[36])
            
            self.lb_pink = binary_value.index(temp_data[37])
            self.tkvar_lb_pink.set(temp_data[37])
            
            self.lb_orange = binary_value.index(temp_data[38])
            self.tkvar_lb_orange.set(temp_data[38])
            
            self.lb_mix = binary_value.index(temp_data[39])
            self.tkvar_lb_mix.set(temp_data[39])
            
            self.lb_other = binary_value.index(temp_data[40])
            self.tkvar_lb_other.set(temp_data[40])            
            

        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

    def saveImage(self):
        if self.tkvar_age.get() == '0':
            print('Less than 16')
            age = '1,0,0'
        if self.tkvar_age.get() == '1':
            print('17-45')
            age = '0,1,0'
        if self.tkvar_age.get() == '2':
            print('More than 45')
            age = '0,0,1'
        with open(self.labelfilename, 'w') as f:
            f.write(self.tkvar_gender.get()+','+age+','+self.tkvar_lHair.get()+','+self.tkvar_glasses.get()
            +','+self.tkvar_hat.get()+','+self.tkvar_ss.get()+','+self.tkvar_trouser.get()+','+self.tkvar_jean.get()
            +','+self.tkvar_skirt.get()+','+self.tkvar_short.get()+','+self.tkvar_backpack.get()+','+self.tkvar_bag.get()+','+self.tkvar_attOther.get()
            +','+self.tkvar_ub_black.get()+','+self.tkvar_ub_white.get()+','+self.tkvar_ub_gray.get()+','+self.tkvar_ub_red.get()+','+self.tkvar_ub_green.get()
            +','+self.tkvar_ub_blue.get()+','+self.tkvar_ub_yellow.get()+','+self.tkvar_ub_brown.get()+','+self.tkvar_ub_purple.get()
            +','+self.tkvar_ub_pink.get()+','+self.tkvar_ub_orange.get()+','+self.tkvar_ub_mix.get()+','+self.tkvar_ub_other.get()
            +','+self.tkvar_lb_black.get()+','+self.tkvar_lb_white.get()+','+self.tkvar_lb_gray.get()+','+self.tkvar_lb_red.get()+','+self.tkvar_lb_green.get()
            +','+self.tkvar_lb_blue.get()+','+self.tkvar_lb_yellow.get()+','+self.tkvar_lb_brown.get()+','+self.tkvar_lb_purple.get()
            +','+self.tkvar_lb_pink.get()+','+self.tkvar_lb_orange.get()+','+self.tkvar_lb_mix.get()+','+self.tkvar_lb_other.get())
        print('Image No. %d saved' %(self.cur))

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "This is first image")

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "All images annotated")

    def gotoImage(self):
        print("@@@@@@:",self.idxEntry.get())
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def deleteImage(self):
        self.saveImage()
        shutil.move(self.labelfilename, os.path.join('./Deleted',self.labelfilename.split('/')[0]))
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "All images annotated")


    def gender_click(self, *args):
        cur_gender_id = self.tkvar_gender.get()
        self.cur_gender_id = binary_value.index(cur_gender_id)

    def hair_click(self, *args):
        cur_long_hair = self.tkvar_lHair.get()
        self.cur_long_hair = binary_value.index(cur_long_hair)

    def glasses_click(self, *args):
        cur_glasses = self.tkvar_glasses.get()
        self.cur_glasses = binary_value.index(cur_glasses)
    
    def age_click(self, *args):
        cur_age = self.tkvar_age.get()
        self.cur_age = age_value.index(cur_age)
    
    def hat_click(self, *args):
        cur_hat = self.tkvar_hat.get()
        self.cur_hat = binary_value.index(cur_hat)

    def ss_click(self, *args):
        cur_ssleeves = self.tkvar_ss.get()
        self.cur_ssleeves = binary_value.index(cur_ssleeves)

    def trouser_click(self, *args):
        cur_trouser = self.tkvar_trouser.get()
        self.cur_trouser = binary_value.index(cur_trouser)
    
    def jean_click(self, *args):
        cur_jean = self.tkvar_jean.get()
        self.cur_jean = binary_value.index(cur_jean)
    
    def skirt_click(self, *args):
        cur_skirt = self.tkvar_skirt.get()
        self.cur_skirt = binary_value.index(cur_skirt)
    
    def short_click(self, *args):
        cur_short = self.tkvar_short.get()
        self.cur_short = binary_value.index(cur_short)
    
    def backpack_click(self, *args):
        cur_backpack = self.tkvar_backpack.get()
        self.cur_backpack = binary_value.index(cur_backpack)
    
    def bag_click(self, *args):
        cur_bag = self.tkvar_bag.get()
        self.cur_bag = binary_value.index(cur_bag)
    
    def attOther_click(self, *args):
        cur_attOther = self.tkvar_attOther.get()
        self.cur_attOther = binary_value.index(cur_attOther)
    
    def ubblack_click(self, *args):
        ub_black = self.tkvar_ub_black.get()
        self.ub_black = binary_value.index(ub_black)
    
    def ubwhite_click(self, *args):
        ub_white = self.tkvar_ub_white.get()
        self.ub_white = binary_value.index(ub_white)
    
    def ubgray_click(self, *args):
        ub_gray = self.tkvar_ub_gray.get()
        self.ub_gray = binary_value.index(ub_gray)
    
    def ubred_click(self, *args):
        ub_red = self.tkvar_ub_red.get()
        self.ub_red = binary_value.index(ub_red)
    
    def ubgreen_click(self, *args):
        ub_green = self.tkvar_ub_green.get()
        self.ub_green = binary_value.index(ub_green)
    
    def ubblue_click(self, *args):
        ub_blue = self.tkvar_ub_blue.get()
        self.ub_blue = binary_value.index(ub_blue)
    
    def ubyellow_click(self, *args):
        ub_yellow = self.tkvar_ub_yellow.get()
        self.ub_yellow = binary_value.index(ub_yellow)
    
    def ubbrown_click(self, *args):
        ub_brown = self.tkvar_ub_brown.get()
        self.ub_brown = binary_value.index(ub_brown)
    
    def ubpurple_click(self, *args):
        ub_purple = self.tkvar_ub_purple.get()
        self.ub_purple = binary_value.index(ub_purple)
    
    def ubpink_click(self, *args):
        ub_pink = self.tkvar_ub_pink.get()
        self.ub_pink = binary_value.index(ub_pink)
    
    def uborange_click(self, *args):
        ub_orange = self.tkvar_ub_orange.get()
        self.ub_orange = binary_value.index(ub_orange)
    
    def ubmix_click(self, *args):
        ub_mix = self.tkvar_ub_mix.get()
        self.ub_mix = binary_value.index(ub_mix)
    
    def ubother_click(self, *args):
        ub_other = self.tkvar_ub_other.get()
        self.ub_other = binary_value.index(ub_other)
    
    def lbblack_click(self, *args):
        lb_black = self.tkvar_lb_black.get()
        self.lb_black = binary_value.index(lb_black)
    
    def lbwhite_click(self, *args):
        lb_white = self.tkvar_lb_white.get()
        self.lb_white = binary_value.index(lb_white)
    
    def lbgray_click(self, *args):
        lb_gray = self.tkvar_lb_gray.get()
        self.lb_gray = binary_value.index(lb_gray)
    
    def lbred_click(self, *args):
        lb_red = self.tkvar_lb_red.get()
        self.lb_red = binary_value.index(lb_red)
    
    def lbgreen_click(self, *args):
        lb_green = self.tkvar_lb_green.get()
        self.lb_green = binary_value.index(lb_green)
    
    def lbblue_click(self, *args):
        lb_blue = self.tkvar_lb_blue.get()
        self.lb_blue = binary_value.index(lb_blue)
    
    def lbyellow_click(self, *args):
        lb_yellow = self.tkvar_lb_yellow.get()
        self.lb_yellow = binary_value.index(lb_yellow)
    
    def lbbrown_click(self, *args):
        lb_brown = self.tkvar_lb_brown.get()
        self.lb_brown = binary_value.index(lb_brown)
    
    def lbpurple_click(self, *args):
        lb_purple = self.tkvar_lb_purple.get()
        self.lb_purple = binary_value.index(lb_purple)
    
    def lbpink_click(self, *args):
        lb_pink = self.tkvar_lb_pink.get()
        self.lb_pink = binary_value.index(lb_pink)
    
    def lborange_click(self, *args):
        lb_orange = self.tkvar_lb_orange.get()
        self.lb_orange = binary_value.index(lb_orange)
    
    def lbmix_click(self, *args):
        lb_mix = self.tkvar_lb_mix.get()
        self.lb_mix = binary_value.index(lb_mix)
    
    def lbother_click(self, *args):
        lb_other = self.tkvar_lb_other.get()
        self.lb_other = binary_value.index(lb_other)

if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(5, minsize=100)
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
