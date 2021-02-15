'''
file: parserforurl.py
language: python3
author: Zaki Bawade
description: Connects to a user provided link and parses the html code of webpage to create a list of unique urls
'''

import socket
import ssl


def connect(link):

    """determines the type of connection to the link (HTTP or HTTPS) and generates a request to send to the end-server
    
    Parameters
    ----------
     link : string
        required to extract the host and connection type

    Returns
    -------
    host : string
        the host to send the request to
    req : string
        request to get an HTML response from the website
    connection_type : string
        defines http or https connection
    """
    connection_type = link.split("://")[0]

    url = link.split("//")[1]

    host = url.split("/")[0]

    page = url[len(host):]

    if page == "":
        page = "/"

    req = "GET " + page + " HTTP/1.1\r\n"
    req += "Accept-Encoding: identity\r\n"
    req += "Host: " + host + "\r\n"
    req += "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0\r\n"
    req += "Connection: Close\r\n\r\n"

    return host, req, connection_type


def setup_http_https(conn_type, host):
    """Establishes an http or https connection
    
    Parameters
    ----------
    conn_type : string
        based on this parameter the required socket is generated

    host : string
        the end website to which the connection will be established

    Returns
    -------
    socket
        to send data
    """

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if conn_type == "http":
        conn.connect((host, 80))
        return conn
    elif conn_type == "https":
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        s_conn = context.wrap_socket(conn, server_hostname=host)
        s_conn.connect((host, 443))
        return s_conn


def response(socket, req):
    """Send the generated request and get the response from the end server
    
    Parameters
    ----------
    socket : socket
        required to establish data transfer between the client and the server

    req : string
        request to get a response from end server

    Returns
    -------
    response : string
        String of data recieved from the end server
    """
    socket.send(req.encode())

    data = socket.recv(8192).decode(encoding="utf_8", errors="ignore")
    response = ""
    while data != "":
        response += data

        data = socket.recv(8192).decode(encoding="utf_8", errors="ignore")

    return response


def urlparser(response):
    """Parse the response from server to extract unique urls
    
    Parameters
    ----------
    response : string
        response generated and sent to client from server (basically HTML data of the webpage)

    Returns
    -------
    urls_no_duplicates : list
        list of external and internal unique urls parsed from the HTML code of the webpage
    """
    http_code = int(response.split(" ")[1])

    if http_code != 200:
        print("Error:" + str(http_code))
        exit(1)

    response = response.replace("><", ">\n<")

    """
    URL attributes list
    Source1: https://www.w3.org/TR/REC-html40/index/attributes.html
    Source2: https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value
    """
    url_attributes = ["action=", "src=", "cite=", "data=", "codebase=", "classid=", "href=", "manifest=",
                      "poster=", "longdesc=", "background=", "profile=", "srcset=", "code=", "usemap=", "formaction=",
                      "value="]
    urls = []
    keywords = ["https", "http", "www"]
    for data in response.split("\n"):

        for attribute in url_attributes:
            if attribute in data:
                # print(data)
                for text in data.split(" "):
                    if attribute in text:

                        url = text[text.find(attribute) + len(attribute):]

                        if len(url) != 0:

                            if url[1] != "/":

                                for word in keywords:
                                    if word in url:

                                        url = url.replace('"', '')
                                        url = url.replace("'", '')
                                        url = url.replace(">", '')
                                        url = url.replace("<", '')
                                        url = url.replace("\\", '')
                                        url_first_part = url.split("://")[0]
                                        try:
                                            url_rest_part = url.split("://")[1]
                                            split_characters = ["\\", "/", "?", ":"]
                                            for char in split_characters:
                                                if char in url_rest_part:
                                                    url_rest_part = url_rest_part.split(char)[0]
                                        except IndexError:
                                            continue

                                        # print(url_rest_part)

                                        urls.append(url_first_part + "://" + url_rest_part)
    urls_no_duplicates = []
    for item in urls:
        if item not in urls_no_duplicates:
            urls_no_duplicates.append(item)
    return urls_no_duplicates
