from PIL import Image
import glob

if __name__ == "__main__":
    path='../data/colors/black/base/*'
    
    path_list =list(glob.glob(path, recursive=True))
    l=1;
    for i in path_list:
        image = Image.open(i)
        width, height = image.size
        
        w1 = width/8
        h1 = height/8
        
        for i in range(8):
            for j in range(8):
                crop_image = image.crop((i*w1, j*h1, (i+1)*w1, (j+1)*h1))
                crop_image.save("../data/colors/black/crop/2"+str(l)+str(i)+str(j)+".PNG")
        l=l+1