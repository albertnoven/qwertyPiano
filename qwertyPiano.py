import pygame
import numpy as np
import soundfile as sf
import librosa
import os

class qwertyPiano:
    
    def __init__(self, keyboard_layout, input_sound, output_folder):
        self.keyboard_layout = keyboard_layout
        self.input_sound = input_sound
        self.output_folder = output_folder

    # ================== GENERATE CHROMATIC SCALE ==================
    def generate_chromatic_scale(self):
        """Generates a 4-octave chromatic scale from an input sound file."""
        os.makedirs(self.output_folder, exist_ok=True)
        y, sr = librosa.load(self.input_sound, sr=None)
        
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chromatic_scale = [f"{note}{octave}" for octave in range(4) for note in notes]  # 4 octaves from 0 to 3
        
        for i, note in enumerate(chromatic_scale):
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=i)  # Apply pitch shift
            sf.write(os.path.join(self.output_folder, f"{note}.wav"), y_shifted, sr)

        return chromatic_scale, sr

    # ================== MAP KEYS TO NOTES ==================
    def create_keyboard_mapping(self, chromatic_scale):
        """Maps keyboard keys to the chromatic scale."""
        if len(self.keyboard_layout) > len(chromatic_scale):
            print(f"Warning: Keyboard layout has more keys than chromatic scale.")
        return {key: chromatic_scale[i] for i, key in enumerate(self.keyboard_layout) if i < len(chromatic_scale)}
    
    # ================== PYGAME PIANO ==================
    def run_piano(self, keyboard_mapping, sample_rate):
        """Runs an interactive Pygame piano with minimal latency and supports chords."""
        pygame.init()
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=1, buffer=512)  # Lower buffer for less latency
        screen = pygame.display.set_mode((500, 300))  # Keeps focus for keyboard input
        pygame.display.set_caption("qwerty Piano")

        # Preload sounds
        sounds = {}
        is_playing = {}
        playing_keys = set()  # To track the currently pressed keys
        
        for key, note in keyboard_mapping.items():
            file_path = os.path.join(self.output_folder, f"{note}.wav")
            if os.path.exists(file_path):
                sound = pygame.mixer.Sound(file_path)
                sounds[key] = sound
                is_playing[key] = False

        running = True
        while running:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                running = False

            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key = event.unicode.lower()

                if event.type == pygame.KEYDOWN:
                    if key in sounds and key not in playing_keys:
                        # Play sound for the newly pressed key
                        sounds[key].play(fade_ms=10)
                        is_playing[key] = True
                        playing_keys.add(key)  # Add key to pressed set

                    elif event.key == pygame.K_ESCAPE:  # Exit
                        running = False

                elif event.type == pygame.KEYUP and key in sounds:
                    # Fade out the sound when the key is released
                    sounds[key].fadeout(500)
                    is_playing[key] = False
                    playing_keys.remove(key)  # Remove key from pressed set

        pygame.quit()

# ================== MAIN EXECUTION ==================
if __name__ == "__main__":
        # ================== CONFIG ==================
    KEYBOARD_LAYOUT = "zxcvbasdfgqwert12345nm,./hjkl;yuiop67890" #a sequence of keys put in a string that will corespond to the full chromatic scale from top to bottom for you keyboard. This can be customized the way you want it. 
    INPUT_SOUND = "/home/albert/pythonProjects/input.wav"  # Path to your sound file in .wav format
    OUTPUT_FOLDER = "/home/albert/pythonProjects/scaled_notes"  # Path and name to the folder that will contain all the notes for you piano

    myPiano = qwertyPiano(KEYBOARD_LAYOUT, INPUT_SOUND, OUTPUT_FOLDER) # Create an instance that is your generated piano.

    chromatic_scale, sample_rate = myPiano.generate_chromatic_scale()  # Generate scale
    keyboard_mapping = myPiano.create_keyboard_mapping(chromatic_scale)  # Map keys to notes
    myPiano.run_piano(keyboard_mapping, sample_rate)  # Run interactive piano
