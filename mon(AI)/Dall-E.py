from craiyon import Craiyon
from PIL import Image 
from io import BytesIO
import base64
from tkinter import *
from PIL import ImageTk, Image
import math
import cohere
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai

co = cohere.Client("LlOs6tjZQqrhF2t0CFz9m4hEdY2QyWCNdRjReyRI")
openai.api_key = "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"

generator = Craiyon()


win = Tk()
win.geometry("1300x900")
win.config(bg='black')
win.title("MonAI")

logo = Image.open("mon(AI)/monai logo 2.png")
logo = logo.resize((280, 75), Image.Resampling.LANCZOS)
logoImg = ImageTk.PhotoImage(logo)
label = Label(master=win, image=logoImg, bg='black', height=120, width=325)
label.pack()


prompts = []

def edit(s):
  return s[3:]

def get_prompts():
  text = "Give me 9 prompts for Dall-E to generate images"

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=text,
    max_tokens=150,
    temperature=0.5
  )

  answer = response.choices[0].text
  prompts = answer[2:].split("\n")

  return list(map(edit, prompts))


def embed_text(texts):
  text_list = [texts]
  output = co.embed(
                model="large",
                texts=text_list)
  embedding = output.embeddings
  return embedding

def get_similarity(target,candidates):
  # Turn list into array
  candidates = np.array(candidates)
  target = np.array(target)

  # Calculate cosine similarity
  sim = cosine_similarity(target,candidates)
  sim = np.squeeze(sim).tolist()

  # Return similarity scores
  return sim

def get_points(target, candidate):
    text1 = embed_text(target)
    text2 = embed_text(candidate)
    sim = get_similarity(text1, text2)
    points = math.floor(sim*100)
    return points

def reset(event):
    frame.destroy()
    win.quit()

def enter(event):
    text.clipboard_clear()
    guess = entry.get()
    entry.delete(0,END)
    point = get_points(sent, guess)
    st = '\n' + guess + ": " + str(point) + '%\n\n'
    text.insert('0.0', st)

    if point >= 99:
        entry.destroy()
        end = Label(text="CORRECT!", bg='black', fg='green', width=30, height=5, master=frame)
        end.pack()


while True:
    if prompts == []:
        prompts = get_prompts()
        print(prompts)

    sent = prompts.pop()
    text = Text(height=30, width=35, bg='grey', fg='black')


    # create a scrollbar widget and set its command to the text widget
    scrollbar = Scrollbar(text, orient='vertical', command=text.yview)

    #  communicate back to the scrollbar
    text['yscrollcommand'] = scrollbar.set
    text.place(anchor="w", relx=0.05, rely=0.48)


    frame = Frame(win, width=800, height=800, bg='black')

    frame.place(anchor='center', relx=0.5, rely=0.5)

    frame.pack()
    space = Label(text="", height=3, bg='black', master=frame)


    entry = Entry(width=30, bg="dark grey", master=frame)


    result = generator.generate(sent)
    images = result.images # A list containing image data as base64 encoded strings
    image = Image.open(BytesIO(base64.decodebytes(images[0].encode("utf-8"))))

    # image = Image.open("image-5.png")

    image = image.resize((400,400), Image.Resampling.LANCZOS)
    # Use the PIL's Image object as per your needs
    img = ImageTk.PhotoImage(image)
    pic = Label(master=frame, image = img, bg='black')


    pic.pack()
    frame.pack()
    space.pack()
    entry.pack()

    entry.bind("<Return>", enter)
    win.bind("<~>", reset)
    win.bind("<Escape>", quit)
    win.mainloop()



