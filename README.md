# Crossref DOI Generator

Scripts to aid in minting Crossref DOIs

## Install

```
pipx install tamu_crossref
```

## Running

You can generate DOIS like this:

```
crossref generate -c myrecords.csv -o briefs.xml -d reports
```

Or find DOIs like this:

```
crossref find -m "mark@example.com"
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
