#!user/bin/env python3

import requests
import argparse
import re
import validators

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

subdomain_file = "subdomains.txt"
subdomainslist = []
alive = []
not_alive = []


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

    def task_3(self, domain):
        """
        Finds potential subdomains

        Params:
        - domain: (type: string) a domain

        Returns:
        - a list of subdomains
        """
        print("domain: ", domain)
        file = open('subdomains-100.txt')
        content = file.read()
        subdomains = content.splitlines()
        i = 0
        for subdomain in subdomains:
            i = i + 1
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                subdomainslist.append(url)
                print(i, "[+] Discovered a subdomain: ", url)
        print(subdomainslist)
        return subdomainslist

    def task_4and5(self):
        """ 
        Open subdomains file
        store the subdomains in a list
        Search through the list to see if they respond
        store the results in 2 seperate lists

        Params:
        - url: (type: string) an url

        Returns:
        - 2 lists, alive and not_alive 
        """
        #file = open(subdomain_file)
        #subdomains = file.read().splitlines()
        # print(subdomains)
        i = 0

        for subdomain in subdomainslist:
            i = i + 1
            if subdomain != True:
                #subdomain_url = f'https://{subdomain}'
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
              "is not alive | Difference is: ", len(subdomainslist)-len(not_alive))
        return alive, not_alive

    def task_6(self):
        """ Prints out the list and calculates the difference in alive and dead subdomains """
        pass

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
        crt_sh.task_1(url_input)
        crt_sh.task_3(url_input)
        crt_sh.task_4and5()
    else:
        crt_sh = CrtSh(parser)
        print(crt_sh.task_1(args.domain))
