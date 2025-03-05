"""V2 scraper for Tesco groceries."""

from ninjas.tesco import extract_tesco

from common.utils import debug

from scraper.saver import save_to_csv, save_to_cloud

def main()->None:
    """Main program function."""
    debug("Started program execution")
    tesco_items = extract_tesco()
    save_to_csv(tesco_items, "output/products.csv")
    save_to_cloud(tesco_items)


if __name__ == "__main__":
    main()
