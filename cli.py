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

    def rank_2_menu(self, x1, x2):
        print("##############################")
        print("#enter 1 or 2 or undo or back#")
        print("##############################")
        ans = input("{}\nor\n{}\n".format(x1["name"], x2["name"]))
        if ans in ['b','back']:
            return -1
        if ans == "u" or ans == "undo":
            return "undo"
        if ans in ["1", "2"]:
            return int(ans)-1
        print("Invalid input")
        return self.rank_2_menu(x1, x2)

    def category_menu(self):
        numRates = self.category.getNumRates()
        totalRates = self.category.getTotalRates()
        print("{}. {}% Complete ({} Rates Left)".format(self.category.getName(), int((numRates/totalRates)*100), totalRates-numRates))
        options = ['rate', 'rank', 'config', 'view', 'back']
        orange = [str(i) for i in range(len(options))]
        for i in orange:
            print("{}) {}".format(i, options[int(i)]))
        action = input("What would you like to do? ")
        if action not in orange:
            return self.category_menu()
        return options[int(action)]

    def rank_items_menu(self):
        algs = self.category.getAvailableRankers()
        chosen_alg = algs[0]
        while 1:
            ranking = self.category.rankWith(chosen_alg)
            ordered_names = sorted(ranking.keys(), key=lambda k: ranking[k])
            print("{}:".format(chosen_alg.name))
            for r in range(len(ordered_names)):
                print("{}) {} ({})".format(len(ordered_names)-(r),ordered_names[r], ranking[ordered_names[r]]))
            print("##############")
            options = [str(i) for i in range(len(algs))]
            for a in options:
                print("{}) {}".format(a, algs[int(a)].name))
            inp = input('Rank By which?\n')
            if inp not in options:
                return
            print(inp)
            print(algs[int(inp)])
            chosen_alg = algs[int(inp)]

    def config_menu(self, config):
        while 1:
            config_keys = list(config.keys())
            options = [str(i) for i in range(len(config_keys))]
            for i in options:
                print("{}) {} ({})".format(i, config_keys[int(i)], config[config_keys[int(i)]]["value"]))
            o = input("Pick option you want to modify, or exit\n")
            if o in ['e', 'exit']:
                return config
            if o in options:
                opt = config_keys[int(o)]
                if config[opt]["type"] == bool:
                    options = ["true", "false"]
                else:
                    options = config[opt]["type"]
                n = input("Pick {}\n".format(",".join(options)))
                if n in options:
                    config[config_keys[int(o)]]["value"] = n

    def view_items(self):
        for item in sorted(map(lambda i: i['name'], self.category.items)):
            print(item)

if __name__ == "__main__":
    ui = CLI_UI()