import sqlite3
import math
from decimal import Decimal

def midi_to_note_name(midi_note):
    midi_note = round(midi_note)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = notes[int(midi_note % 12)]
    octave = int((midi_note - 12) / 12)
    return f"{note_name}{octave}"

def hz_to_note_name(frequency):
    midi_note = 12 * math.log2(frequency / 440) + 69
    note_name = midi_to_note_name(midi_note)
    return note_name

def get_overtones(note_name, octave, num_overtones):
    # notes used are in the 0th octave
    notes = {
        'C': 16.35160,
        'C#': 17.32391,
        'D': 18.35405,
        'D#': 19.44544,
        'E': 20.60172,
        'F': 21.82676,
        'F#': 23.12465,
        'G': 24.49971,
        'G#': 25.95654,
        'A': 27.50000,
        'A#': 29.13524,
        'B': 30.86771,
    }
    #multiply frequency of 0th octave by the octave requested
    frequency = notes[note_name] * (2**(int(octave)))
    #round frequency to 2 digits
    frequency = round(Decimal(frequency), 2)

    overtones = [frequency * (1 + n) for n in range(1, num_overtones + 1)]
    return overtones

if __name__ == "__main__":
    # Connect to the database
    conn = sqlite3.connect('notes.db')

    # Create the notes table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            overtones TEXT NOT NULL
        );
    ''')

    num_overtones = int(input("Enter the number of overtones to generate: "))

    #Populate the notes table with MIDI note numbers
    midinotes = range(21, 128)
    for midinote in midinotes:
        note_name = midi_to_note_name(midinote)
        overtones = get_overtones(note_name[:-1], note_name[-1], num_overtones)
        
        for idx, _ in enumerate(overtones):
            name = hz_to_note_name(overtones[idx])
            overtones[idx] = f"{name}: " + str(overtones[idx])
        
        #Merge overtones list into a single string
        overtone_str = ",".join(overtones)

        conn.execute('''
            INSERT INTO notes (name, overtones)
            VALUES (?, ?)
        ''', (note_name, overtone_str))
       

    # Commit the changes and close the connection
    conn.commit()
    conn.close()