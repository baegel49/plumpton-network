### Plumpton Letters and Papers - Network Dataset (Kirby edition)

Derived from Joan Kirby (ed.), *The Plumpton Letters and Papers*
(Camden Fifth Series, vol. 8, Cambridge University Press, 1996).

Format follows Ahnert & Ahnert, *Tudor Networks of Power* (OUP, 2023).

---

**Scope**: 230 letters extracted (of 252 total in Kirby), c.1450–1552.

**Files**:
- `letter_edgelist.tsv` — Directed temporal edge list (230 letters)
- `people_labels.tsv` — Person ID → Name (125 individuals)
- `places_labels.tsv` — Place ID → Name (30 places)
- `places_metadata.tsv` — Place ID, latitude, longitude

**Date encoding**: Days since 1 January 1400. Value of 0 = unknown date.

**Known limitations**:
- 22 letters (of 252) not captured due to OCR noise in header lines.
- Place of writing is not yet extracted (PLACE_ID = 0 for all).
  Extractable from full letter text in a second pass.
- A small number of letter numbers are OCR-garbled (e.g. "7" read as "4").
- Earl of Northumberland not disambiguated by individual (4th vs 5th Earl).
  Could be split using date ranges: 4th Earl d.1489, 5th Earl 1489–1527.
- Some approximate dates assigned to 1 Jan of the estimated year.

**Key actors** (by frequency):
- Sir Robert Plumpton (recipient of 153 letters)
- Sir William Plumpton (recipient of 27 letters)
- William Plumpton, son (25 letters, as sender or recipient)
- Earl of Northumberland (24 letters as sender)
- Edward Plumpton (20 letters as sender)
- Dame Agnes Plumpton (11 letters)
- Isabel Plumpton, née Babthorpe (11 letters)
- Robert Plumpton, kinsman (9 letters)
- German de la Pole (8 letters)
- Sir William Gascoigne (8 letters)
- Godfrey Greene (7 letters)
- Robert Eyre III (6 letters)

**Citation**:
Kirby, J. (ed.), *The Plumpton Letters and Papers*
(Camden Fifth Series, vol. 8, Royal Historical Society, 1996).

**Generation script**: `build_plumpton_v2.py`
