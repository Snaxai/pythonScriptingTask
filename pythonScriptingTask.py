#!user/bin/env python3

import requests
import argparse
import re
import validators
#import multiprocessing as mp
#from multiprocessing import Queue, Process, JoinableQueue
from threading import Thread
from queue import Queue
import threading

""" Contains the all the functions for the python scripting tasks in DAT234 """

# Skriver inn url
# sjekker om den er riktig
# sjekker subdomains -> legger dette i liste
# sjekker gjennom lista og kjører requests til hvert subdomain
# response 200 -> legger til i alive liste
# ikke response 200 -> legger til not_alive liste
# Printer ut alive og not_alive liste
# regner ut differansen og printer ut dette
# legge til riktig oppgave der den hører til

subdomainslist = []
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
        # Checks if contains https or not. adds https:// at start if it does not contain it
        new_url = self.check_if_contains_https(url)
        # Checks if its an valid url with validators dependency
        valid = validators.url(new_url)

        if valid == True:
            try:
                response = requests.get(new_url)
                print("Got response. code: ", response)
            except requests.exceptions.RequestException as error:
                print("connection error", error)
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

    def task_3(self, domain, subdomains):
        """
        Finds potential subdomains

        Params:
        - domain: (type: string) a domain

        Returns:
        - a list of subdomains
        """
        for subdomain in subdomains:
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url, timeout=100)
            except requests.ConnectionError:
                pass
            else:
                subdomainslist.append(url)
                print("[+] Discovered a subdomain:", url)

        print(subdomainslist)
        return subdomainslist

    def task_4and5(self):
        """
        Search through a list of subdomains to see if they respond
        store the results in 2 seperate lists

        Params:
        - url: (type: string) an url

        Returns:
        - 2 lists, alive and not_alive
        """
        # file = open(subdomain_file)
        # subdomains = file.read().splitlines()
        # print(subdomains)
        i = 0

        for subdomain in subdomainslist:
            i = i + 1
            if subdomain != True:
                valid = validators.url(subdomain)
                if valid == True:
                    try:
                        response = requests.get(subdomain)
                        if response.status_code == 200:
                            alive.append(subdomain)
                        else:
                            not_alive.append(subdomain)
                    except requests.exceptions.RequestException as error:
                        print("connection error", error)
                        not_alive.append(subdomain)
                        pass
                    finally:
                        print(i, '[$] Your target domain :- ', subdomain)
                else:
                    print("not valid url: ", subdomain)
                    break
            else:
                break
        print("Total subdomains: ", len(subdomainslist))
        print("----------")
        print("ALIVE SUBDOMAINS: ", alive)
        print("----------")
        print("NOT ALIVE SUBDOMAINS: ", not_alive)
        print("----------")

        print(len(alive), "is alive | ", len(not_alive),
              "is not alive | Difference is: ", len(subdomainslist)-len(alive))
        return alive, not_alive

    def check_if_contains_https(self, url):
        """ Checks if the url contains https://. if not adds it to the url """
        url_start = "https://"
        search_url = re.search(url, url_start)
        # noe feil her.
        if search_url == None:
            new_url = "https://" + url
            print(new_url)
            return new_url
        else:
            return self

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
            proc = Thread(target=self.multiproctask_3, args=(domain,))
            proc.daemon = True
            proc.start()

    def multiproctask_3(self, domain):
        """
        Finds potential subdomain with the help of multiprocessing
        """
        global q
        while True:
            subdomain = q.get()
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                subdomainslist.append(url)
                print("[+] Discovered subdomain:", url)
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
        # Multiprocess / threading for task 3
        crt_sh.multiproc(url_input, subdomains=open(
            "subdomains-1000.txt").read().splitlines())
        q.join()
        # Task 3 without multiprocessing / threading
        # crt_sh.task_3(url_input, subdomains=open(
        #    "subdomains-1000.txt").read().splitlines())
        crt_sh.task_4and5()
    else:
        # this output here does not include the threading version
        crt_sh = CrtSh(parser)
        print(crt_sh.task_1(args.domain))
        crt_sh.task_3(args.domain, subdomains=open(
            "subdomains-1000.txt").read().splitlines())
        crt_sh.task_4and5()
