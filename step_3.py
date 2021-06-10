import skimage.io as io # basic image methods
import numpy as np # for ndarray

class ImageAnalysis:
    def __init__(self, image):
        self.image = io.imread(image) # immediately read picture data into numPy array
        self.hidden = None # blank for hidden image data
        
    def __str__(self): # method to tell default print() what to write to the output
        # this uses string formatting of the 'shape' int tuple into string
        # notice (<item>,) notation (especially the comma after the first item) /
        # this tells Python that this is a formatting tuple with one operand, /
        # not an expression (<expr>)
        return 'Shape is: {}'.format(self.image.shape)
    
    def show(self):
        io.imshow(self.image) # transfer image data into the output queue
        io.show() # show image in queue, using GUI

    # to display hidden picture and ensure it was saved in the class instance
    def showHidden(self):
        if self.hidden is None:
            print('No hidden picture built!')
        else:
            io.imshow(self.hidden)
            io.show()

    def retriveHidden(self):
        # initialize sedulting array in the class instance
        # specifying dimensions + type, latter to avoid imprecise conversions
        self.hidden = np.ndarray(( 131, 100, 3 ), np.uint8)
        
        for row in range(131): # for each resulting row...
            for col in range(100): # for each resulting col...
                self.hidden[row, col] = self.image[row * 11][col * 11] # take each 11th pixel
        
        io.imsave('./hidden.jpg', self.hidden) # save

    def fix(self):
        # prepare source image dimensions
        height = len(self.image) 
        width = len(self.image[0])

        # running through each pixel
        for row in range(height):
            for col in range(width):
                # pass ones than are not 11th they are ok
                if row % 11 != 0 and col % 11 != 0:
                    continue

                """
                4 neighbouring pixels (N) around target pixel (A):
                .N.
                NAN
                .N.
                """
                neighboursIndices = [[row + 1, col + 1], [row + 1, col - 1], [row - 1, col + 1], [row - 1, col - 1]]

                # collect only ones that don't step out of bounds
                neighbours = []
                for nI in neighboursIndices:
                    rown, coln = nI
                    if rown < 0 or rown >= height or coln < 0 or coln >= width:
                        continue
                    neighbours.append(self.image[rown, coln])
                
                count = len(neighbours)
                # this shouldn't happen semanticaly, but just in case
                if count == 0:
                    continue
                # count avg of each component
                sumR = sumG = sumB = 0;
                for n in neighbours:
                    r,g,b = n
                    sumR += r
                    sumG += g
                    sumB += b

                # write new pixel
                self.image[row, col, 0] = sumR // count;
                self.image[row, col, 1] = sumG // count;
                self.image[row, col, 2] = sumB // count;
                    
                        

i = ImageAnalysis('mountain.png')
print(i)
# i.show()
i.retriveHidden()
# i.showHidden()
i.fix() # fixing "in place", not making new picture
i.show()
# io.imsave('./fixed.jpg', i.image) # save fixed result into file, just in case 