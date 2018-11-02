###########################################################################################
#
# SteelConnect.py
#
# This Python module provides functions for calling the SteelConnect SDWAN 
# REST API.  The functions in this module include requesting site data, creating sites
# and deleting sites.
#
# Use 'site_list.json' as sample file for inputing sites.
#
# Nolan Chen
###########################################################################################

import requests
import json

##############################################################################################
#
# def get_requests(url,user,password)
#
# Makes REST API Get request
################################################################################################
def get_request(url,user,password):
    r = requests.get(url, auth=(user,password))
    return r
 

#########################################################################
#
# def read_sites()
#
# This function reads a JSON file containing SteelConnect sites
# and returns a list of dictionaries called 'site_list.' Each dictionary 
# contains info for one Site.  
##########################################################################
def read_sites_file():
    try:
        filename = input("\nEnter JSON filename for sites: ")
        print("open JSON filename: "+filename)
        f = open(filename)
        site_dict = json.load(f)
        return site_dict['Items']

    except FileNotFoundError:
        print("File '"+filename+"'not found.")
        return []
    
##########################################################################
#
# def get_org_sites(user,password,url)
#
# This function returns a list of sites from a SteelConnect org in 
# a dictionary.
#############################################################################
def get_org_sites(user,password, url):
    r= get_request(url=url, user=user, password=password)
    
    if ( r.status_code == 200):
        site_dict = r.json()
        #print("Sites:\n"+str(site_dict))
        write_json_file("output.json", site_dict)
    else:
        print ("Error retrieving sites. Code "+str(r.status_code))
        site_dict = None

    site_list = site_dict['items']

    return site_list

###############################################################################
#
# def create_sites
#
# Takes a list of sites and creates the sites in SteelConnect org.
##################################################################################
def create_sites(user,password, sites_url, site_dict):
    for site in site_dict:
        print("Creating site "+site['name']+"...")
        r = create_site(user,password,sites_url,site)
        if r.status_code == 200:
            print("Site successfully created.")
        else:
            print("Site creation failed.  Status code: "+str(r.status_code))

def create_site(user, password,url, site_data):
    r = requests.post(url, auth=(user, password), json=site_data)
    return r


###############################################################################
#
# def delete_site(user,password, site_url, site_id)
#
# Deletes a site
##################################################################################
def delete_site(user,password, site_url, site_id):
    url = site_url + site_id
    print("Deleting site_id: '"+site_id+"'")
    r = requests.delete(url, auth=(user,password))
    if (r.status_code == 200):
        print("Site successfully deleted.")
    else:
        print("Site deletion failed.")
    return r

###############################################################################################
#
# def get_site_id(longname)
#
# This function returns the site_id for a Site using the longname of the Site as input.
###############################################################################################
def get_site_id(user,password,sites_url,longname):
    site_id = ""
    site_list = get_org_sites(user,password, sites_url)
    for site in site_list:
        if site['longname'] == longname:
            site_id = site['id']

    return site_id

def get_org_dictionary(response):
    org_item = response.json()  #HTTP Response Object contains a dictionary of Items key and List of one dictionary
    #print("org_item: \n"+ str(org_item))
    org_value_list = org_item['items']
    org_dictionary = org_value_list[0]
    #print("\n org_value:\n"+str(org_value))

    return org_dictionary
    
def print_dictionary_contents(dictionary):
    for key, value in dictionary.items():
        print("\nkey: " + key)
        print("Value: " + str(value))

def write_json_file(filename, dict):
    f = open(filename, 'w')
    json.dump(dict,f, indent=2)
    f.close()

####################################################################################
#
# def sites_demo()
#
# Sites Demo program
#
# sites_demo calls functions for listing, creating and deleting sites
#####################################################################################
def sites_demo(user, password, orgid, base_uri):

 
   
    sites_url = base_uri + "org/"+orgid + "/sites" 
 
    print("Hello SteelConnect Sites!")

    #Print Sites
    site_list = get_org_sites(user,password, sites_url)
    print("\nSites in '"+orgid+"':")
    for site in site_list:
        #print_dictionary_contents(site)
        print(site['longname'])


    #Create Sites
    #site_dict = read_sites_file()
    #create_sites(user,password,sites_url, site_dict)


    #Delete Site
    """
    site_id = ""
    delete_url = base_uri + "site/"
    site_longname = input("\nEnter Site name to delete:")
    site_id = get_site_id(user,password, sites_url,site_longname)
    if site_id != "":
        delete_site(user,password,delete_url, site_id)
    else:
        print("Site ID for '"+site_longname+"' not found.")

    """
##############################################################################
#
# def get_api(user,password,url)
#
# Returns a list of dictionaries.  Each dictionary contains application info
#
##############################################################################
def get_api(user, password,url):
    r = get_request(url, user,password)


    if ( r.status_code == 200):
        json_result = r.json()
        #print("Results:\n"+str(json_result))
        write_json_file("output.json", json_result)
        result = json_result["items"]
    else:
        print ("API GET Request Error Code: "+str(r.status_code))
        result = {}
        
    

    return result


###################################################
#
# def print_item_names
#
# items = list of dictionaries
#
######################################################
def print_item_names(items):
    i=0
    name_list = []
    for apps in items:

        app_name = apps['name']
        name_list.append(app_name)
        #print(str(i)+": "+ app_name)
    name_list.sort()
    f = open('name_list.txt', 'w')
    for name in name_list:
        i=i+1
        app = str(i) +": "+name
        print(app)
        f.write(app+'\n')

    f.close()

#########################################################
# 
# def print_items(items)
# 
# Outputs a list of items to a JSON file.
# 
#########################################################    

def print_items(items):
    filename = 'items.json'

    write_json_file(filename, items)

    print ("items outputed to file: '"+filename+"'")

    """
    f = open('items.txt','w')

    for item in items:
        output = "\n" + str(item)
        print(output)
        f.write(output)
    """
        



##################################################
#
# Main Program
#
##################################################


#######################################################
# SCM Credentials
#########################################################

user = 'Nolan.Chen@riverbed.com'
password = 'SteelConnectRocksXXXX!'
orgid = "org-Orgrvbd039-6b209b6973717378"
base_uri = "https://riverbed-se01.riverbed.cc/api/scm.config/1.0/"

print ("Hello SteelConnect!")

######################################################################
# Demonstrate listing, adding and deleting SteelConnect Sites
######################################################################

#sites_demo(user, password, orgid, base_uri)



#####################################################################
# Use REST API to GET from SCM
#####################################################################

#get_param = "apps"

#List all BGP Neighbors
get_param = "org/" + orgid + "/bgpneighs"

#Get BGP Neighbor Info
#bgpneighid = "bgpneigh-aristabgp-377f1dfe2c7fdd34"
#get_param = "bgpneighs/"+bgpneighid



url = base_uri + get_param    

items = get_api(user,password, url)   
print_items(items)
#print_item_names(items)


print ("Program complete.")