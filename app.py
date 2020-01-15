from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
import time
import gc
import random

# creates database or connects
def initial_db():
    db = sql.connect('eng-chi.db')
    cs = db.cursor()
    cs.execute("CREATE TABLE IF NOT EXISTS dictionary ('eng','hanzi','pinyin')")
    db.commit()
    db.close()

# main Class
class App(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        container = Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        # Got from a tutorial, in order to show different pages...
        for F in (MainPage,RandomPage,AddPage,DictPage,QuizPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self,context):
        frame = self.frames[context]
        frame.tkraise()

    def close_app(self):
        time.sleep(0.2)
        self.destroy()

class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        lb1 = Label(self,text="English-Chinese Vocabulary Exercise App",font=(("times new roman"),25,"bold"))
        lb1.place(relx=0.5,rely=0.15,anchor="center")

        lb2 = Label(self,text="You can add vocabulary,\ncreate your own dictionary and exercise!",font=(("times new roman"),16,"italic"),fg="gray")
        lb2.place(relx=0.5,rely=0.4,anchor="center")

        add_but = Button(self,text="Add Vocabulary",font=(("times new roman"),14),width=16,
                         command=lambda:[controller.show_frame(AddPage),self.add_ref()])
        add_but.place(relx=0.2,rely=0.65,anchor="center")

        dict_but = Button(self,text="Dictionary",font=(("times new roman"),14),width=16,
                          command=lambda:[controller.show_frame(DictPage),self.dict_update()])
        dict_but.place(relx=0.4,rely=0.65,anchor="center")

        rand_but = Button(self,text="Random Words",font=(("times new roman"),14),width=16,
                          command=lambda:[controller.show_frame(RandomPage),self.init_rand()])
        rand_but.place(relx=0.6,rely=0.65,anchor="center")

        quiz_but = Button(self, text="Quiz", font=(("times new roman"), 14), width=16,
                          command=lambda:[controller.show_frame(QuizPage), self.init_quiz()])
        quiz_but.place(relx=0.8, rely=0.65, anchor="center")

        quit_but = Button(self,text="Quit",fg="red",font=(("times new roman"),14),width=16,
                          command=controller.close_app)
        quit_but.place(relx=0.5,rely=0.80,anchor="center")

    #refreshes Addpage, DictPage, RandomPage and QuizPage every time when they become present
    def add_ref(self):
        for obj in gc.get_objects():
            if isinstance(obj, AddPage):
                obj.refresh()
    def dict_update(self):
        for obj in gc.get_objects():
            if isinstance(obj, DictPage):
                obj.dict_control()
    def init_rand(self):
        for obj in gc.get_objects():
            if isinstance(obj, RandomPage):
                obj.initialRandom()
    def init_quiz(self):
        for obj in gc.get_objects():
            if isinstance(obj, QuizPage):
                obj.initialRand()

class AddPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        l1 = Label(self,text="Add Vocabulary",font=(("times new roman"),25,"bold"))
        l1.place(relx=0.5,rely=0.15,anchor="center")

        l2 = Label(self,text="In order to add new vocabulary into your dictionary\nfill in the gaps below",
                   font=(("times new roman"),16,"italic"),fg="gray")
        l2.place(relx=0.5,rely=0.35,anchor="center")

        l3 = Label(self,text="In English",font=(("times new roman"),14))
        l3.place(relx=0.2,rely=0.55,anchor="center")
        ent_eng = Entry(self,width=20,fg="gray",font=(("times new roman"),14,"italic"))
        ent_eng.place(relx=0.2,rely=0.65,anchor="center")
        self.ent_eng=ent_eng

        l4 = Label(self, text="In Pinyin", font=(("times new roman"), 14))
        l4.place(relx=0.5, rely=0.55, anchor="center")
        ent_pin = Entry(self, width=20, fg="gray", font=(("times new roman"), 14, "italic"))
        ent_pin.place(relx=0.5, rely=0.65, anchor="center")
        self.ent_pin = ent_pin

        l5 = Label(self, text="In Hanzi", font=(("times new roman"), 14))
        l5.place(relx=0.8, rely=0.55, anchor="center")
        ent_han = Entry(self, width=20, fg="gray", font=(("times new roman"), 14, "italic"))
        ent_han.place(relx=0.8, rely=0.65, anchor="center")
        self.ent_han=ent_han

        add_but = Button(self,text="Add",font=(("times new roman"), 14),width=16,
                         command=self.add_vocab)
        add_but.place(relx=0.35,rely=0.8,anchor="center")

        mp_but = Button(self,text="Main Page",font=(("times new roman"),14),width=16,
                        command=lambda:controller.show_frame(MainPage))
        mp_but.place(relx=0.65,rely=0.8,anchor="center")

    def refresh(self):
        self.ent_eng.delete(0, END)
        self.ent_pin.delete(0, END)
        self.ent_han.delete(0, END)

    def add_vocab(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT eng FROM dictionary")
        sec = cs.fetchall()
        cont_eng_list = []
        for i in sec:
            i = i[0]
            cont_eng_list.append(i)
        while True:
            x = self.ent_eng.get()
            x = x.lower()
            y = self.ent_han.get()
            z = self.ent_pin.get()
            if not x or not y or not z:
                messagebox.showinfo("Message", "You must fill all of them!")
                db.close()
                break
            elif x in cont_eng_list:
                messagebox.showinfo("Message", f"'{x}' is already in the dictionary...")
                self.refresh()
                db.close()
                break
            else:
                fin = f"INSERT INTO dictionary VALUES('{x}','{y}','{z}')"
                cs.execute(fin)
                db.commit()
                db.close()
                messagebox.showinfo("Message", f"""'{x}-{y}-{z}' is in the dictionary now!""")
                self.refresh()
                break

class DictPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        l1 = Label(self,text="Dictionary",font=(("times new roman"),25,"bold"))
        l1.place(relx=0.5,rely=0.1,anchor="center")

        mp_but = Button(self, text="Main Page", font=(("times new roman"), 14), width=16,
                        command=lambda: controller.show_frame(MainPage))
        mp_but.place(relx=0.5, rely=0.9, anchor="center")

        lb = Listbox(self, width=30)
        lb.place(relx=0.5, rely=0.45, anchor="center")
        self.lb = lb

        dlt_b = Button(self, text="Delete",font=(("times new roman"),14),width=16,
                       command=self.dict_del)
        dlt_b.place(relx=0.5,rely=0.8,anchor="center")

    def dict_del(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        try:
            x = self.lb.get(self.lb.curselection())
            x = x.split("  -  ")
            x = x[0]
            cs.execute(f"DELETE FROM dictionary WHERE eng='{x}'")
            db.commit()
            db.close()
            self.lb.delete("anchor")
        except:
            db.close()
            pass

    def dict_control(self):
        #Burada baba bir performans kaybı var muhtemelen
        self.lb.delete(0,'end')
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT * FROM dictionary ORDER BY eng")
        slc = cs.fetchall()
        for i in slc:
            x = 1
            i = i[0]+"  -  "+i[1]+"  -  "+i[2]
            self.lb.insert(x,i)
            x += 1
        db.close()

class RandomPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        l1 = Label(self,text="Random Vocab",font=(("times new roman"),25,"bold"))
        l1.place(relx=0.5,rely=0.15,anchor="center")

        l2 = Label(self,text="Click the button that you wish to see first,\nthen see the translation and others...",
                   font=(("times new roman"),16,"italic"),fg="gray")
        l2.place(relx=0.5,rely=0.3,anchor="center")

        l3 = Label(self,text="English",font=(("times new roman"),14))
        l3.place(relx=0.2,rely=0.45,anchor="center")
        r1 = Label(self,text="",font=(("times new roman"),14),borderwidth=1,relief="solid",width=20)
        r1.place(relx=0.2,rely=0.52,anchor="center")
        b_eng = Button(self,text="See English first!",font=(("times new roman"),14),width=16,
                       command=lambda: self.first(1))
        self.b_eng=b_eng
        b_eng.place(relx=0.2,rely=0.62,anchor="center")
        self.r1 = r1

        l4 = Label(self, text="Hanzi", font=(("times new roman"), 14))
        l4.place(relx=0.5, rely=0.45, anchor="center")
        r2 = Label(self, text="", font=(14), borderwidth=1, relief="solid", width=20)
        r2.place(relx=0.5, rely=0.52, anchor="center")
        b_han = Button(self, text="See Hanzi first!", font=(("times new roman"), 14),width=16,
                       command=lambda: self.first(2))

        self.b_han = b_han
        b_han.place(relx=0.5, rely=0.62, anchor="center")
        self.r2 = r2

        l5 = Label(self, text="Pinyin", font=(("times new roman"), 14))
        l5.place(relx=0.8, rely=0.45, anchor="center")
        r3 = Label(self, text="", font=(("times new roman"),14), borderwidth=1, relief="solid", width=20)
        r3.place(relx=0.8, rely=0.52, anchor="center")
        b_pin = Button(self, text="See pinyin first!", font=(("times new roman"), 14),width=16,
                       command=lambda: self.first(3))
        self.b_pin = b_pin
        b_pin.place(relx=0.8, rely=0.62, anchor="center")
        self.r3 = r3

        b_others = Button(self, text="See others", font=(("times new roman"), 14),width=16,command=self.see_others)
        b_others.place(relx=0.5, rely=0.72, anchor="center")

        mp_but = Button(self, text="Main Page", font=(("times new roman"), 14),width=16,
                        command=lambda: controller.show_frame(MainPage))
        mp_but.place(relx=0.5, rely=0.9, anchor="center")

    def initialRandom(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT hanzi FROM dictionary ORDER BY RANDOM() LIMIT 1")
        sec = cs.fetchall()
        if not sec:
            messagebox.showinfo("Message", "No vocabulary in the database, please add some into your dictionary...")
            self.r2['text'] = ""
            self.r1['text'] = ""
            self.r3['text'] = ""
        else:
            for i in sec:
                i = i[0]
            self.r1['text'] = ""
            self.r2['text'] = i
            self.r3['text'] = ""
        db.close()

    def first(self,control_num):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT * FROM dictionary")
        control = cs.fetchall()

        if control_num == 1:
            while True:
                x = self.r1['text']
                cs.execute("SELECT eng FROM dictionary ORDER BY RANDOM() LIMIT 1")
                slc = cs.fetchall()
                if not slc:
                    messagebox.showinfo("Message","No vocabulary in the database, please add some into your dictionary...")
                    break
                elif len(control) == 1:
                    messagebox.showinfo("Message","There is only one vocab in your dictionary, please add more...")
                    break
                else:
                    for i in slc:
                        i = i[0]
                    if i == x:
                        continue
                    else:
                        self.r1['text'] = i
                        self.r2['text'] = ""
                        self.r3['text'] = ""
                        db.close()
                        break

        elif control_num == 2:
            while True:
                x = self.r2['text']
                cs.execute("SELECT hanzi FROM dictionary ORDER BY RANDOM() LIMIT 1")
                slc = cs.fetchall()
                if not slc:
                    messagebox.showinfo("Message","No vocabulary in the database, please add some into your dictionary...")
                    break
                elif len(control) == 1:
                    messagebox.showinfo("Message","There is only one vocab in your dictionary, please add more...")
                    break
                else:
                    for i in slc:
                        i = i[0]
                    if i == x:
                        continue
                    else:
                        self.r2['text'] = i
                        self.r1['text'] = ""
                        self.r3['text'] = ""
                        db.close()
                        break

        elif control_num == 3:
            while True:
                x = self.r3['text']
                cs.execute("SELECT pinyin FROM dictionary ORDER BY RANDOM() LIMIT 1")
                slc = cs.fetchall()
                if not slc:
                    messagebox.showinfo("Message","No vocabulary in the database, please add some into your dictionary...")
                    break
                elif len(control) == 1:
                    messagebox.showinfo("Message","There is only one vocab in your dictionary, please add more...")
                    break
                else:
                    for i in slc:
                        i = i[0]
                    if i == x:
                        continue
                    else:
                        self.r3['text'] = i
                        self.r1['text'] = ""
                        self.r2['text'] = ""
                        db.close()
                        break

    def see_others(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        x = self.r1['text']
        y = self.r2['text']
        z = self.r3['text']
        if x == "" and y == "" and z == "":
            messagebox.showinfo("Message", "No vocabulary in the database, please add some into your dictionary...")
        elif x == "" and y == "":
            cs.execute(f"SELECT eng FROM dictionary WHERE pinyin='{z}'")
            slc = cs.fetchall()
            for i in slc:
                i = i[0]
            cs.execute(f"SELECT hanzi FROM dictionary WHERE pinyin='{z}'")
            slc = cs.fetchall()
            for j in slc:
                j = j[0]
            self.r1['text'] = i
            self.r2['text'] = j

        elif x == "" and z == "":
            cs.execute(f"SELECT eng FROM dictionary WHERE hanzi='{y}'")
            slc = cs.fetchall()
            for i in slc:
                i = i[0]
            cs.execute(f"SELECT pinyin FROM dictionary WHERE hanzi='{y}'")
            slc = cs.fetchall()
            for j in slc:
                j = j[0]
            self.r1['text'] = i
            self.r3['text'] = j

        elif y == "" and z == "":
            cs.execute(f"SELECT hanzi FROM dictionary WHERE eng='{x}'")
            slc = cs.fetchall()
            for i in slc:
                i = i[0]
            cs.execute(f"SELECT pinyin FROM dictionary WHERE eng='{x}'")
            slc = cs.fetchall()
            for j in slc:
                j = j[0]
            self.r2['text'] = i
            self.r3['text'] = j

class QuizPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        l1 = Label(self, text="Chinese Quiz", font=(("times new roman"), 25, "bold"))
        l1.place(relx=0.5, rely=0.15, anchor="center")

        l2 = Label(self, text="Test your vocabulary with randomly appearing words in hanzi, english and pinyin",
                   font=(("times new roman"), 16, "italic"), fg="gray")
        l2.place(relx=0.5, rely=0.3, anchor="center")

        l3 = Label(self, text="Select the corresponding...", font=(("times new roman"), 14, "italic"))
        l3.place(relx=0.25, rely=0.45, anchor="center")

        l_q = Label(self, text="", font=(("times new roman"), 16, "bold"), borderwidth=1, relief="solid", width=20)
        l_q.place(relx=0.25, rely=0.55, anchor="center")
        self.l_q = l_q

        l4 = Label(self, text="Answer is...", font=(("times new roman"), 14, "italic"))
        l4.place(relx=0.75, rely=0.45, anchor="center")

        l_ans = Label(self, text="", font=(("times new roman"), 16, "bold"), borderwidth=1,
                    relief="solid", width=20)
        l_ans.place(relx=0.75, rely=0.55, anchor="center")
        self.l_ans = l_ans

        l_check = Label(self, text="", font=(("times new roman"), 14), fg="green")
        l_check.place(relx=0.75, rely=0.7, anchor="center")
        self.l_check = l_check

        next_but = Button(self, text="Next", font=(("times new roman"), 14), width=16,
                          command=self.skip)
        next_but.place(relx=0.5, rely=0.8, anchor="center")

        mp_but = Button(self, text="Main Page", font=(("times new roman"), 14), width=16,
                        command=lambda: controller.show_frame(MainPage))
        mp_but.place(relx=0.5, rely=0.9, anchor="center")

        but1 = Button(self, text="", font=(("times new roman"), 14), width=16, command=lambda: self.checker(1))
        but1.place(relx=0.5, rely=0.45, anchor="center")
        self.but1 = but1

        but2 = Button(self, text="", font=(("times new roman"), 14), width=16, command=lambda: self.checker(2))
        but2.place(relx=0.5, rely=0.55, anchor="center")
        self.but2 = but2

        but3 = Button(self, text="", font=(("times new roman"), 14), width=16, command=lambda: self.checker(3))
        but3.place(relx=0.5, rely=0.65, anchor="center")
        self.but3 = but3

    def initialRand(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT COUNT(*) FROM dictionary")
        kont = cs.fetchall()
        for i in kont:
            i = i[0]
        print(i,type(i))
        if i < 4:
            messagebox.showinfo("Message", "Not enough vocabulary in the database, please add some into your dictionary...")
            self.l_q['text'] = ''
            self.l_ans['text'] = ''
            self.l_check['text'] = ''
            self.but1['text'] = ''
            self.but2['text'] = ''
            self.but3['text'] = ''
        else:
            sec = ['hanzi','eng','pinyin']
            s = random.randint(0,2)
            sec1 = sec[s]
            sec.remove(sec1)
            s = random.randint(0, 1)
            sec2 = sec[s]
            cs.execute(f"SELECT {sec1} FROM dictionary ORDER BY RANDOM() LIMIT 1")
            ques = cs.fetchall()
            for i in ques:
                ques = i[0]
            cs.execute(f"SELECT {sec2} FROM dictionary WHERE {sec1}='{ques}'")
            key = cs.fetchall()
            for i in key:
                key = i[0]
            print(key)
            answers = [key, ]
            
            while len(answers) < 3:
                while True:
                    cs.execute(f"SELECT {sec2} FROM dictionary ORDER BY RANDOM() LIMIT 1")
                    sec = cs.fetchall()
                    for i in sec:
                        i = i[0]
                    if i  in answers:
                        continue
                    else:
                        answers.append(i)
                        break
            self.l_q['text'] = ques
            s = random.randint(0,2)
            ran1 = answers[s]
            self.but1['text'] = ran1
            answers.remove(ran1)
            s = random.randint(0,1)
            ran2 = answers[s]
            self.but2['text'] = ran2
            answers.remove(ran2)
            self.but3['text'] = answers[0]

    def skip(self):
        db = sql.connect('eng-chi.db')
        cs = db.cursor()
        cs.execute("SELECT COUNT(*) FROM dictionary")
        kont = cs.fetchall()
        for i in kont:
            i = i[0]
        if i < 4:
            messagebox.showinfo("Message", "Not enough vocabulary in the database, please add some into your dictionary...")
        else:
            self.initialRand()
            self.l_ans['text'] = ''
            self.l_check['text'] = ''

    def checker(self,connum):
        if self.l_check['text'] == 'correct!' or self.l_check['text'] == 'incorrect!':
            self.l_check['text'] = self.l_check['text'] + '\nyou have already selected one...'
        elif self.l_check['text'] == '':
            db = sql.connect('eng-chi.db')
            cs = db.cursor()
            liste = ['hanzi', 'eng', 'pinyin']
            ques = self.l_q['text']
            prospect = []
            for i in liste:
                cs.execute(f"SELECT * FROM dictionary WHERE {i}='{ques}'")
                sec = cs.fetchall()
                if not sec:
                    pass
                else:
                    x = 0
                    for j in range(3):
                        for k in sec:
                            print(type(k))
                            y = k[x]
                            print(x)
                            prospect.append(y)
                            x += 1
            print(prospect)
            prospect.remove(ques)
            if self.but1['text'] == prospect[0] or self.but2['text'] == prospect[0] or self.but3['text'] == prospect[0]:
                key = prospect[0]
            elif self.but1['text'] == prospect[1] or self.but2['text'] == prospect[1] or self.but3['text'] == prospect[1]:
                key = prospect[1]

            if connum == 1:
                if self.but1['text'] == key:
                    self.l_ans['text'] = key
                    self.l_check['text'] = "correct!"
                    self.l_check['fg'] = 'green'
                else:
                    self.l_ans['text'] = key
                    self.l_check['text'] = 'incorrect!'
                    self.l_check['fg'] = 'red'

            elif connum == 2:
                if self.but2['text'] == key:
                    self.l_ans['text'] = key
                    self.l_check['text'] = "correct!"
                    self.l_check['fg'] = 'green'
                else:
                    self.l_ans['text'] = key
                    self.l_check['text'] = 'incorrect!'
                    self.l_check['fg'] = 'red'

            elif connum == 3:
                if self.but3['text'] == key:
                    self.l_ans['text'] = key
                    self.l_check['text'] = "correct!"
                    self.l_check['fg'] = 'green'
                else:
                    self.l_ans['text'] = key
                    self.l_check['text'] = 'incorrect!'
                    self.l_check['fg'] = 'red'


initial_db()
app = App()
app.geometry("700x300")
app.title("Exercise Chinese")
app.resizable(0,0)
app.mainloop()












