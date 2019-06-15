from bs4 import BeautifulSoup
import requests
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import youtube_dl



class yt_downloader():

    def __init__(self):
        # yt channel url from command line 
        try:
            url = sys.argv[1]
            print(url)
            self.url = url + '/playlists'            
            soup = self.grabber(url + '/about') 
            author_name = soup.find(id='channel-title').text
            # current directory
            self.path = os.getcwd() + '\\'+  author_name
            
        except:
            print('\nplease provide a youtube channel\n')
            sys.exit()
            
        self.playlist()
       
        self.playlist_details()
        
        
    # grabs source code of the page
    def grabber(self,url=None):

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
            options.add_argument('--headless')
            
            # chromedriver should be present in the working directory
            try:
                
                driver = webdriver.Chrome(os.getcwd() + '\chromedriver.exe' , chrome_options=options)
                
               
                driver.get(url)
                # download page source code
                page = driver.execute_script('return document.body.innerHTML')
                # converting to beautiful soup obj for manipulation
                soup = BeautifulSoup(''.join(page), 'html.parser')
                
            except:
                print('\nchromedriver not found\n')
                sys.exit()

        
            
    
        else:
        
            print('\nplease provide a youtube channel\n')
        
        return soup

    # gets all playlists and their corresponding video urls
    def playlist(self):
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
        
        # each youtube links in a playlist
        for each_playlist in self.playlists:
            
            each_playlist = 'https://www.youtube.com' + each_playlist
            # grabs the source code of each playlist
            soup = self.grabber(url=each_playlist)
            # extracts playlist name from source code
            playlist_name = [content.contents[0].strip() for content in soup.find_all('a',class_='yt-simple-endpoint style-scope yt-formatted-string')][0]  
            
            
            # check if folder with playlist name exist
            if not os.path.exists(self.path + '\\' + playlist_name):
                # create new folder with playlist name           
                os.makedirs(self.path + '\\' + playlist_name)
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
       
        #options for youtube-dl
        ydl_opts = {'outtmpl': self.path + '\\' + playlist_name + '\%(title)s.%(ext)s'}
        # formatting youtube.com/watch?v=something      
        url = 'https://www.youtube.com' + url
        
        try:
        
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except:
            print('\n'+ playlist_name + '\nvideo unavailable skipping\n')
        
       
      
            

if __name__ == "__main__":
    yt_downloader()
    
