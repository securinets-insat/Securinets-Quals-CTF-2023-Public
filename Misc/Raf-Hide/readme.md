# Write up for Raf-Hide

### Description:
> My friend write a tool that can hide data inside an image. He give me this tool with an anime video without any source code and challenge me to get the secret! . Can you help me extract the flag? 
Flag format: Securinets{Secrect}

> In this Challenge you will get a go binary and a video! I will not explain how to reverse the binary. The main Idea is to understand what the binary do and extract the data from the video

This is a python version of what the binary can do : 

```python
from PIL import Image
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Example program using options and arguments')

# Add options and arguments
parser.add_argument('-i', '--input', help='select cover-image', type=str)
parser.add_argument('-e', '--embedfile', help='select image to be embedded', type=str)
parser.add_argument('-o', '--output', help='The output', type=str)

# Parse the arguments
args = parser.parse_args()

# Check if the options and arguments are correct
if args.input and args.embedfile and args.output:
    print('Starting Hiding ...')
else:
    # Provide an usage message if the input is incorrect
    parser.print_usage()
    exit()

image=Image.open(args.input)
embed=Image.open(args.embedfile).convert('1')
if image.size != embed.size:
    print('The Images are not in the same size!')
    exit()


embed_data=embed.load()
image_data=image.load()
index=0

for j in range(image.height):
    for i in range(image.width):
        flag_pix=int(embed_data[i,j])
        flag_pix &=1
        im_pix=list(image_data[i,j])
        data = ((flag_pix << index%2) | (254-index%2)) 
        if flag_pix ==1 :
            im_pix[index%3]|= data & (1+index%2)
        else:
            im_pix[index%3]&= data
        image_data[i,j]=tuple(im_pix)
        index+=1
image.save(args.output)
```

This is a golang version of what the binary can do :
 
```go
package main

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"os"
	"flag"
)

func main() {

	// Create a new FlagSet to parse command line arguments
	flagSet := flag.NewFlagSet("steganography", flag.ExitOnError)

	// Define command line options and arguments
	inputFileName := flagSet.String("i", "", "select cover-image")
	embedFileName := flagSet.String("e", "", "select image to be embedded")
	outputFileName := flagSet.String("o", "", "The output")

	// Parse the command line arguments
	flagSet.Parse(os.Args[1:])

	// Check if the options and arguments are correct
	if *inputFileName == "" || *embedFileName == "" || *outputFileName == "" {
		flagSet.Usage()
		os.Exit(1)
	}



	// Open the input file
	inputFile1, err := os.Open(*embedFileName)
	if err != nil {
		panic(err)
	}
	defer inputFile1.Close()

	// Decode the PNG image
	inputImage1, _, err := image.Decode(inputFile1)
	if err != nil {
		panic(err)
	}

	// Check if the image is grayscale
	grayImage, ok := inputImage1.(*image.Gray)
	if !ok {
		fmt.Println("Error: input image is not grayscale")
		return
	}

	// Get the width and height of the image
	embed_width := grayImage.Bounds().Size().X
	embed_height := grayImage.Bounds().Size().Y

	// Open the input file
	inputFile, err := os.Open(*inputFileName)
	if err != nil {
		panic(err)
	}
	defer inputFile.Close()

	// Decode the image as a generic Image interface value
	inputImage, _, err := image.Decode(inputFile)
	if err != nil {
		panic(err)
	}

	// Assert the image to an *image.RGBA or *image.NRGBA value
	rgba, ok := inputImage.(*image.RGBA)
	if !ok {
		nrgba, ok := inputImage.(*image.NRGBA)
		if !ok {
			panic("Input image format not supported")
		}
		rgba = image.NewRGBA(nrgba.Bounds())
	}

	// Get the width and height of the image
	bounds := rgba.Bounds()
	width := bounds.Size().X
	height := bounds.Size().Y
	index:=0

	if width!=embed_width || height!=embed_height {
		panic("The Images are not in the same size!")

	}
	// Invert the colors of the image by subtracting each RGB component from 255
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			intensity := grayImage.GrayAt(x, y).Y & 1
			i:=uint8(index%2)
			data:= ((intensity << i) | (254-i))
			r, g, b, a := rgba.At(x, y).RGBA()
			im_pix:= [3]uint8{uint8(r),uint8(g),uint8(b)}
			j:= uint(index%3)
			if intensity == 1 {
				im_pix[j] = im_pix[j] | (data & (1+i))
			} else {
				im_pix[j] = im_pix[j] & data
			}
			newColor := color.RGBA{
				R: uint8(im_pix[0]),
				G: uint8(im_pix[1]),
				B: uint8(im_pix[2]),
				A: uint8(a),
			}
			rgba.SetRGBA(x, y, newColor)
			index++
		}

	}

	// Create the output file
	outputFile, err := os.Create(*outputFileName)
	if err != nil {
		panic(err)
	}
	defer outputFile.Close()

	// Encode the output image as PNG
	if err := png.Encode(outputFile, rgba); err != nil {
		panic(err)
	}

	fmt.Println("Output image saved successfully")
}
```

