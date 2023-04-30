import argparse
import sqlite3
import sys

def get_overtones(note_name):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT notes.overtones FROM notes WHERE name = '{note_name}';")
    result = cursor.fetchone()
    conn.close()
    #result is originally a single string inside of a tuple. It needs to be a list for later comparisons
    return (result[0].split(","))

def make_ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(int(n) % 10, 4)]
    return str(n) + suffix

def extract_note_names(toneList):
    for idx, tone in enumerate(toneList):
        toneList[idx] = tone.split(":")[0]
    return toneList

def is_overtone(note_name, reference_note):
    overtones = get_overtones(reference_note)
    overtones = extract_note_names(overtones)

    if note_name in overtones:
        #Add one for ordinal counting and to prevent index of 0 from triggering false for "if result"
        return overtones.index(note_name) + 1
    
    #If note not in overtones, return false
    return False
    

def share_overtones(note1, note2):
    overtonesN1 = get_overtones(note1)
    overtonesN2 = get_overtones(note2)

    overtonesN1 = extract_note_names(overtonesN1)
    overtonesN2 = extract_note_names(overtonesN2)

    #set is used to remove duplicates
    if bool(set(overtonesN1) & set(overtonesN2)):
        return (set(overtonesN1) & set(overtonesN2))
    #If no notes are shared, return False
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('note', nargs='*')
    parser.add_argument('-l', '--list-overtones', action='store_true', help="List the overtones for the specified notes")
    parser.add_argument('-c', '--check-overtones', nargs='+', help="Check if any of the notes after the flag are overtones of the note before the flag")
    parser.add_argument('-s', '--share-overtones', nargs='+', help="Check if any of the notes after the flag share overtones with the note before the flag")
    
    #parse the command-line arguments
    args = parser.parse_args()

    #If there are no notes in the arguments, raise exception
    if args.note == []:
        raise Exception("No notes specified")

    if args.check_overtones:
        reference = args.note
        for refnote in reference:
            fail_list = []
            for checkednote in args.check_overtones:
                result = is_overtone(checkednote, refnote)
                if result:
                    print(f"{checkednote} is the {make_ordinal(result)} overtone of {refnote}")
                else:
                    fail_list.append(checkednote)
            print(f"{fail_list} are not overtones of {refnote}")
            print("---------")

    if args.share_overtones:
        reference = args.note
        for refnote in reference:
            for note in args.share_overtones:
                result = share_overtones(refnote, note)
                if result:
                    print(f"{refnote} and {note} both have the following overtones: {result}")
                else:
                    print(f"{refnote} and {note} do not share overtones")
            print("---------")

    if args.list_overtones:
        reference = args.note
        for refnote in reference:
            overtones = get_overtones(refnote)
            print(f"The overtones of {refnote} are {overtones}")
