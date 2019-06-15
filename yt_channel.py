from bs4 import BeautifulSoup
import requests
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import youtube_dl



class yt_downloader():

    def __init__(self):
        '''
        1. extract channel link from command line
        2. finds name of the channel
        3. create channel name folder to store playlist name folder
        '''
        
        # check if url is provided on command line
        try:
            
            # yt channel url from command line
            url = sys.argv[1]
            
        except:
            
            # exit if not channel is not provided
            print('\nplease provide a youtube channel\n')
            sys.exit()
        
        # to redirect yt channel to playlist
        self.url = url + '/playlists'
        
        # check if driver is loaded and ready to grab html source code
        try:
        
            # redirect to about page
            soup = self.grabber(url + '/about')
            # finds name of the channel
            author_name = soup.find(id='channel-title').text
            # inside channel name directory
            self.path = os.path.join(os.getcwd(),author_name)
            
        except:
            
                sys.exit()

        self.playlist()
        self.playlist_details()
        
        
    
    def grabber(self,url=None):
        '''
        1. check if url is provided
        2. download html source code
        '''
        
        # if no url is provided, uses the default one from the command line
        if not url:
            
            # default url from the command line
            url = self.url
        
        # checking if correct url is provided
        if url:
            
            # code from selenium for downloading dynamic page's source code
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            # these prevents the browser from launching
            options.add_argument('--headless')
            
            # chromedriver should be present in the working directory
            try:
                if os.name == 'nt':
                
                    # initializing webdriver for chrome
                    
                    driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe' , chrome_options=options)
                
                        
                else:
                
                    driver = webdriver.Chrome(os.getcwd() + '/chromedriver' , chrome_options=options)
                

                # to get the particular website
                driver.get(url)
                # download page source code
                page = driver.execute_script('return document.body.innerHTML')
                # converting to beautiful soup obj for manipulation
                soup = BeautifulSoup(''.join(page), 'html.parser')
            
                
            except:
                
                # missing chromedriver.exe for windows and chromedriver.sh for mac
                print('\nchromedriver not found\n')
                # exit from the program
                sys.exit()
            
                

        
            
    
        else:
            
            print('\nplease provide a youtube channel\n')

        
                    
        return soup


    
                    

    
    def playlist(self):
        '''
        1. checks if provided url is www.youtube.com
        2. extracts all the playlists
        '''
        
        # takes default command line url
        url = self.url
        
        if url:
            
            # checking if url is from youtube
            if 'www.youtube.com' not in url:
                print('\nplease provide a youtube channel\n')
                sys.exit()
            
            # grabs the source code of that current url
            soup = self.grabber(url)
            # extracting playlist urls from the source code
            x = soup.find_all('a',class_="yt-simple-endpoint style-scope yt-formatted-string")
        # check for playlist
        if not x:
            
            # if the channel does not contain any playlist
            print("no playlists") 
            sys.exit()
        
        else:
            
            # store the playlist in a list called self.playlists
            self.playlists = []
            
            # loops around each parts of the source code
            for value in x:               
                # playlist urls present in href class
                urls = value.get('href')
                # storing playlist urls in the list
                self.playlists.append(urls)



            

    def playlist_details(self):
        '''
        1. find video urls for each playlist
        2. create playlist name folder
        3. filter video urls
        '''
        
        # each youtube links in a playlist
        for each_playlist in self.playlists:
            
            each_playlist = 'https://www.youtube.com' + each_playlist
            # grabs the source code of each playlist
            soup = self.grabber(url=each_playlist)
            # extracts playlist name from source code
            playlist_name = [content.contents[0].strip() for content in soup.find_all('a',class_='yt-simple-endpoint style-scope yt-formatted-string')][0]
            # check if folder with playlist name exist
            self.loc = os.path.join(self.path,playlist_name)
            if not os.path.exists(self.loc):
                # create new folder with playlist name           
                os.makedirs(self.loc)
            
            # playlist containing urls
            playlist_video_urls = [value.get('href') for value in soup.find_all('a',class_='yt-simple-endpoint style-scope ytd-playlist-video-renderer')]
            '''
            filtering playlist url by removing &list=

            unfiltered: /watch?v=ZF8d6kMDoLk&list=PLTKUP0v0mxht7MMR4cwj1qyw78-x1Kouj&index=2&t=0s
            filtered: /watch?v=ZF8d6kMDoLk
            '''
            playlist_video_urls_filtered =  [a.split('&list')[0] for a in playlist_video_urls]
            
            # going through each yt video urls of a single playlist
            for video_url in playlist_video_urls_filtered:
                # calling download_video function with each url as parameter
                self.download_video(video_url,playlist_name)



    def download_video(self,url,playlist_name):
        '''
        1. download video using youtube-dl library
        2. stores downloaded videos in corresponding playlist name folder
        3. skips video that are private
        '''
       
        #options for youtube-dl
        ydl_opts = {'outtmpl': os.path.join(self.loc,'\%(title)s.%(ext)s')}
        # formatting youtube.com/watch?v=something      
        url = 'https://www.youtube.com' + url
        
        try:
        
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    
        except KeyboardInterrupt:
            
            sys.exit()
        
        except:
            
            print('\n'+ playlist_name + '\nvideo unavailable skipping\n')
        
       
      
            

if __name__ == "__main__":
    yt_downloader()
    
