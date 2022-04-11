import os
import json
import pwinput

json_files = "json"
if not os.path.exists(json_files):
    os.mkdir(json_files)

admin_logon = "_admin"
os.chdir(json_files)
logged = ["", False]
on_commands = ["list", "nav", "back", "logoff", "read", "mkdir", "mkvl", "edit", "del", "copy", "paste", "rename", "save"]
off_commands = ["login", "register", "help"]
admin_commands = ["nav", "back", "logoff", "read", "mkdir", "mkvl", "edit", "del", "copy", "paste", "listusers", "exit", "delete"]

cript = {
    "N": "a",
    "p": "b",
    "h": "c",
    "d": "d",
    "*": "e",
    "2": "f",
    "=": "g",
    "!": "h",
    "y": "i",
    "&": "j",
    "{": "k",
    "z": "l",
    "3": "m",
    "t": "n",
    "k": "o",
    "4": "p",
    "~": "q",
    "$": "r",
    "S": "s",
    ",": "t",
    "I": "u",
    "8": "v",
    "X": "w",
    "g": "x",
    "K": "y",
    "n": "z",
    "U": "0",
    ".": "1",
    "%": "2",
    "q": "3",
    "@": "4",
    "_": "5",
    "Y": "6",
    "0": "7",
    "P": "8",
    "R": "9",
    "u": "A",
    "w": "B",
    "<": "C",
    "O": "D",
    "J": "E",
    "c": "F",
    "W": "G",
    "/": "H",
    "(": "I",
    "s": "J",
    "5": "K",
    "7": "L",
    "l": "M",
    "e": "N",
    "D": "O",
    "M": "P",
    "+": "Q",
    "A": "R",
    "j": "S",
    "a": "T",
    "H": "U",
    "b": "V",
    "L": "W",
    "V": "X",
    ")": "Y",
    "^": "Z",
    ";": "~",
    "?": "!",
    "G": "@",
    "x": "#",
    "6": "$",
    "o": "%",
    "Q": "^",
    ":": "&",
    "1": "*",
    "B": "(",
    "E": ")",
    "'": "_",
    "-": "+",
    ">": "-",
    "f": "=",
    "m": "{",
    "v": "}",
    "#": "|",
    "Z": ":",
    "}": ";",
    "r": "'",
    "C": ",",
    "|": "<",
    "9": ".",
    "F": ">",
    "T": "/",
    "i": "?",
    "\n": "\n",
    "¨": "\\",
    "\\": "¨"
}  # file encriptation


