'''
file: HTTPParser.py
language: python3
author: Zaki Bawade
description: HTML parser takes a link as an argument and prints out external links along with their count
'''
import sys
import parserforurl

def verify_url(link):
    """Verify the user entered link
    
    Parameters
    ----------
    link : string
        link to be verified

    Returns
    -------
    Nothing    
    
    """
    if len(link) < 2:
        print("Invalid Argument")
        exit(1)
    

    if "://" not in link:
        print("Invalid URL")
        exit(1)

    

    if "http" not in link and "https" not in link:
        print("Invalid URL")
        exit(1)

def print_url(url_list,link):
    """Prints the external links for the original link that user provided
    
    Parameters
    ----------
    link : string
        original link to be compared and removed from the external link list
    
    url_list : list
        list of unique urls found in the html code of the link
    Returns
    -------
    Nothing
    
    """
    for i in url_list:
        if link in url_list:
            url_list.remove(link)
    for item in url_list:       
        print(item+"\n")
    print("**********************************************\n")
    print("External references found: " + str(len(url_list)) )
    print("**********************************************\n")


def main():
    link = sys.argv[1]
    verify_url(link)
    host, req, c_type = parserforurl.connect(link)
    sock = parserforurl.setup_http_https(c_type,host)
    response = parserforurl.response(sock,req)
    url_list=[]
    url_list=parserforurl.urlparser(response)
    print_url(url_list,link)

main()