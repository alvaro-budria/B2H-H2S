import csv
from collections import Counter
import pandas as pd


CATEG_PATHS = {
    "train": "/mnt/gpid08/datasets/How2Sign/metadata/How2Sign/categories/categories/videoID_categoryID_train.csv",
    "val": "/mnt/gpid08/datasets/How2Sign/metadata/How2Sign/categories/categories/videoID_categoryID_val.csv",
    "test": "/mnt/gpid08/datasets/How2Sign/metadata/How2Sign/categories/categories/videoID_categoryID_test.csv"
}

MAP_ID_CATEG_PATH = "/mnt/gpid08/datasets/How2Sign/metadata/How2Sign/categories/categories/categoryName_categoryID.csv"


# returns a dict mapping an id (11 chars) to its category ([1-9])
def get_ids_categ(key, skip_header=True):
    file_path = CATEG_PATHS[key]
    reader = csv.reader(open(file_path))
    if skip_header:
        header = next(reader)  # skip header
    id_categ_dict = {}  # key: id, value: category ([1-9])
    for row in reader:
        key = row[0]
        if key not in id_categ_dict:
            id_categ_dict[key] = int(row[1])
    return id_categ_dict


# given a list clip_names of clip names, and a mapping id_categ_dict {id: category}
# returns a list of categories with same length as clip_ids
# notice the mapping from a clip to a category is implicit, and assumes clip_names and categ_list follow the same order
def get_clips_categ(clip_names, id_categ_dict):
    categ_list = []
    for clip_name in clip_names:
        clip_id = clip_name[:11]  # first 11 characters are the id
        categ_list.append(id_categ_dict[clip_id])
    return categ_list


def plot_barChart_categs(categs):
    count = Counter(categs)
    df = pd.DataFrame.from_dict(count, orient='index')
    ax = df.plot(kind='bar', title=f"Examples per class in {set} set")
    fig = ax.get_figure()
    fig.savefig(f"barChart_classes_{set}.png")
    print(f"*** Generated barChart_classes_{set}.png ***", flush=True)