As we see here this script try to hide image inside another image in a specific way. We need to understand how he hide data. 

The tool take a black-white image that have only 2 values in his pixels and try to inject this pixels in the LSB of RGB channels of the other image! 
But be carefull is not a traditional or simple LSB steganoraphy here! In each iteration it take a single channel. For example the 1st pixel will use the Red value, 2nd will use the Green value, 3rd will use the Blue and so on. 

We need to reverse this algorithm and write a script that can extract from images used by this tool.

Let's use this one! 

```python
from PIL import Image

INPUT_FILFE="input.png"
EXTRACTED_DATA="extracted.png"
image=Image.open(INPUT_FILFE)
image_data = image.load()
extracted = Image.new('1', (image.width,image.height), 1)
index=0
output_data=extracted.load()
for j in range(image.height):
    for i in range(image.width):  
        im_pix=list(image_data[i,j])
        flag_pix = (im_pix[index%3]&(1+index%2)) 
        if flag_pix >= 1:
            flag_pix=255
        output_data[i,j]=flag_pix
        index+=1
extracted.save(EXTRACTED_DATA)
```
To make sure that everything is ok now! We can use the given tool and hide a black-white image and try to extract it with our new script.

We assume that everything is fine. Let's take a look now how can we extract data from the video!

![](./video-gif.gif)

Let's extract every frame from this video and try to extract a data from it using our last script. Maybe we will find something here!

### Extract all the frames using ffmpeg
After running this command. we get 383 frames.
```bash
raf@Securinets:~$ mkdir frames
raf@Securinets:~$ ffmpeg -i challenge.mp4 frames/%3d.png
```
### Extract data from each frame using our solver

Let's use our solver to try extracting data from each frame.
```bash 
raf@Securinets:~$ mkdir data
```
We will put our solver inside a function and use a for loop to run it on each frame 
```python

def extract(frame,output):
    image=Image.open(frame)
    image_data = image.load()
    extracted = Image.new('1', (image.width,image.height), 1)
    index=0
    output_data=extracted.load()
    for j in range(image.height):
        for i in range(image.width):  
            im_pix=list(image_data[i,j])
            flag_pix = (im_pix[index%3]&(1+index%2)) 
            if flag_pix >= 1:
                flag_pix=255
            output_data[i,j]=flag_pix
            index+=1
    extracted.save(output)

for i in range(383):
    index="0"*(3-len(str(i+1)))+str(i+1)+".png"
    extract("frames/"+index,"data/"+index)
```

Let's now check the result and what we get!
Of couse we will get 383 images. But is all the images are usefull or not? Let's check.

We find this image extracted from the 1st frame of the image!

![](./000.png)

Bingo! We are on the right way! The author told us to check the last images! Yeah we will but let's check what we got in all the images!

We found a big number of image that have a black line in random position of the image!

<p float="left">
  <img src="015.png" width="450" style="margin-right:50px;" />

  <img src="210.png" width="450" /> 
</p>

Ok Let's focus on the last images as the author said. This is will be better for us. Wait what?! We found a 2 pastebin links and 2 images putted as hint for us. And of couse a rabbit hole(Fake Flag)

<p float="center">
  <img src="372.png" width="320"style="margin-right:10px;" />
  <img src="377.png" width="320"style="margin-right:10px;" /> 
  <img src="381.png" width="320"style="margin-right:10px;" /> 
</p>

Let's check the content of the 2 pastebin links and see what we have! 

