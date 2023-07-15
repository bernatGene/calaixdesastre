from pathlib import Path
import argparse
import requests
import yaml


def list_index(index_path, pages_path, add=None, delete=None):
    index_list = Path(index_path).read_text().splitlines()
    to_delete_index = None
    for i, entry in enumerate(index_list):
        if entry.startswith("#"):
            continue
        entry = entry.rstrip()
        content = entry[entry.rfind("[")+1:entry.find("]")]
        if "|" in content: # Name includes path
            content = content[content.find("|")+1:]
            print("Contains path", content)
        year = content[content.find("(")+1:content.rfind(")")]
        title = content[:-7]
        if " - " in title: # Original name - translated or viceversa
            title = title[:title.find(" - ")]
        
        print(title.strip(), delete, title == delete)
        if title.strip() == delete:
            to_delete_index = i
        
        page = (Path(pages_path) / (content + ".md"))
        print(page)
        if page.exists() and len(page.read_text()) > 0:
            print("Already a non-empty entry. continuing", title)
            continue
        else:
            info = get_film_data_format(title, year)
            page.write_text(info)

    if to_delete_index is not None:
        print("deleteing", delete, "from wathcilist")
        delete = index_list.pop(to_delete_index)
    elif delete is not None:
        print("Could not find movie to delete", delete)
        delete = None

    if add is not None:
        print("adding", add, "to seen")
        index_list.append(add)

    Path(index_path).write_text("\n".join(sorted(index_list)))

    return delete
        


def get_film_data_format(title, year, api_key="d00ac1f4"):
    url = f"http://www.omdbapi.com/?t={title}&y={year}&apikey={api_key}"
    response = requests.get(url).json()
    if response["Response"] == "False" or "Error" in response:
        print("There was an error", response, title, year)
        print("-"*50)
        return "Automatic search failed"
    
    def comma_list_2_list_of_links(string):
        return  ", ".join([f'[[{t}]]' for t in string.split(", ")])

    info = {
        "Title": response["Title"],
        "Year": response["Year"],
        "Language": comma_list_2_list_of_links(response["Language"]),
        "Director": comma_list_2_list_of_links(response["Director"]),
        "Runtime": response["Runtime"],
        "Ratings": response["Ratings"],
        "Plot": response["Plot"],
    }
    info = yaml.dump(info, allow_unicode=True)
    return info


def main():
    parser = argparse.ArgumentParser("Build film index")
    parser.add_argument('-is', '--seen', default="/Users/bernatskrabec/Vault/filmstuff/Seen films.md") 
    parser.add_argument('-iw', '--watchlist', default="/Users/bernatskrabec/Vault/filmstuff/Watchlist.md") 
    parser.add_argument('-pd', '--pages_dir', default="/Users/bernatskrabec/Vault/filmstuff/films")
    parser.add_argument('-s', "--aseen", default=None)
    args = parser.parse_args()
    deleted = list_index(args.watchlist, args.pages_dir, None, args.aseen)
    list_index(args.seen, args.pages_dir, deleted, None)
    print("done")


if __name__ == "__main__":
    main()





