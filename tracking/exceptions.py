class NameNotUniqueInCategory(Exception):
    def __init__(self):
        msg = "There is already a Trackable in this category that has this name."
        super().__init__(msg)

class NameNotUniqueInUserCategories(Exception):
    def __init__(self):
        msg = "User already has a Category with this name."
        super().__init__(msg)