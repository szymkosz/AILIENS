class Widget:
    def __init__(self, recipe):
        self.recipe = recipe.upper()    ## Case insensitive
        self.manufactured = False
        self.progress = ""

    def __str__(self):
        return self.progress

    def __repr__(self):
        return self.recipe

    ## Attempts to add a component to the widget. Returns a boolean indicating
    #   if building was successful.
    def build(self, char):
        char = char[0].upper()      ## Truncate to first char
        if not self.manufactured:
            if char == recipe[len(progress)]:
                progress += char
                if recipe == progress:
                    self.manufactured = True
                return True
        return False
