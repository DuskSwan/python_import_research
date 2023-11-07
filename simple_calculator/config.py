class cfg:
    def __init__(self):
        self.name = "simple_calculator"
        self.version = "1.0.0"
        self.author = "Zhang San"
    def show_info(self):
        print("This is class cfg")
        print("The calculator's name is " + self.name\
            + ", version is " + self.version\
            + ", author is " + self.author)