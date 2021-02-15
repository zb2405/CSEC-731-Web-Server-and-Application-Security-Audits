'''
file: Request_Parser.py
language: python3
author: Zaki Bawade
description: Reads an HTTP request from a text file and validates the syntax of the request
'''

import sys


def file_read(fname):
    """
    Opens the text file and reads the HTTP request into lists
    
    Parameters:
    fname : String
        filename to be read

    Returns:
    List
        Lists with http request and message body 
    """

    http_request = []
    message_body = []

    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            http_request.append(line.strip())
            if "Connection:" in line:
                break

    f.close()
    with open(fname, 'r') as f:
        for line in f:
            if 'Connection:' in line:
                for line in f:
                    message_body.append(line.strip())
    f.close()
    message_body.pop(0)
    return http_request, message_body


def parse_read(request):
    """
    Parses the HTTP request to obtain the request line, Request-URI, request method, HTTP version, request line and the request headers
    
    Parameters:
    request : List
        request to be parsed

    Returns:
    String
        request line, Request-URI, request method, HTTP version, request line
    List
        request headers
    """
    
    
    request_line = request.pop(0)
    request_headers = [req.split(' ', 1)[0] for req in request]
    req_line = request_line
    request_line = request_line.split(" ")
    method = request_line[0]
    uri = request_line[1]
    http_ver = request_line[2]

    return (request_headers, method, uri, http_ver, req_line)


def method_check(method):
    """
    Validates the Request method of the request line. If the method is not valid error 400 is thrown
    Source: (RFC 7231 pg 21)
    
    Parameters:
    method : String
        request method

    Returns:
    Nothing
    
    """    
    attributes = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH",
                  "POST", "PUT", "TRACE"]
    if method not in attributes:
        response_400()


def headers_check(request_headers, msg_body):
    """
    Validates the Request headers of an HTTP request,  
    Error 400 will be thrown in following cases:
    
    1) request header is not followed by a ":" (RFC 7230 pg 21 section 3.2)
    2) There is a " " between request header and the ":" (RFC 7230 pg 24 section 3.2.4)
    3) The Host header is absent (RFC 2616 pg 128 and pg 171)
    4) Content-Length header is present in absence of a message body (RFC 2616 pg 33)
    
    Parameters:
    method : String
        request method

    Returns:
    Nothing
    
    """ 
    for headers in request_headers:
        if headers.count(":") != 1:
            response_400()
    for headers in request_headers:
        if headers[-1] != ":":
            response_400()
    if "Host:" not in request_headers:
        response_400()
    if len(msg_body) == 0:
        for headers in request_headers:
            if "Content-Length:" in request_headers:
                response_400()


def uri_check(uri):
    """
    Validates the Request-URI would be implemented later
    
    Parameters:
    uri : String
        Request-URI 

    Returns:
    Nothing
    """
    pass
    

def http_ver_check(http_ver):
    """
    Validates the http version in request line
    throws 400 error if the HTTP version is not valid
    (RFC 2616 pg 17)
    
    Parameters:
    http_ver : String
        HTTP version from the request line 

    Returns:
    Nothing
    
    """
    
    http_attributes = ["HTTP/0.9", "HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
    if http_ver not in http_attributes:
        response_400()


def req_line_check(req_line):
    """
    Validates the request line
    throws 400 error if the request line does not ccontains 2 spaces as per the syntax
    (RFC 2616 pg 34 section 5.1)
    
    Parameters:
    req_line : String
        request line 

    Returns:
    Nothing
    """
    if req_line.count(" ") != 2:
        response_400()


def check_content_length(request_headers):
    """
    Validates the Request headers to check if Content-Length header is present in presence of a message body (RFC 2616 pg 33)  
    
    Parameters:
    request_headers : List
        request headers

    Returns:
    Nothing
    """
    for headers in request_headers:
        if "Content-Length:" not in request_headers:
            response_400()


def response_200():
    """
    Prints HTTP 200 OK response and exits
    
    Parameters:
    Nothing

    Returns:
    Nothing
    """
	print("**********************************************\n")
	print("200 OK\n")
	print("**********************************************\n")
	exit(1)


def response_400():
    """
    Prints HTTP 400 BAD REQUEST response and exits
    
    Parameters:
    Nothing

    Returns:
    Nothing
    """
	print("**********************************************\n")
	print("400 BAD REQUEST\n")
	print("**********************************************\n")
	exit(1)


def response_500():
    """
    Prints HTTP 500 INTERNAL SERVER ERROR response and exits
    
    Parameters:
    Nothing

    Returns:
    Nothing
    """
	print("**********************************************\n")
	print("500 INTERNAL SERVER ERROR\n")
	print("**********************************************\n")
	exit(1)


def main():
    try:
        http_req = []
        if len(sys.argv) != 2:
            print("invalid arguments")
            exit(1)

        else:
            filename = sys.argv[1]
            http_req, msg_body = file_read(filename)

        request_headers, method, uri, http_ver, request_line = parse_read(http_req)
        req_line_check(request_line)
        if len(msg_body) != 0:
            check_content_length(request_headers)

        method_check(method)
        uri_check(uri)
        http_ver_check(http_ver)
        headers_check(request_headers, msg_body)
        response_200()

    except Exception:
        response_500()


main()
