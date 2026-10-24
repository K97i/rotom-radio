from songClass.songClass import Song

from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import json

class Ranking:

    # Limit constant (set to 40)
    LIMIT = 40

    @staticmethod
    def loadSet():
        """
        Lets user select the actual dataset

        Returns:
            (object): Contents of the JSON, all available lists
        """
        root = tk.Tk()
        root.withdraw()

        filePath = filedialog.askopenfilename(
            title="Select data set",
            filetypes=[("JSON files", "*.json")]
        )

        if filePath:
            with open(filePath, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print("User canceled the selection.")

    @staticmethod
    def prettyPrint(data: list[Song]):
        """
        Prints the given list in a specified format
        
        Args:
            data (list[Song]): Final list
        """

        for i in range(len(data)):
            print(f"{i + 1}: {data[i].artist} - {data[i].title} (Last Position: {data[i].lastPosition} Hotness: {data[i].hotness})")

    @staticmethod
    def boringPrint(data: list[Song]):
        """
        Prints the given list in a pasteable
        
        Args:
            data (list[Song]): Final list
        """

        for i in range(len(data)):
            print(f"{data[i].artist} - {data[i].title}")

    @staticmethod
    def parse(data: object):
        """
        Parses and returns all lists in the JSON
        
        Args:
            data (object): Actual JSON object

        Returns:
            (list[list[Song]]): Lists of all song lists
        """
        return [
            [
                Song (
                    title=song["title"], 
                    artist=song["artist"], 
                    lastPosition=song["lastPosition"], 
                    hotness=song["hotness"]
                )
                for song in item
            ]

            for item in data.values()
        ]

    @staticmethod
    def merge(lists: list[list[Song]]):
        """
        Merges all lists using a point-based system (higher points = higher rank).
        """
        points = defaultdict(int)

        for songList in lists:
            chart_len = len(songList)
            for idx, item in enumerate(songList):
                pts = chart_len - idx
                points[item] += pts

        # Sort in descending order of points
        return sorted(points.keys(), key=lambda x: points[x], reverse=True)[:Ranking.LIMIT]

    @staticmethod
    def rank():
        """
        Final rank method to call

        Returns:
            finalList (list[Song]): Final list of songs limited to LIMIT constant
        """
        # Load JSON
        data = Ranking.loadSet()

        if data:
            # Merge lists to final top 40
            finalList = Ranking.merge(
                # Parse to individual lists
                lists=Ranking.parse(data)
            )

            # Ranking.prettyPrint(finalList)
            Ranking.boringPrint(finalList)

            # Return final list
            return finalList