"""V2 scraper for Tesco groceries."""

from scraper.saver import save_to_csv

from ninjas.tesco import extract_tesco

def main()->None:
    """Main program function."""
    tesco_items = extract_tesco()
    save_to_csv(tesco_items, "tesco.csv")

if __name__ == "__main__":
    main()
