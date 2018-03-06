import bs4 as bs
import urllib.request
import re
import csv
import time

sleep = True
#We'll store the results as we find them in the array below
my_results = []
#After we have all the results, we'll write to a csv file we can open in excel
datafile = open('gpu_output.csv','w',encoding='utf-8', newline='')
data_writer = csv.writer(datafile)

#These are graphics cards we want to match
regex = r"1080|1070|1060|480|570|580"
#Each page contains 120 results, starting with 0 will show 1-120. Will increment this to capture everything
page = 0
partslink = "https://chicago.craigslist.org/search/sop?s="
source = urllib.request.urlopen(partslink+str(page)).read()


soup = bs.BeautifulSoup(source, 'lxml')
#Finding a the classes in the html where the total page count is stored to know how times we need to loop to cover all pages
totCount = soup.select(".totalcount")[0].string
#There are 120 entries per page, need to load this many different pages
totLoops = round(int(totCount)/120)
hits = 0


for i in range(0,int(totCount)-1):

    
    allResults = soup.select(".result-row")
    #Start looping throught results on page
    for result in allResults:

        matches = re.search(regex,result.p.a.string, re.IGNORECASE)

        if matches:
            posttime = result.time['datetime']
            link = result.a['href']
            descrip = result.p.a.string
            #Listing potentially may not have this info, so have to wrap in Try-Catch to capture errors

            try:
                price = result.select(".result-meta")[0].select(".result-price")[0].string
            except:
                price = "NA"

            try:
                location = result.select(".result-meta")[0].select(".result-hood")[0].string
            except:
                location = "NA"
            my_results.append([posttime,descrip,price,location, link])
            hits+=1
            print("Match found. Total matches so far: "+str(hits))
            #print(posttime, link, descrip, price, location)
    #Sleeping 10 sec before reopening next page        
    if sleep:
        time.sleep(10)
        print("Sleeping 10s...\n This option can be turned off by setting sleep to False")
    page+=120
    source = urllib.request.urlopen(partslink+str(page)).read()
    soup = bs.BeautifulSoup(source, 'lxml')


print("Writing results to csv...")
data_writer.writerow(["Post_Time","Description","Price","Location","Link"])
data_writer.writerows(my_results)

print("Finished. gpu_out csv saved in current folder. Open in excel to view. Delete before rerunning.")
datafile.close()