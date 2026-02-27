import xml.etree.ElementTree as ET
import pandas as pd
import os


def process_xml(xml_path, start_time=None, end_time=None):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    label_types = set()
    players = set()

    # -------------------------
    # PASS 1 — Collect labels
    # -------------------------
    for instance in root.findall(".//instance"):
        start = float(instance.find("start").text)
        end = float(instance.find("end").text)

        # Apply inclusive timestamp filter if provided
        if start_time is not None and end_time is not None:
            if not (start_time <= start <= end_time):
                continue

        for label in instance.findall("label"):
            text_element = label.find("text")
            if text_element is not None and text_element.text:
                label_types.add(text_element.text.strip())

    # -------------------------
    # PASS 2 — Collect players
    # -------------------------
    for instance in root.findall(".//instance"):
        start = float(instance.find("start").text)
        end = float(instance.find("end").text)

        if start_time is not None and end_time is not None:
            if not (start_time <= start <= end_time):
                continue

        code = instance.find("code")
        if code is None or not code.text:
            continue

        player_name = code.text.strip()

        if player_name not in label_types:
            players.add(player_name)

    if not players:
        raise Exception("No players found in selected time range.")

    df = pd.DataFrame({"Player": sorted(players)})
    df.set_index("Player", inplace=True)

    for label in label_types:
        df[label] = 0

    # -------------------------
    # PASS 3 — Accumulate
    # -------------------------
    for instance in root.findall(".//instance"):
        start = float(instance.find("start").text)
        end = float(instance.find("end").text)

        if start_time is not None and end_time is not None:
            if not (start_time <= start <= end_time):
                continue

        code = instance.find("code")
        if code is None or not code.text:
            continue

        player_name = code.text.strip()

        if player_name not in df.index:
            continue

        for label in instance.findall("label"):
            text_element = label.find("text")
            if text_element is None or not text_element.text:
                continue

            label_text = text_element.text.strip()
            if label_text in df.columns:
                df.loc[player_name, label_text] += 1

    df.reset_index(inplace=True)

    # Output naming
    base_name = os.path.splitext(xml_path)[0]
    if end_time is not None:
        output_path = f"{base_name}_output_{int(end_time)}.xlsx"
    else:
        output_path = f"{base_name}_output.xlsx"

    df.to_excel(output_path, index=False)

    return output_path

