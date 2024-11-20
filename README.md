# Crossref DOI Generator

Scripts to aid in minting Crossref DOIs

## Install

```
pipx install tamu_crossref
```

## Running

```
crossref generate -c myrecords.csv -o briefs.xml -d reports
```

## Testing DOIs before Upload to Crossref

You can test files before you upload to Crossref.  To do this, mkdir called `dois` and cp your xml to it:

```
mkdir dois
cp my.xml dois
```

Then, run pytest:

```
pytest
```
