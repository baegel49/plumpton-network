#!/usr/bin/env python3
"""
Convert TNP_DATA (Plumpton Letters) into the file formats expected by
the Tudor Networks of Power analysis pipeline (Chapters 2-7).

Input:  TNP_DATA/letter_edgelist.tsv
        TNP_DATA/people_labels.tsv
        TNP_DATA/places_labels.tsv
        TNP_DATA/places_metadata.tsv

Output: Converted data files distributed to each chapter directory.
"""

import os
import shutil
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
TNP = os.path.join(BASE, 'TNP_DATA')


def read_tsv(filename, skip_header=True):
    """Read a TSV file, optionally skipping the #-prefixed header."""
    rows = []
    with open(os.path.join(TNP, filename)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if skip_header and line.startswith('#'):
                continue
            rows.append(line.split('\t'))
    return rows


def convert_date(date_int):
    """
    Convert a date from 'days since 1 Jan 1400' to YYYYMMDD string.
    0 means unknown -> '00000000'.
    """
    val = int(date_int)
    if val == 0:
        return '00000000'
    from datetime import date, timedelta
    epoch = date(1400, 1, 1)
    d = epoch + timedelta(days=val)
    return d.strftime('%Y%m%d')


def build_fromto(edges, places):
    """
    Build fromto_all_place_mapped_sorted from letter_edgelist.tsv.

    Target format (8 columns, tab-separated, sorted by DATE_FROM):
      SENDER_ID  RECIPIENT_ID  DATE_FROM  DATE_TO  MS_ID  PLACE_NAME  XML_PATH  MS_REF

    The Plumpton data has no XML paths, so we use '-' as placeholder.
    Place IDs are resolved to place names (or '-' if unknown/0).
    """
    lines = []
    for row in edges:
        sender = row[0]
        recipient = row[1]
        date_from = convert_date(row[2])
        date_to = convert_date(row[3])
        ms_id = row[4]
        place_id = row[5]
        ms_ref = row[6] if len(row) > 6 else ms_id

        place_name = places.get(place_id, '-')
        if place_name == 'Unknown':
            place_name = '-'

        # XML path placeholder (Plumpton data has no XML files)
        xml_path = '-'

        lines.append((date_from, f'{sender}\t{recipient}\t{date_from}\t{date_to}\t{ms_id}\t{place_name}\t{xml_path}\t{ms_ref}'))

    # Sort by date_from (string sort works for YYYYMMDD), then by sender
    lines.sort(key=lambda x: x[0])
    return [l[1] for l in lines]


def build_people_docs(edges, people):
    """
    Build people_docs_auto from letter_edgelist.tsv and people_labels.tsv.

    Target format (4 columns, tab-separated):
      PERSON_ID  PERSON_NAME  DOC_COUNT_OR_ALIAS  DOC_REFS

    The script reads: l[0]=ID, l[1]=name, l[2]=alias/count, l[3]=doc_refs
    For Plumpton data we use PERSON_ID as the alias field and list MS_IDs.
    """
    # Collect documents per person
    person_docs = defaultdict(list)
    for row in edges:
        sender = row[0]
        recipient = row[1]
        ms_id = row[4]
        person_docs[sender].append(ms_id)
        person_docs[recipient].append(ms_id)

    lines = []
    for pid, name in sorted(people.items(), key=lambda x: int(x[0])):
        docs = person_docs.get(pid, [])
        # Use person ID as the alias field (single value, no commas/semicolons)
        lines.append(f'{pid}\t{name}\t{pid}\t{" ".join(docs)}')

    return lines


def build_empty_file():
    """Return empty content for added_people and renamed_people."""
    return []


def build_final_women():
    """Return empty women list (needs manual curation for Plumpton data)."""
    return []


def build_cleanlinkeddata():
    """Return empty linked data file."""
    return []


def distribute_file(content, filename, destinations):
    """Write content to all destination directories."""
    for dest in destinations:
        path = os.path.join(BASE, dest, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('\n'.join(content))
            if content:
                f.write('\n')
        print(f'  Written: {path}')


def main():
    print('Reading TNP_DATA...')

    # Read source data
    edges = read_tsv('letter_edgelist.tsv')
    people_raw = read_tsv('people_labels.tsv')
    places_raw = read_tsv('places_labels.tsv')

    # Build lookup dicts
    people = {row[0]: row[1] for row in people_raw}
    places = {row[0]: row[1] for row in places_raw}

    print(f'  {len(edges)} letters, {len(people)} people, {len(places)} places')

    # Convert to target formats
    print('\nConverting...')
    fromto = build_fromto(edges, places)
    people_docs = build_people_docs(edges, people)
    added = build_empty_file()
    renamed = build_empty_file()
    women = build_final_women()
    linked = build_cleanlinkeddata()

    # Define where each file needs to go
    fromto_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
        'CHAPTER_2',
        'CHAPTER_4',
        'CHAPTER_5',
        'CHAPTER_6',
        'CHAPTER_7',
    ]

    people_docs_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
        'CHAPTER_2',
        'CHAPTER_4',
        'CHAPTER_5',
        'CHAPTER_6',
        'CHAPTER_7',
    ]

    added_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
        'CHAPTER_2',
        'CHAPTER_4',
        'CHAPTER_5',
        'CHAPTER_6',
        'CHAPTER_7',
    ]

    renamed_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
        'CHAPTER_2',
        'CHAPTER_4',
        'CHAPTER_5',
        'CHAPTER_6',
        'CHAPTER_7',
    ]

    women_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
    ]

    linked_destinations = [
        'CHAPTER_2/Network_Analysis_Tool',
    ]

    # Distribute files
    print('\nDistributing files...')

    print('\n--- fromto_all_place_mapped_sorted ---')
    distribute_file(fromto, 'fromto_all_place_mapped_sorted', fromto_destinations)

    print('\n--- people_docs_auto ---')
    distribute_file(people_docs, 'people_docs_auto', people_docs_destinations)

    print('\n--- added_people ---')
    distribute_file(added, 'added_people', added_destinations)

    print('\n--- renamed_people ---')
    distribute_file(renamed, 'renamed_people', renamed_destinations)

    print('\n--- final_women.out ---')
    distribute_file(women, 'final_women.out', women_destinations)

    print('\n--- cleanlinkeddata.out ---')
    distribute_file(linked, 'cleanlinkeddata.out', linked_destinations)

    print('\nDone! Plumpton data has been converted and distributed.')
    print('\nNotes:')
    print('  - final_women.out is empty (needs manual curation for Plumpton data)')
    print('  - cleanlinkeddata.out is empty (no linked authority data for Plumpton)')
    print('  - bigrank.out will be generated when you run the Network Analysis Tool')
    print('  - The "period" file in Chapter 2 may need updating for Plumpton date ranges')


if __name__ == '__main__':
    main()