```txt
Advertising flash, it's time to relax and rest.
This pastebin is the solution to your problem 
Those links will Absolutely help you 
 
https://4n6nk8s.tech
https://anas-cherni.me/
https://ironbyte.me/
https://yassine-belkhadem.tech/ ( Don't waste your time with this link)
https://github.com/M0ngi
https://soter14.tech/
 
 
Thi is the FLAG: GG_Tr0ll1ng_1s_MY_G4mE_!
 
https://github.com/Mohamed-Rafraf
https://github.com/adamlahbib
https://www.linkedin.com/in/mohamed-rafraf/
https://www.linkedin.com/in/adamlahbib/
https://www.linkedin.com/in/anascherni/
https://www.linkedin.com/in/yassine-belkhadem-396266204/
https://www.linkedin.com/in/m0ngi/
https://www.linkedin.com/in/mohamed-ali-ouachani-00a452237/
https://www.linkedin.com/in/rania-midaoui-b0163a1bb/
https://www.linkedin.com/in/mohamed-ayadi-5a10621a4/
https://www.linkedin.com/in/yassine-belarbi-853303208/
```

There is another fake flag & links for the blogs of the author and his team members! Yeah It's SOter14 team. Let's Check the other one. Maybe it will help

```txt
6 <--> 29
15 <--> 25
11 <--> 34
10 <--> 24
1 <--> 23
14 <--> 35
2 <--> 19
17 <--> 33
3 <--> 32
8 <--> 27
13 <--> 31
0 <--> 18
7 <--> 20
5 <--> 28
12 <--> 30
```

Absolutely this thing will help but we still didn't know how this text file will help us! Let's understand the explanation putted on the other frames.

![](./377.png)

The author told us that he split the image to many slices and put each slice in an empty unique image!!! We get it! The random lines are tiny pieces of unique image!

But how can we collect this slice and re-order them to get the original? The lines are ordered randomly? Let's think.

### collect the pieces and recover the orginal image

The solution is simple. That's assume that the white color have a `0 value` and the black color have `1 value`. We can sum the pixels of all the images with this concept to recover the image, right? 

> We know that our image size is 720x720 (The resolution of our video) and from our extracted images we know that we have 360 images that splitted to slices. which mean that every line present 2px (width) from the original image.

Take a look at this script then!

```python
from PIL import Image

img=Image.new('1',(720,720),255)
imgpixs=img.load()
for n in range(1,360):
    name="0"*(3-len(str(n+1)))+str(n+1)+".png"
    image=Image.open("data/"+name)
    image_pixs=image.load()
    print("Image Number : ",n)
    for i in range(720):
        for j in range(720):
            if image_pixs[i,j]!=255:
                imgpixs[i,j]=image_pixs[i,j]

img.save("Recovered.png")
```
In this script we collect all the black pixels and ignore the white pixels. Because we generate a white image and we will fill it with the black color. Let's recover the image now!!

Bingo! There is a progress, we got this image!

![](./recoverd.png)

Oh god! It's a broken QR code. How can we deal with this thing. Oh yeah! We have another clue! The author left this hint for us! 

![](./381.png)

Oh cool! The author split the QRCode to small square and shuffle them in random order! We need to recover them. The squares are numeroted from 0 to n-1 pieces. This order will help us. Now We get the utility of the pastebin link!

```txt
6 <--> 29
15 <--> 25
11 <--> 34
10 <--> 24
1 <--> 23
14 <--> 35
2 <--> 19
17 <--> 33
3 <--> 32
8 <--> 27
13 <--> 31
0 <--> 18
7 <--> 20
5 <--> 28
12 <--> 3
```
This is will help us how re-order the QRCode. Let's take a deep look now the the broken QRCode!.

The QRCode is splitted by 6 in width and 6 in height. So each piece's size is 120x120. And we have 36 pieces. It's impossible to recover the image without the help of pastebin link. Let's take this line for example `0 <--> 18`, this link told us that the author switch the 1st piece with the 19th piece. (We Start counting from 0 due to the explanation). So we need to write a script that can order this QRCode! We need to recover it!

