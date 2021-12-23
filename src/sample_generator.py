import os

from PIL import Image
import numpy as np
import pandas as pd


def gen_csv(root="../tile_masks", verbose=0):
    df = pd.DataFrame(
        columns=[
            "tile_name",
            "case_index",
            "label_0",
            "label_1",
            "label_2"])
    for case in os.listdir(root):
        case_ind = case
        npy = "/npy"
        tiles = "/tiles"
        for tile in os.listdir(root + '/' + case + tiles):
            tile_name = tile.removesuffix('.png')
            x = np.load(
                root +
                "/" +
                case +
                npy +
                "/" +
                tile_name +
                "_mask.npy")
            d = {0: (x == 0).sum(), 1: (x == 1).sum(), 2: (x == 2).sum()}
            label_0 = d[0] / sum(d.values())
            label_1 = d[1] / sum(d.values())
            label_2 = d[2] / sum(d.values())
            df = df.append({'tile_name': tile_name,
                            "case_index": case_ind,
                            "label_0": label_0,
                            "label_1": label_1,
                            "label_2": label_2},
                           ignore_index=True)
            if verbose:
                print(tile_name)

    df.to_csv("tile_masks.csv", index=False)
    return df


def gen_png(df, root="../tile_masks", sample_size=100,
            out_dir="sample", rule_0=0.99, rule_1=0.5, rule_2=0.1):

    df["label"] = np.nan
    df.loc[df.label_0 > rule_0, 'label'] = 0
    df.loc[df.label_1 > rule_1, 'label'] = 1
    df.loc[df.label_2 > rule_2, 'label'] = 2
    df_sample = pd.DataFrame()

    for i in range(3):
        rd = df.loc[df.label == i]
        rd = rd.iloc[np.random.choice(
            len(rd.index.tolist()), sample_size, replace=False)]
        rd["path"] = out_dir + "/%d/" % i + rd.tile_name + ".png"

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        for case, tile in rd.loc[:, ["case_index", "tile_name"]].values:
            if not os.path.exists(out_dir + "/%d" % i):
                os.mkdir(out_dir + "/%d" % i)
            img = Image.open(root + '/' + case + "/tiles/" + tile + ".png")
            img.save(out_dir + "/%d/" % i + tile + ".png")
        df_sample = pd.concat([df_sample, rd])
    df_sample.to_csv(out_dir + "/" + out_dir + ".csv", index=False)


def main():
    # df = gen_csv(root = "../tile_masks")
    df = pd.read_csv("tile_mask.csv")
    gen_png(df=df, sample_size=100)


if __name__ == "__main__":
    main()
