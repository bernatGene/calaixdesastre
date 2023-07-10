from pathlib import Path
import argparse
import requests
import yaml


def list_index(index_path, pages_path):
    index_list = Path(index_path).read_text().splitlines()
    for entry in index_list:
        if entry.startswith("#"):
            continue
        entry = entry.rstrip()
        content = entry[entry.rfind("[")+1:entry.find("]")]
        year = content[content.find("(")+1:content.rfind(")")]
        title = content[:-7]
        if " - " in title: # Original name - translated or viceversa
            title = title[:title.find(" - ")]
            print(title)
        
        page = (Path(pages_path) / (content + ".md"))
        print(page)
        if page.exists() and len(page.read_text()) > 0:
            print("Already a non-empty entry. continuing", title)
            continue
        else:
            info = get_film_data_format(title, year)
            page.write_text(info)

    Path(index_path).write_text("\n".join(sorted(index_list)))


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
    parser.add_argument('-ip', '--index_path')
    parser.add_argument('-pd', '--pages_path')
    args = parser.parse_args()
    list_index(args.index_path, args.pages_path)


if __name__ == "__main__":
    main()





