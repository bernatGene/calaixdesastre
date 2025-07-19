from isbnlib import meta, is_isbn10, is_isbn13
from isbnlib.registry import bibformatters


SERVICE = "openl"
bibtex = bibformatters["bibtex"]

def get_isbn(entry):
        entry = entry.strip("-")
        isbn = entry.strip()
        if is_isbn10(isbn) or is_isbn13(isbn):
            res = meta(isbn, SERVICE)
            if res is not None:
                try:
                    print(bibtex(res))
                except AttributeError:
                    print(res)
            else:
                print("Not found")
        else:
            print("Bad format")


def main():
      entry = input("ISBN: ")
      get_isbn(entry)

if __name__ == "__main__":
       main()
