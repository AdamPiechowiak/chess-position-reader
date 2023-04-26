from PIL import Image
import glob
import os

def splitImage(input_dir,output_dir,cols,rows):
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
        

if __name__ == "__main__":
    splitImage("../data/colors/black/base", "../data/colors/black/crop", 8, 8)
    splitImage("../data/colors/white/base", "../data/colors/white/crop", 8, 8)
    
    splitImage("../data/chess_pieces/king/base", "../data/chess_pieces/king/crop", 8, 8)
    splitImage("../data/chess_pieces/knight/base", "../data/chess_pieces/knight/crop", 8, 8)
    splitImage("../data/chess_pieces/none/base", "../data/chess_pieces/none/crop", 8, 8)
    splitImage("../data/chess_pieces/pawn/base", "../data/chess_pieces/pawn/crop", 8, 8)
    splitImage("../data/chess_pieces/queen/base", "../data/chess_pieces/queen/crop", 8, 8)
    splitImage("../data/chess_pieces/bishop/base", "../data/chess_pieces/bishop/crop", 8, 8)
    splitImage("../data/chess_pieces/rook/base", "../data/chess_pieces/rook/crop", 8, 8)
        