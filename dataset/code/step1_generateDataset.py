import pandas as pd
import os.path


def get_clean_data (row):

    headers = ["NO", "img_ID", "ratings_1", "ratings_2", "ratings_3", "ratings_4", "ratings_5", "ratings_6", "ratings_7", "ratings_8", "ratings_9", "ratings_10", "tag_1", "tag_2", "challenge_ID"]
    all_info =[]
    df = pd.read_csv("/Users/s.oury/Code/thumbnails_selection/datasets/AVA/data_txt.csv", index_col = None)
    for i in range (row):
        data = df.loc[i,headers]
        img_id=data["img_ID"]
        if os.path.exists('/Users/s.oury/Code/thumbnails_selection/datasets/AVA/images/%s.jpg' %int(img_id)) == True:
            info={} # dict
            for h in headers:
                info[h]=data[h]

            all_info.append(info)
            #print(all_info)
            if i%100==0:

                print("sample {}/{}".format(i,255530))

            #print(data["img_ID"])
        else:
            print("{} dos nor exist".format(int(img_id)))

    return all_info

if __name__ == "__main__":
    all_info = get_clean_data(255530)
    df = pd.DataFrame.from_dict(all_info, orient='columns')
    export_csv = df.to_csv (r'/Users/s.oury/Code/thumbnails_selection/datasets/AVA/dataset_AVA_clear2.csv', index = None, header = True)
