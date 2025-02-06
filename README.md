#qwertyPiano
A musical instrument using a computer keyboard with customizable key mappings and sound files of your choice.

On lines 87 to 89, you can customize your keyboard by selecting your own key mapping and choosing the .wav file that will represent the sound of your instrument.

The KEYBOARD_LAYOUT variable, located on line 87, is a string that corresponds to the keys mapped to a chromatic scale. You can modify this string to change the keyboard layout. Many people prefer layouts like the Janko or various accordion layouts. Perhaps you can create a revolutionary keyboard layout on your own laptop!

The INPUT_SOUND variable is the path to the .wav file that will represent the sound of your instrument. You can choose any .wav file you like for the sound. This file will correspond to the lowest note on your keyboard. The program will then generate the appropriate pitches for your instrument using this .wav file. This process is handled in the generate_chromatic_scale function. I have attached a .wav file to this repository which you can use. But you can also record your own or download your own .wav file from anywhere. 

The OUTPUT_FOLDER is the path where you want the folder containing all the chromatic notes for your keyboard to be saved.

Modify all these three variables to your liking. Install the neccesary python packages and you are ready to make music on the qewrtyPiano!
