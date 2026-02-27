# Raja Swaminathan

# Spiideo XML to Excel Converter for Vanderbilt Women's Soccer team

A GUI-based application that converts Spiideo XML tag exports into Excel spreadsheets.

## Features
- Takes an input XML file and outputs an excel spreadsheet with the accumulated statistics.
- Can be fed timestamps that filter out what tags end up in spreadsheet
- Simple GUI with select XML file
- Automatic tag acuumulation per player

## How to Use
- On the Spiideo video with tags, press info on the left hand side and then press export tags
- This will give you a file with a long name and end with .xml, rename that file
- Download the .exe file from the release tab of the GitHub, which will be on the right hand side
- In the app, press the button and choose the XML file of your choosing
- If you want an accumulation of stats from the full practice, press "Generate Spreadsheet"
- If you want to generate with timestamps, choose your start and end timestamps in HH:MM:SS format
- The spreadsheet will be located in whatever path the pop-up window says

## Installation

```bash
pip install -r requirements.txt
python main.py