from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import ffmpeg

def saveFile():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.asksaveasfilename(
        title="Save final .mp3",
        filetypes=[("MP3 file", "*.mp3")]
    )

    if filePath:
        return filePath
    else:
        print("User canceled the selection.")

def loadFile():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename(
        title="Open input audio file",
        filetypes=[("Audio files", "*.mp3 *.wav *.flac *.aiff *.aac *.ogg")]
    )

    if filePath:
        return filePath
    else:
        print("User canceled the selection.")

def convert(inputPath, outputFile):
    (
        ffmpeg
        .input(inputPath)
        .output(
            outputFile,
            acodec="libmp3lame",
            audio_bitrate="192k",
            ar="44100",
            ac=1,
            )
        .run(overwrite_output=True)
    )

def tryConvert():
    inputFile = loadFile()

    if inputFile:
        outputFile = saveFile()

        if outputFile:
            convert(inputFile, outputFile)