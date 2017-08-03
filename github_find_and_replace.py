from selenium import webdriver
from time import sleep

'''
Originally by Angello Maggio @ JFrog, August 2nd, 2017
This script searches through a specified GitHub in a DFS
manner, looking for any file containing a specified filter.
It will then look through these files found, and find the ones
with the specific to_find value. After that it will look
in your home_path for the file, and modify them for you
changing all the to_find values to the to_repalce values.

Right now it only work for readme files.
'''

base_url = "https://github.com/JFrogDev/artifactory-user-plugins"
base_path = "/Users/angellom/artifactory-user-plugins/"
home_path = "/Users/angellom/artifactory-user-plugins/"
# Variables to find and replace
to_find = '|'
to_replace = ';'
_filter = "README.md"

def main():

    # Start browser
    ch = webdriver.Chrome()




    # Global holders of readme files and file links we've already seen
    readme_links = []
    files = []
    # The script will pick up the branches as links and will create an infinite loop, so we avoid all branches but the master
    branches = ['development', 'documentation_and_tests', 'mark-new-rest-demo', 'pommerv2', 'provisional']

    # Make these variables global
    global readme_links, files, branches

    # Get started on the main page
    find_filter(ch, base_url)

    print "readme links"
    print readme_links

    links_with_result = narrow_down(ch, readme_links)
    find_in_system(links_with_result)


def find_filter(ch, url):

    # Open the page you are looking for
    ch.get(url)

    # Get global variables and then sleep 3 seconds so GitHub doesn't kick me out
    global readme_links, files
    sleep(3)

    print "Inside findReadMe for url ", url

    # Find all the file elements (this includes branches and what not)
    files_directories = [x.get_attribute("href") for x in ch.find_elements_by_class_name("js-navigation-open")]

    # Go over each one
    for file_url in files_directories:

        _flag = True

        # This is the url split by directory
        file_dir_name = file_url.split('/')

        # If the file is a _filter file
        if _filter in file_dir_name[-1]:
            # save it
            if file_url not in readme_links:
                readme_links.append(file_url)
                print readme_links

        # If the file doesn't have an extension or is not the LICENSE file
        elif ('.' not in file_dir_name[-1]) and ('LICENSE' not in file_dir_name[-1]) and (file_dir_name[-1] not in branches):

            for i in range(0, len(file_dir_name)):
                if file_dir_name[i] in branches:
                    _flag = False

            if file_url not in files and _flag:
                print file_dir_name
                files.append(file_url)
                find_filter(ch, file_url)


def narrow_down(ch, urls):
    answer =[]
    for url in urls:
        ch.get(url)
        try:
            text = ch.find_element_by_class_name("readme").text
            if to_find in text:
                answer.append(url)
                print url
        except:
            print "Could not find for:", url
    return answer


def find_in_system(urls):
    paths = []


    for item in urls:
        split_item = item.split('/')
        path = home_path + '/'.join(split_item[7:])
        print path
        paths.append(path)

    for file_path in paths:
        # Read in the file
        with open(file_path, 'r') as file:
          filedata = file.read()
        # Replace the target string
        filedata = filedata.replace(to_find, to_replace)
        print filedata

        # Write the file out again
        with open(file_path, 'w') as file:
          file.write(filedata)


if __name__ == '__main__':
    main()
