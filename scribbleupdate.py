from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import os.path, time
from os import listdir
from os.path import isfile, join

##Open blog client
blog = Client('http://swarna.tonse.in/xmlrpc.php', 'admin', 'xxxx')

def deleteDraft(postname):
    offset = 0
    increment = 20
    while True:
        posts = blog.call(GetPosts({'number': increment, 'offset': offset}))
        if len(posts) == 0:
                break  # no more posts returned
        for post in posts:
                if(post.title == postname):
                    blog.call(DeletePost(post.id))
        offset = offset + increment

##Retrieve date from file
t_file = open('S:/Academic/DraftPost/timefile', 'r')
t = t_file.readline()
last_update_time = datetime.strptime(t,"%d/%m/%Y %H:%M:%S")

##Get files in directory
local_path = 'S:/Scribbles'
files = listdir(local_path)
print(files)

for f in files:
    if isfile(join(local_path, f)):
        #print(getmtime(join(local_path, f))
        if(datetime.fromtimestamp(os.path.getmtime(join(local_path, f))) > last_update_time):
            post = WordPressPost()
            new_post = open(join(local_path, f), 'r')
            post.title = f
            post.content = new_post.read()
            deleteDraft(f)
            blog.call(NewPost(post))

##Update time in file
t = datetime.now()
t_file.write(t.strftime("%d/%m/%Y %H:%M:%S"))
t_file.close()


