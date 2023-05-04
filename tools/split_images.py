from PIL import Image
import glob
import os

def splitImages(input_dir,output_dir,cols,rows):
    path_list =list(glob.glob(input_dir+"/*.png", recursive=True))
    
    for path in path_list:
        image = Image.open(path)
        width, height = image.size
        w1 = width/cols
        h1 = height/rows
        
        for i in range(cols):
            for j in range(rows):
                crop_image = image.crop((i*w1, j*h1, (i+1)*w1, (j+1)*h1))
                crop_image.save(output_dir+"/"+str(os.path.basename(os.path.splitext(path)[0]))+str(i)+str(j)+".PNG")
     
def splitImage(image,cols,rows):
    
    width, height = image.size
    w1 = width/cols
    h1 = height/rows
    
    image_list = []
    
    for j in range(cols):
        image_list.append([])
        for i in range(rows):
            crop_image = image.crop((i*w1, j*h1, (i+1)*w1, (j+1)*h1))
            image_list[j].append(crop_image)
            
    return image_list

if __name__ == "__main__":
    splitImages("../data/base/colors/black", "../data/crop/colors/black", 8, 8)
    splitImages("../data/base/colors/white", "../data/crop/colors/white", 8, 8)
    
    splitImages("../data/base/chess_pieces/king", "../data/crop/chess_pieces/king", 8, 8)
    splitImages("../data/base/chess_pieces/knight", "../data/crop/chess_pieces/knight", 8, 8)
    splitImages("../data/base/chess_pieces/none", "../data/crop/chess_pieces/none", 8, 8)
    splitImages("../data/base/chess_pieces/pawn", "../data/crop/chess_pieces/pawn", 8, 8)
    splitImages("../data/base/chess_pieces/queen", "../data/crop/chess_pieces/queen", 8, 8)
    splitImages("../data/base/chess_pieces/bishop", "../data/crop/chess_pieces/bishop", 8, 8)
    splitImages("../data/base/chess_pieces/rook", "../data/crop/chess_pieces/rook", 8, 8)
        