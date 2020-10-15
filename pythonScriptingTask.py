#!user/bin/env python3

import requests
import argparse
import re
import validators

""" Contains the all the functions for the python scripting tasks in DAT234 """

subdomain_file = "subdomains.txt"
subdomains = []
alive = []
not_alive = []
domains = []

print(not_alive)
print(alive)
print(subdomains)


class CrtSh:
    def __init__(self, url: str):
        print("init")
        """
        __init__ [summary]

        [extended_summary]

        Args:
            url (type: string): [url??.. fill in more here]
        """
        self.url = url
        print("URLEN SOM BLE SKREVET INN:", url)

    def task_1(self, url):
        """
        checks if url is valid and returns a response

        Params:
        - url: (type: string) an url

        Returns:
        - response [type: string]: [return http response code]
        """
        """ Checks if contains https or not. adds https:// at start if it does not contain it """
        new_url = self.check_if_contains_https(url)
        """ Checks if its an valid url with validators dependency """

        valid = validators.url(new_url)
        """ 
        if valid makes a request to the url and returns the response
        if not valid prints out 'Invalid url' 
        """
        domains.append(new_url)
        print(domains)
        if valid == True:
            response = requests.get(new_url)
            print("Got response. code: ", response)
            return response
        else:
            print("Invalid url")

    def task_2(self):
        pass

    def task_3(self):
        """ 
        Split the domains 
        Scan each subdomain
        Store them in a list

        Params:
        - url: (type: string) an url

        Returns:
        - 
        """
        file = open(subdomain_file)
        subdomains = file.read().splitlines()
        print(subdomains)
        i = 0

        for subdomain in subdomains:
            i = i + 1
            if subdomain != True:
                subdomain_url = f'https://{subdomain}'
                valid = validators.url(subdomain_url)
                if valid == True:
                    try:
                        response = requests.get(subdomain_url)
                        if response.status_code == 200:
                            alive.append(subdomain_url)
                        else:
                            not_alive.append(subdomain_url)
                    except requests.exceptions.RequestException as error:
                        print("connection error", error)
                        not_alive.append(subdomain_url)
                        pass
                    finally:
                        print(i, '[$] Your target domain :- ', subdomain_url)
                else:
                    print("not valid url: ", subdomain_url)
                    break
            else:
                break
        print("Total subdomains: ", len(subdomains))
        print("----------")
        print("ALIVE SUBDOMAINS: ", alive)
        print("----------")
        print("NOT ALIVE SUBDOMAINS: ", not_alive)
        print("----------")

        print(len(alive), "is alive | ", len(not_alive),
              "is not alive | Difference is: ", len(alive)-len(not_alive))

    def task_4(self):
        """ asd """
        pass

    def task_5(self):
        """ asd """
        pass

    def task_6(self):
        """ Prints out the list and calculates the difference in alive and dead subdomains """
        pass

    def check_if_contains_https(self, url):
        """ Checks if the url contains https://. if not adds it to the url """
        url_start = "https://"
        search_url = re.search(url, url_start)
        if search_url is None:
            new_url = "https://" + url
            print(new_url)
            return new_url
        else:
            return self


if __name__ == "__main__":
    """ Make a argument parser """
    parser = argparse.ArgumentParser(description="crt_sh subdomain searcher")
    """ add in option(s) for the argument parser """
    parser.add_argument('-dn', '--domain',
                        help="What url do you want to check?", type=str)

    args = parser.parse_args()
    if not args.domain:
        url_input = input("Enter an URL you want to check: ")
        crt_sh = CrtSh(url_input)
        # crt_sh.task_1(url_input)
        crt_sh.task_3()
    else:
        crt_sh = CrtSh(parser)
        print(crt_sh.task_1(args.domain))
