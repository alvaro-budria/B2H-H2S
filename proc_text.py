import argparse
import pickle

import torch
import clip

TEXT_PATHS = {
    "train": "/mnt/gpid08/datasets/How2Sign/How2Sign/utterance_level/train/text/en/raw_text/train.text.id.en",
    "val": "/mnt/gpid08/datasets/How2Sign/How2Sign/utterance_level/val/text/en/raw_text/val.text.id.en",
    "test": "/mnt/gpid08/datasets/How2Sign/How2Sign/utterance_level/test/text/en/raw_text/test.text.id.en"
}


device = "cuda" if torch.cuda.is_available() else "cpu"

sentences = ['This framework generates embeddings for each input sentence',
             'Sentences are passed as a list of string.', 
             'The quick brown fox jumps over the lazy dog.',
             "Esta frase está escrita en español",
             "Aquesta frase és en català."]

sample_data = ["fyI1Ev5m1w4_12-8-rgb_front And then you would start to turn your pile.",
               "fyI1Ev5m1w4_13-8-rgb_front You would take the top and you would put it on the bottom, just like this.",
               "fyI1Ev5m1w4_2-8-rgb_front Because, if you layered it right, and you watered it right, and you got your microorganisms in there, and you put the compost inoculate in there, you shouldn't have to turn this pile.",
               "fyI1Ev5m1w4_3-8-rgb_front Now, obviously, this is a brand new pile that we just made today.",
               "fyI1Ev5m1w4_4-8-rgb_front But, if for some reason your pile didn't cook down, which means if your pile is four feet high, when it's finished it should be about a foot and a half high.",
               "fyI1Ev5m1w4_5-8-rgb_front And it should cook down, and it should go down, and you should be able to see that it looks like compost, not like this material.",
               "fyI1Ev5m1w4_6-8-rgb_front But if you come across your pile, and it hasn't done those things, then you're going to want to turn your pile.",
               "fyI1Ev5m1w4_7-8-rgb_front The way we would do that is we would do just like we did in the beginning.",
               "fyI1Ev5m1w4_8-8-rgb_front We would put holes in the ground so it would drain good.",
               "fyI1Ev5m1w4_9-8-rgb_front We would create--add some more sticks, which we've run out of"]


def load_text(key, ids):
    file_path = TEXT_PATHS[key]
    dict_text = {}
    with open(file_path) as fp:
        for line in fp:
            id, text = line.split(" ", 1)  # first space separates id from text
            if id in ids:
                dict_text[id] = text
    # sentence_list = [v for _, v in sorted(dict_text.items())]  # it's important that the result is sorted by clip ID
    sentence_list = [v for _, v in dict_text.items()]  # it's important that the result is already sorted by clip ID
    print(f"len(sentence_list): {len(sentence_list)}", flush=True)
    return sentence_list


# obtain embeddings for each sentence in the input list
def obtain_embeddings(key, ids):
    model, _ = clip.load('ViT-B/32', device)
    # Calculate features
    sentence_list = load_text(key, ids)
    sentence_tensor = torch.cat([clip.tokenize(sent, truncate=True) for sent in sentence_list]).to(device)
    with torch.no_grad():
        embeddings = model.encode_text(sentence_tensor)
    return embeddings.numpy()


# returns the ID of those clips for which text is available
def get_clip_ids(key="test"):
    file_path = TEXT_PATHS[key]
    id_list = []
    with open(file_path) as fp:
        for line in fp:
            id, text = line.split(" ", 1)  # first space separates id from text
            id_list.append(id)
    return id_list


def process_text(subset=0.005):
    for key in TEXT_PATHS:
        sentence_list = load_text(key)
        idx_max = int(len(sentence_list)*subset)
        print(f"idx_max: {idx_max}", flush=True)
        sentence_list = sentence_list[0:idx_max]
        sentence_tensor = torch.cat([clip.tokenize(sent, truncate=True) for sent in sentence_list]).to(device)

        print(sentence_tensor.shape, flush=True)
        embeddings = obtain_embeddings(sentence_tensor)
        print(embeddings.shape, flush=True)
        # #Store sentences & embeddings on disk
        with open(f'video_data/{key}_sentence_embeddings.pkl', "wb") as fOut:
            pickle.dump(embeddings.numpy(), fOut, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'video_data/{key}_sentence_raw.pkl', "wb") as fOut:
            pickle.dump(sentence_list, fOut, protocol=pickle.HIGHEST_PROTOCOL)
        print("Saved sentence embeddings.", flush=True)


if __name__=="__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--file_path', type=str, default="/mnt/gpid08/datasets/How2Sign/How2Sign/utterance_level/test/text/en/raw_text/test.text.id.en", help="path to the file where text dataset is located")
    # args = parser.parse_args()

    process_text()
