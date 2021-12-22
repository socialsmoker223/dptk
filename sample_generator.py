import pandas as pd 
import numpy as np 
from PIL import Image
import os 

def gen_csv(root = "../tile_masks"):
    df = pd.DataFrame(columns=["tile_name", "case_index", "label_0", "label_1", "label_2"])
    for case in os.listdir(root):
        case_ind = case
        npy = "/npy"
        masks = "/masks"
        tiles = "/tiles"
        for tile in os.listdir(root + '/' + case + tiles):
            tile_name = tile.removesuffix('.png')
            x = np.load(root+"/"+case+npy+"/"+tile_name+"_mask.npy")
            d = {0:(x==0).sum(), 1:(x==1).sum(), 2:(x==2).sum() }
            label_0 = d[0]/sum(d.values())
            label_1 = d[1]/sum(d.values())
            label_2 = d[2]/sum(d.values())
            df = df.append({'tile_name': tile_name, "case_index":case_ind, "label_0":label_0, "label_1":label_1, "label_2": label_2}, ignore_index=True)
            print(tile_name)
        
    print(df)
    df.to_csv("tile_masks.csv", index=False)
    return(df)

def gen_png(root = "../tile_masks",df = pd.read_csv("tile_masks.csv"), sample_size = 100, out_dir="sample"):

    df["label"] = np.nan
    df.loc[df.label_0>0.99, 'label'] = 0
    df.loc[df.label_1>0.5, 'label'] = 1
    df.loc[df.label_2>0.1, 'label'] = 2
    df_sample = pd.DataFrame()

    for i in range(3):
        rd = df.loc[df.label==i]
        rd = rd.iloc[np.random.choice(len(rd.index.tolist()), sample_size, replace = False)]
        rd["path"] = out_dir + "/%d/" %i + rd.tile_name + ".png"

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        for case, tile in rd.loc[:,["case_index","tile_name"]].values:
            if not os.path.exists(out_dir+"/%d" %i):
                os.mkdir(out_dir+"/%d" %i)
            img = Image.open(root + '/' + case + "/tiles/" + tile + ".png")
            img.save(out_dir+ "/%d/" %i+tile+".png")
        df_sample = pd.concat([df_sample,rd])
    df_sample.to_csv(out_dir + "/" + out_dir + ".csv", index = False)

    pass


def main():
    # df = gen_csv(root = "../tile_masks")
    gen_png(root = "../tile_masks",df = pd.read_csv("tile_masks.csv"),sample_size = 100)
    pass
if __name__ == "__main__":
    main()
    pass
