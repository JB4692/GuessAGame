import os, random
from PIL import Image

def make_crops(infile_path, filename):
    head, tail = os.path.split(filename)
    file, ext = os.path.splitext(tail)
    outfile = file + "_cropped"
    
    try:
        with Image.open(infile_path) as img:
            x, y = img.size
            if x < 500 or y < 500:
                img = img.resize((x*2, y*2), Image.Resampling.LANCZOS)
                print("image resized")
            print(x, y)
            x, y = img.size
            left = random.randint(int(x*.3), int(x*.7))
            upper = random.randint(int(y*.3), int(y*.7))
            center_x = left + 128
            center_y = upper + 128

            for size in range(128, 1080, 128):
                half = size // 2

                new_left  = center_x - half
                new_upper = center_y - half
                new_right = center_x + half
                new_lower = center_y + half
                
                region = (new_left, new_upper, new_right, new_lower)                
                cropped_img = img.crop(region)

                new_file = "./crop_imgs/"+ outfile + f"_{str(size)}.jpg" 
                cropped_img.save(new_file)
                print("Saved file to:", new_file)

    except OSError as e:
        print("cannot convert", infile_path)
        print(e)

def get_file_names(path):
    files = []

    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        if os.path.isfile(full_path):
            files.append(file)
    return files
    

if __name__ == "__main__":
    base_path = "./base_imgs/" 
    game_titles = get_file_names(base_path)
    
    random_index = random.randint(0, len(game_titles)-1)
    file_name = game_titles[3]
    file_path = base_path + file_name
    print(file_name, file_path)
    
    make_crops(file_path, file_name)
    