class Nav:
    def __init__(self, initialdir="main"):
        self.initialdir = initialdir
        self.dir = self.initialdir
        self.separator = "/"
        self.backdir = ".."
        self.backinitialdir = "."
        self.savefile = ".s"
        self.copy_paste = ["", {}]

        self.folders_dict = None

    def decrypt(self):
        folders = open("folders.json", "rt")
        decript = folders.read()
        decripted = ""

        exceptions = ['"', " "]

        for letter in decript:
            if letter in cript:
                decripted += cript[letter]
            elif letter in exceptions:
                decripted += letter

        folders_dict = json.loads(decripted)
        folders.close()
        self.folders_dict = folders_dict

    @staticmethod
    def encrypt(json_dict):
        folders = open("folders.json", "wt")
        encript = str(json_dict).replace("'", '"')
        encripted = ""

        values = list(cript.values())
        keys = list(cript.keys())

        exceptions = ['"', " "]

        for letter in encript:
            if letter in values:
                encripted += keys[values.index(letter)]
            elif letter in exceptions:
                encripted += letter

        folders.write(encripted)
        folders.close()

    def list_files(self):
        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                for file in dic:
                    if type(dic[file]) == dict:
                        print(f"[FOLDER] {file[0:40]}")
                    elif type(dic[file]) == str:
                        print(f"[VALUE]  {file[0:40]}")

                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

    def back(self):
        if len(self.dir.split(self.separator)) > 1:
            listdir = self.dir.split(self.separator)
            del listdir[-1]
            self.dir = self.separator.join(listdir)

    def nav(self, foldername):
        if foldername == "":
            return

        if foldername == self.backdir:
            self.back()
            return None
        elif foldername == self.backinitialdir:
            self.dir = self.initialdir
            return None

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                if foldername not in dic:
                    for name in dic:
                        if name.startswith(foldername):
                            if type(dic[name]) != dict:
                                print("Nao e possivel navegar em um valor")
                                return None

                            self.dir += f"{self.separator}{name}"
                            return None

                    print("Pasta nao existe")
                    return None

                if type(dic[foldername]) != dict:
                    print("Nao e possivel navegar em um valor")
                    return None

                self.dir += f"{self.separator}{foldername}"
                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

    def read(self, filename):
        if filename == "":
            return

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                if filename in dic:
                    print("# CONTENT")
                    print(dic[filename])

                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

    def mkdir(self, foldername):
        if foldername == "":
            return

        # -------------
        files = []

        def getfiles(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                for file in dic:
                    files.append(file)

                return None

            getfiles(di, dic[dirs[b]], b + 1)

        getfiles(self.dir, self.folders_dict)

        if foldername in files:
            question = input(f"Ja existe uma pasta/arquivo chamada(o) '{foldername}'. Gostaria de substituir? (s, n) ").lower()
            if question == "n":
                return None

        # -------------

        def getfolders(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                dic[foldername] = {}
                return None

            getfolders(di, dic[dirs[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)

    def mktxt(self, filename):
        if filename == "":
            return

        # -------------
        files = []

        def getfiles(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                for folder in dic:
                    files.append(folder)

                return None

            getfiles(di, dic[dirs[b]], b + 1)

        getfiles(self.dir, self.folders_dict)

        if filename in files:
            question = input(f"Ja existe uma pasta/arquivo chamada(o) '{filename}'. Gostaria de substituir? (s, n) ").lower()
            if question == "n":
                return None

        # -------------

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                dic[filename] = ""
                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)

    def edit(self, filename):
        if filename == "":
            return

        lines = []

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                print("# -------------CONTENT")
                print(dic[filename])

                print(f"# -------------EDIT (Type '{self.savefile}' to save)")
                while True:
                    edit = input()
                    if edit == self.savefile:
                        break

                    lines.append(edit)

                dic[filename] = "\n".join(lines)
                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)

    def delvl(self, filename):
        if filename == "":
            return

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                del dic[filename]
                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)

    def copy(self, vl):
        if vl == "":
            return

        def getfolders(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                try:
                    self.copy_paste[0] = vl
                    self.copy_paste[1] = dic[vl]
                except KeyError:
                    print("Valor nao existe no diretorio atual")

                return None

            getfolders(di, dic[dirs[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

    def paste(self):
        if self.copy_paste[0] == "":
            return None

        # -------------
        files = []

        def getfiles(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                for f in dic:
                    files.append(f)

                return None

            getfiles(di, dic[dirs[b]], b + 1)

        getfiles(self.dir, self.folders_dict)

        if self.copy_paste[0] in files:
            question = input(f"Ja existe uma pasta/arquivo chamada(o) '{self.copy_paste[0]}'. Gostaria de substituir? (s, n) ").lower()
            if question == "n":
                return None

        # -------------

        def getfolders(di, dic, b=0):
            dirs = di.split(self.separator)

            if b == len(dirs):
                dic[self.copy_paste[0]] = self.copy_paste[1]
                return None

            getfolders(di, dic[dirs[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)

    def rename(self, filename):
        if filename == "":
            return

        def getfolders(di, dic, b=0):
            folder = di.split(self.separator)

            if b == len(folder):
                if filename not in dic:
                    print("Valor nao existe no diretorio atual")
                    return None

                print(f"ORIGINAL > {filename}")
                new_name = input("NEW > ")
                content = dic[filename]

                del dic[filename]
                dic[new_name] = content
                del content

                return None

            getfolders(di, dic[folder[b]], b + 1)

        getfolders(self.dir, self.folders_dict)

        self.encrypt(self.folders_dict)


nav = Nav("main")


class Loggon:
    @staticmethod
    def decrypt(plain_text):
        if plain_text == "":
            return ""

        decripted = ""

        exceptions = ['"', " "]

        for letter in plain_text:
            if letter in cript:
                decripted += cript[letter]
            elif letter in exceptions:
                decripted += letter

        return decripted

    @staticmethod
    def encrypt(plain_text):
        if plain_text == "":
            return ""

        values = list(cript.values())
        keys = list(cript.keys())
        encripted = ""

        exceptions = ['"', " "]

        for letter in plain_text:
            if letter in values:
                encripted += keys[values.index(letter)]
            elif letter in exceptions:
                encripted += letter

        return encripted

    @staticmethod
    def register():
        print("[Register]")

        users = os.listdir()
        username = input("Username: ").lower()

        if username in users:
            print("Usuario ja existe")
            return None

        password = input("Password: ")
        login_dict = {
            "user": username,
            "pass": Loggon.encrypt(password)
        }

        os.mkdir(username)
        os.chdir(username)

        with open("login.json", "w") as file:
            json.dump(login_dict, file, indent=4)
            file.close()

        with open("folders.json", "w") as folder:
            template = {
                "main": {
                }
            }
            json.dump(template, folder, indent=4)
            folder.close()

        os.chdir("..")

    @staticmethod
    def login():
        users = os.listdir()
        if len(users) < 1:
            print("Nenhuma conta salva")
            return None

        print("[Login]")
        username = input("Username: ").lower()

        if username not in users:
            print("Usuario nao existe")
            return False

        os.chdir(username)
        file = open("login.json", "r")
        login_dict = json.load(file)

        if login_dict["pass"] == "":
            logged[0] = username
            return True

        decripted_password = Loggon.decrypt(login_dict["pass"])
        for x in range(3):
            password = pwinput.pwinput(prompt=f"Password[{x + 1}]: ", mask="*")
            if password == decripted_password:
                logged[0] = username
                nav.decrypt()
                return True

        print(f"{x + 1}/3 Erros")
        file.close()
        os.chdir("..")
        return False

    @staticmethod
    def logoff():
        global logged
        print(f"Deslogado de '{logged[0]}'")
        logged = ["", False]
        nav.dir = nav.initialdir
        os.chdir("..")

    # admin is not done yet
    @staticmethod
    def admin():
        global logged

        print("This is a special admin zone")
        print("Help for commands")
        logged[0] = "admin"

        while True:
            admin = input(f"{logged[0]} : {nav.dir}> ")

            admin_args = admin.split()
            os.system("cls")

            # exit command
            if admin == admin_commands[11]:
                logged[0] = ""
                return None

            # delete command
            if admin == admin_commands[12] and not logged[1]:
                user = admin_args[1::]
                if user in os.listdir():
                    os.remove(" ".join(user))
            elif admin == admin_commands[12] and logged[1]:
                print("Logoff first (logoff)")

            # list users command
            if admin == admin_commands[10]:
                print("## Users List")
                for x in os.listdir():
                    with open(f"{x}\\login.json") as f:
                        print(f"{x} - {json.load(f)['pass']}")
                        f.close()
                print("## --")

            # login command
            if admin == off_commands[0]:
                print("## Users List")
                for x in os.listdir():
                    with open(f"{x}\\login.json") as f:
                        print(f"{x} - {json.load(f)['pass']}")
                        f.close()
                print("## --")

                user = input(f"{logged[0]}> ")
                os.system("cls")

                if user in os.listdir():
                    logged = [user, True]
                    os.chdir(user)
                    nav.decrypt()
                else:
                    print("User does not exist")

            # register command
            if admin == off_commands[1]:
                Loggon.register()

            # admin help command
            if admin == admin_commands[0]:
                [print(x) for x in admin_commands]
                [print(x) for x in off_commands]

            # on commands
            try:
                if admin_args[0].lower() in admin_commands and logged[1]:
                    # nav command
                    if admin_args[0] == admin_commands[0]:
                        nav.nav(" ".join(admin_args[1::]))

                    # back command
                    if admin == admin_commands[1]:
                        nav.back()

                    # read command
                    if admin_args[0] == admin_commands[3]:
                        nav.read(" ".join(admin_args[1::]))

                    # mkdir command
                    if admin_args[0] == admin_commands[4]:
                        nav.mkdir(" ".join(admin_args[1::]))

                    # mktxt command
                    if admin_args[0] == admin_commands[5]:
                        nav.mktxt(" ".join(admin_args[1::]))

                    # edit command
                    if admin_args[0] == admin_commands[6]:
                        nav.edit(" ".join(admin_args[1::]))

                    # del command
                    if admin_args[0] == admin_commands[7]:
                        nav.delvl(" ".join(admin_args[1::]))

                    # copy command
                    if admin_args[0] == admin_commands[8]:
                        nav.copy(" ".join(admin_args[1::]))

                    # paste command
                    if admin == admin_commands[9]:
                        nav.paste()

                    # logoff command
                    if admin == admin_commands[2]:
                        print(f"Logged off from '{logged[0]}'")
                        logged = ["admin", False]
                        nav.dir = nav.initialdir
                        os.chdir("..")

                elif admin_args[0] in on_commands and not logged[1] is False:
                    print("Usuario nao logado")
            except IndexError:
                pass

            # if logged: list directory
            if logged[1]:
                nav.list_files()
            else:
                os.listdir()


print("'help' Para mostrar os comandos")
while True:
    if logged[0] == "":
        a = input(f"{nav.dir}> ")
    else:
        a = input(f"{logged[0]} : {nav.dir}> ")

    args = a.split()
    os.system("cls")

    if a == admin_logon:
        Loggon().admin()

    # login command
    if a == off_commands[0]:
        if Loggon.login():
            logged[1] = True
            os.system("cls")

    # register command
    if a == off_commands[1] and logged[1] is False:
        Loggon.register()
    elif a == off_commands[1] and logged[1]:
        print("Usuario deve estar deslogado para se registrar (logoff)")

    # help command
    if a == off_commands[2]:
        print("On Commands:")
        [print(on) for on in on_commands]

        print("\nOff Commands:")
        [print(off) for off in off_commands]

    # on commands
    try:
        if args[0].lower() in on_commands and logged[1]:
            # nav command
            if args[0] == on_commands[1]:
                nav.nav(" ".join(args[1::]))

            # back command
            if a == on_commands[2]:
                nav.back()

            # read command
            if args[0] == on_commands[4]:
                nav.read(" ".join(args[1::]))

            # mkdir command
            if args[0] == on_commands[5]:
                nav.mkdir(" ".join(args[1::]))

            # mktxt command
            if args[0] == on_commands[6]:
                nav.mktxt(" ".join(args[1::]))

            # edit command
            if args[0] == on_commands[7]:
                nav.edit(" ".join(args[1::]))

            # del command
            if args[0] == on_commands[8]:
                nav.delvl(" ".join(args[1::]))

            # copy command
            if args[0] == on_commands[9]:
                nav.copy(" ".join(args[1::]))

            # paste command
            if a == on_commands[10]:
                nav.paste()

            # rename command
            if args[0] == on_commands[11]:
                nav.rename(" ".join(args[1::]))

            # logoff command
            if a == on_commands[3]:
                Loggon.logoff()

            # save command
            if a == on_commands[12]:
                nav.encrypt(nav.folders_dict)
        elif args[0] in on_commands and not logged[1] is False:
            print("Usuario nao logado")
    except IndexError:
        pass

    # if logged: list directory
    if logged[1]:
        nav.list_files()
