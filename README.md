# EPCOT Wait Time Tracker

A simple, free, automated tracker for EPCOT ride wait times, built to learn
the basics of scheduled data collection and static web hosting.

## How it works
1. `.github/workflows/fetch.yml` tells GitHub to run `scripts/fetch_waits.py`
   automatically every hour.
2. The script calls the free Queue-Times.com API for EPCOT (park ID 5),
   averages the current wait times, and appends one record to
   `data/epcot_waits.json`.
3. GitHub Actions commits that updated file back to the repo.
4. `index.html`, hosted for free via GitHub Pages, reads that data file
   and displays a chart plus a "best day to visit" recommendation.

## Cost
$0. GitHub Actions free tier and GitHub Pages free tier cover this
comfortably at this scale.

## Data source
Powered by Queue-Times.com (https://queue-times.com) — free API, no key
required, attribution required.
