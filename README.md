# MelbourneEspressoHTMX

This is the main repo for all files required for hosting a [melbourneespresso.com](https://melbourneespresso.com)-style web application (new rewrite in Flask/HTMX).

## What is Melbourne Espresso?

Melbourne Espresso is a web app that I built that shows good toilet and coffee locations in Melbourne. It currently uses very very very rudimentary authentication so that I can keep it to be viewable only by friends (might make it fully public in future).

The web app uses what I've stupidly dubbed the `PFfHhhh Stack` (as in the noise you make when exhaling loudly from pursed lips in disbelief); this stack uses the following technologies:

 - [Postgres](https://www.postgresql.org/)
 - [Flask](https://github.com/pallets/flask)
   - **(optional)** [Fly.io](https://fly.io/) (for hosting since it's just so easy!)
 - [HTMX](https://github.com/bigskysoftware/htmx)
 - *and most importantly*: `hours` of work wrangling HTML/CSS/JS into line

## Dependencies

This project is not a complete repo as for the sake of copyright licences, etc I have left out all external libs, fonts and the images that I made. However, adding them back is quite simple. Create the following folders under `static/`:
- `fonts` (for your fonts, this project uses `GoogleFonts DMSans-Regular`)
- `images` (for images, favicon, etc)
- `lib` (for [HTMX](https://github.com/bigskysoftware/htmx) and [LeafletJS](https://github.com/Leaflet/Leaflet) and any other libraries you want)

## Running

If you want to run Melbourne Espresso, it's reasonably simple. 

To begin with, clone this repo:
```nu-script
git clone https://github.com/Ash-Olorenshaw/MelbourneEspressoHTMX.git
cd MelbourneEspressoHTMX
```

Next, you'll need a `.env` file. Your `.env` file must have the following fields:

```python
DB_NAME=      # database name
DB_USER=      # database username
DB_PWD=       # database password
DB_HOST=      # database host
DB_PORT=      # database port

LOGIN_PWD=    # your desired application password

TOILET_TABLE= # db table name for toilet info
CAFE_TABLE=   # db table name for cafe info
```

Your Postgres DB should be then populated with a Cafe table that has the following columns:

**Title** | **Longtitude** | **Latitude** | **Address** | **Coffee** | **Size** | **Price** | **Matcha** | **Chai** | **Notes**

And the toilet table should contain the following:

**Title** | **Longtitude** | **Latitude** | **Address** | **Notes**

After that, create a Python Virtual Environment like this:

```nu-script
python3 -m venv venv
```

Activate it and then install the required dependencies:

```nu-script
# *nix
. ./venv/bin/activate
# Windows (PowerShell)
./venv/Scripts/activate.ps1

pip install -r requirements.txt
```

Then run the server!

```nu-script
python3 -m flask run --host=0.0.0.0 --port=8080
```
