import sys
import cv2

import src.dog_vision as dog
import src.bee_vision as bee
import src.fly_vision as fly
import src.cow_vision as cow
import src.cat_vision as cat
import src.shark_vision as shark
import src.horse_vision as horse
import src.bird_vision as bird

animal = sys.argv[1]
img_path = sys.argv[2]

img = cv2.imread(img_path)
res = ''

if animal == 'bee':
    res = bee.see(img)
elif animal == 'bird':
    res = bird.see(img)
elif animal == 'cat':
    res = cat.see(img)
elif animal == 'cow':
    res = cow.see(img)
elif animal == 'dog':
    res = dog.see(img)
elif animal == 'fly':
    res = fly.see(img)
elif animal == 'horse':
    res = horse.see(img)
elif animal == 'shark':
    res = shark.see(img)

cv2.imshow(animal + 'Eye', res)
cv2.waitKey()
cv2.destroyAllWindows()
