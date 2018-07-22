# Command Line Version of the UI

### Opens to Main Menu
 # Select one of the categories (each has own config file)
    # List % Complete
    # Rate
     # Select 1 of the two things that you like better
     # Go Back Button
    # See Ranking
     # Go Back Button
     # Option to see for other ranks
    # Configure
     # Configuration options
     # Save Button
    # View all items
    # Go Back button

from UI import UI

class CLI_UI(UI):
    def __init__(self):
        UI.__init__(self)

    def select_category(self):
        choices = [str(i) for i in range(len(self.availableCategories))]
        for i in choices:
            print("{}) {}".format(i, self.availableCategories[int(i)]))
        x = input("Select a category: ")
        if x not in choices:
            return self.select_category()
        return self.availableCategories[int(x)]

    def rank_2(self, x1, x2):
        print("##############################")
        print("#enter 1 or 2 or undo or back#")
        print("##############################")
        ans = input("{}\nor\n{}\n".format(x1["name"], x2["name"]))
        if ans == "-1":
            return -1
        if ans == "u":
            return "undo"
        if ans in ["1", "2"]:
            return [x1,x2][int(ans)-1]
        print("Invalid input")
        return self.rank_2(x1, x2)

    def printRank(self, ranks):
        for rank in ranks:
            print("{}: {}".format(rank[1], rank[0]))

if __name__ == "__main__":
    ui = CLI_UI()