from pytube import YouTube
url = 'https://www.youtube.com/watch?v=LBp0dThh2Tg'
yt = YouTube(url)       
yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
yt.download(os.getcwd())