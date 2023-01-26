# MONAI
A game that prompts Dall-E generated images to the player and the player has to guess the prompt that was used to generate the image.The images are 
obtained by API calls to the craiyon.ai API. The prompts for the pictures are generated using the OpenAI API text completion of the text davinci 003 model, 
using the request "give me prompts for DALL-E to generate images". This allows for the game to have an infinite number of levels as the prompts generated
are different everytime. The temperature setting for the model can be changed however, a value of 0.5 gave the best results after extensive testing. The 
accuracy of players guesses are compared to the actual prompt by first changing them to vector embeddings then using cosine similarity. The generated 
images, the entry box for user input and the display for percentage of similarity are all done using the Tk GUI toolkit through the TKinter framework on 
Python. The loading time for each level is 53 seconds on average due to the API calls to craiyon, and the next level can be loaded up by pressing the "~"
key on your keyboard anytime.
