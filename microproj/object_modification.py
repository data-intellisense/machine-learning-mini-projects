# this script demonstrates that the changes when functions operates on mutable objects such as
# list and dataframe will reflect on the original object
# A common misconception is that if an object with the same name created within
# the function, then changes on the same name object will Not be reflected on original object!!!


def revise_list(example_list, method=1):

    # a new object is created, even though the name is 'example_list'
    # it is different from the 'example_list' of the function input
    # therefore the original 'example_list' does not point to the 'example_list'
    # in the funciton
    if method == 1:
        example_list = [2, 2]

    # Method 2:
    # this operates on the original 'example_list' object
    # which will change
    elif method == 2:
        example_list[0] = 2


example_list = [1, 2]

revise_list(example_list, method=1)
print(example_list)  # result: [1, 2]

revise_list(example_list, method=2)
print(example_list)  # result: [2, 2]

import pandas as pd


def revise_df(example_df, method=1):

    # a new object is created, even though the name is 'example_df'
    # it is different from the 'example_df' of the function input
    # therefore the original 'example_df' does not point to the 'example_df'
    # in the funciton, any changes on the new example_df won't be reflected on the
    # original 'example_df'
    if method == 1:
        example_df = pd.DataFrame([2, 2])
        example_df.index = [0, 1]

    # Method 2:
    # this operates on the original 'example_df' object
    # which will change original 'example_df'
    elif method == 2:
        # example_df.iat[0, 0] = 2
        example_df.reset_index(inplace=True, drop=True)


example_df = pd.DataFrame([1, 2], index=["a", "b"])
example_df.set_index(keys=0)

revise_df(example_df, method=1)
print(example_df)

revise_df(example_df, method=2)
print(example_df)
