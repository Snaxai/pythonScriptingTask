#!user/bin/env python3

import requests
import json
import click
import argparse
import re
import validators
from threading import Thread
from queue import Queue
import threading

""" Contains the all the functions for the python scripting tasks in DAT234 """

alive = []
not_alive = []

#q = JoinableQueue()
q = Queue()


class CrtSh:
    def __init__(self, url: str):
        """
        inits class with an url

        Args:
            url (type: string): a domain
        """
        self.url = url
        print("URLEN SOM BLE SKREVET INN:", url)

    def task_1(self, url):
        """
        Checks if url is valid and returns a response

        If it is valid then it makes a request to the url and returns the response
        If not valid prints out 'Invalid url'

        Params:
        - url: (type: string) an url

        Returns:
        - response [type: string]: [return http response code]
        """
        # Checks if contains https or not. removes https:// if it does contain it
        new_url = self.check_if_contains_https(url)
        # Checks if its an valid url with validators dependency
        valid = validators.url(f"https://{new_url}")

        if valid == True:
            try:
                response = requests.get(f"https://{new_url}")
                print("Got response. code: ", response)
            except requests.exceptions.RequestException as error:
                print("Connection error", error)
                exit()
            finally:
                if response.status_code == 200:
                    print("passed")
                    return response
                else:
                    print("Did not get status 200")
                    exit()
        else:
            print("Invalid url")
            exit()

    def task_3(self, domain):
        """
        Finds and gets subdomains from crt.sh site

        Params:
        - domain: (type: string)

        Returns:
        - a list of subdomains
        """
        # Checks if contains https or not. removes https:// if it does contain it
        new_domain = self.check_if_contains_https(domain)
        try:
            crt_request = requests.get(
                f"https://crt.sh/?q=%.{new_domain}&output=json").json()
        except requests.exceptions.ConnectionError:
            click.secho("Failed to connect to CRT.SH, Try again.",
                        bold=True, fg="red")
        list_of_subdomains = []
        for i in range(len(crt_request)):
            list_of_subdomains.append(crt_request[i]['common_name'])

        list_of_subdomains = list(dict.fromkeys(list_of_subdomains))
        print(list_of_subdomains)

        print("Subdomains hentet fra crtsh:")
        print(list_of_subdomains, "\nLengden av denne listen er:",
              len(list_of_subdomains))
        return list_of_subdomains

    def task_4and5(self, domain):
        """
        Search through a list of subdomains to see if they respond
        store the results in 2 seperate lists

        Params:
        - url: (type: string) an url

        Returns:
        - 2 lists, alive and not_alive
        """
        i = 0
        subdomainlist = self.task_3(domain)

        for subdomain in subdomainlist:
            i = i + 1
            subdomain = f"http://{subdomain}"
            if subdomain != True:
                try:
                    response = requests.get(subdomain)
                    if response.status_code == 200:
                        print("try alive")
                        alive.append(subdomain)
                    else:
                        print("try not_alive")
                        not_alive.append(subdomain)
                except requests.exceptions.RequestException as error:
                    print("connection error", error)
                    not_alive.append(subdomain)
                    pass
                finally:
                    print(i, '[$] Your target domain :- ', subdomain)
            else:
                break
        print("Total subdomains: ", len(subdomainlist))
        print("----------")
        print("ALIVE SUBDOMAINS: ", alive)
        print("----------")
        print("NOT ALIVE SUBDOMAINS: ", not_alive)
        print("----------")

        print(len(alive), "is alive | ", len(not_alive),
              "is not alive | Difference is: ", len(subdomainlist)-len(alive))
        return alive, not_alive

    def check_if_contains_https(self, url):
        """ Checks if the url contains https://. if not adds it to the url 

            Params:
            - url (type: string) the url the user entered

            Return:
            - url (type: string) the url with https:// if it did not contain it already      
        """
        search_url = re.search("^https://", url)
        if search_url != None:
            new_url = url.replace("https://", "")
            print(new_url)
            return new_url
        else:
            return self.url

    # Et forsøk på multiprocessing / threading
    def multiproc(self, domain, subdomains):
        """
        Setup for the multiprocessing

        Params:
        - domain (type: string) a domain entered by the user
        - subdomain (type: list of strings) a list of subdomains
        """
        global q
        print("multi task_3")
        for subdomain in subdomains:
            q.put(subdomain)

        for t in range(8):
            proc = Thread(target=self.multiproctask_4and5, args=(domain,))
            proc.daemon = True
            proc.start()

    # Et forsøk på multiprocessing / threading
    def multiproctask_4and5(self, domain):
        """
        Finds potential subdomain with the help of multiprocessing
        """
        global q
        while True:
            subdomainlist = self.task_3(domain)

        for subdomain in subdomainlist:
            i = i + 1
            subdomain = f"http://{subdomain}"
            if subdomain != True:
                try:
                    response = requests.get(subdomain)
                    if response.status_code == 200:
                        print("try alive")
                        alive.append(subdomain)
                    else:
                        print("try not_alive")
                        not_alive.append(subdomain)
                except requests.exceptions.RequestException as error:
                    print("connection error", error)
                    not_alive.append(subdomain)
                    pass
                finally:
                    print(i, '[$] Your target domain :- ', subdomain)
            else:
                break
            q.task_done()


if __name__ == "__main__":
    """ Make a argument parser """
    parser = argparse.ArgumentParser(description="crt_sh subdomain searcher")
    """ Add in option(s) for the argument parser """
    parser.add_argument('-dn', '--domain',
                        help="What url do you want to check?", type=str)

    args = parser.parse_args()
    if not args.domain:
        url_input = input("Enter an URL you want to check: ")
        crt_sh = CrtSh(url_input)
        crt_sh.task_1(url_input)
        crt_sh.task_4and5(url_input)
    else:
        crt_sh = CrtSh(parser)
        print(crt_sh.task_1(args.domain))
        crt_sh.task_4and5(args.domain)