Let's put the content of the pastebin inside a textfile named `help.txt` and start write our solver.
```python
from PIL import Image

W_SPLIT=6
H_SPLIT=6

ASSEMBLED_IMAGE="Assembled.png"
SPLITTED_IMAGE="Recovered.png"
image= Image.open(SPLITTED_IMAGE)
width, height = image.size
pixels = image.load()

def change_chunk(index1,index2):
    pos1=[]
    pos1.append(index1 % W_SPLIT)
    pos1.append(index1 // W_SPLIT)
    pos2=[]
    pos2.append(index2 % W_SPLIT)
    pos2.append(index2 // W_SPLIT)
    height_chunk=height // H_SPLIT
    width_chunk= width // W_SPLIT
    for i in range (width_chunk):
        for j in range (height_chunk):
            aux= pixels[pos1[0]*width_chunk+i,pos1[1]*height_chunk+j]
            pixels[pos1[0]*width_chunk+i,pos1[1]*height_chunk+j]= pixels[pos2[0]*width_chunk+i,pos2[1]*height_chunk+j]
            pixels[pos2[0]*width_chunk+i,pos2[1]*height_chunk+j]= aux

data=open("help.txt","r").read().split("\n")
for i in range(len(data)-1):
    position=data[i].split("<-->")
    print(position)
    change_chunk(int(position[0]),int(position[1]))

image.save(ASSEMBLED_IMAGE)
```
Yeah It works fine!! We recover the QRCode! 

![](./Assembled.png)

But something is wrong here! It sills broken and We can't scan it :(. But why? are we have any problem with our solver?

Ah No. I get it! We have 36 pieces and each line from `help.txt` have correspond to 2 pieces! So we have to find 18 lines, right ? 

```bash 
raf@Securinets:~$ wc -l help.txt
15
```
Oh no we have 15 lines, So we have 6 pieces we need to re-order them by ourselves! Now I get why the Author said Help `LITTLE BIIT`. He left the 6 pieces to deal with it.

In this case we need to do a bruteforce to all the combinasions. We have 6 pieces, so we have 6! possibility
and 6! = 720 which is possible to deal with it using a python script. Let's re-order the 6 pieces each time and try to scan the QRCode. Once the QRCode is readable, we will stop our program!

Let's get the flag now !!! Let's DO IT NOW! We're so close!

So the 1st thing that we need to do it is that we need to get the index of missed pieces. The `help.txt` is the key!

Let's generate an array that have the order (index) of the missed pieces. Then we use our `change_chunck()` method and try all the combinaisons using the `itertools`. Finally try to scan the QRCode each time using the `qrtools`

Let's install the qrtools first 

```bash 
raf@Securinets:~$ sudo apt-get install python3-qrtools

```
Now let's write down our last script (I Hope) :
```python

from PIL import Image
import qrtools
from itertools import permutations

qr=qrtools.QR()

def missed_data():
    not_missed=[]
    data=open("help.txt","r").read().split("\n")
    for i in range(len(data)-1):
        position=data[i].split("<-->")
        not_missed.append(int(position[0]))
        not_missed.append(int(position[1]))
    print(not_missed)
    missed=[]
    for i in range(0,36):
        if not (i in not_missed):
            missed.append(i)
    return missed

chuncks=missed_data()
print(chuncks)
H_SPLIT=6
W_SPLIT=6
SPLITTED_IMAGE="Assembled.png"
height,width=720,720

permutations=list(permutations(chuncks,6))
image=Image.open("Assembled.png")
pixels=image.load()

def change_chunk(index1,index2):
    pos1=[]
    pos1.append(index1 % W_SPLIT)
    pos1.append(index1 // W_SPLIT)
    pos2=[]
    pos2.append(index2 % W_SPLIT)
    pos2.append(index2 // W_SPLIT)
    height_chunk=height // H_SPLIT
    width_chunk= width // W_SPLIT
    for i in range (width_chunk):
        for j in range (height_chunk):
            aux= pixels[pos1[0]*width_chunk+i,pos1[1]*height_chunk+j]
            pixels[pos1[0]*width_chunk+i,pos1[1]*height_chunk+j]= pixels[pos2[0]*width_chunk+i,pos2[1]*height_chunk+j]
            pixels[pos2[0]*width_chunk+i,pos2[1]*height_chunk+j]= aux

print('[-] Trying to fix the QRCode and Getting the flag ...')

for i in range(len(permutations)):
    comb=list(permutations[i])
    change_chunk(comb[0],comb[1])
    change_chunk(comb[2],comb[3])
    change_chunk(comb[4],comb[5])
    image.save("Final.png")
    if qr.decode("Final.png"):
        print(qr.data)
        break
```

And we got the flag as an output Here!!! BINGO! We get the flag! 

![](./finally.png)

And of course the QRCode is saved! And this is our QRCode!

![](./Final.png)

> The Final flag is : Securinets{Every_Fr4Me_H4S_HiS_own_S7ory}