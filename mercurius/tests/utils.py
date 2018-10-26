
def compare_unordered_lists(view, list1, list2):
    view.assertTrue(set(list1) == set(list2))
