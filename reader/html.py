"""
WIKIFILE (wf) FRONTEND INTERFACE
Generates and dumps an HTML file
(builtin css) with correct formating
and images to display a wikifile
with a wikipedia-like style

WARNING: DO NOT RUN IT ALONE
IT WILL NOT RESULT IN ANY 
OUTPUT. THIS IS JUST A LIBRARY
"""
import os
import base64

class BareRender:
    def render_header(text:str,style=""):
        return '<h1 style="{}">'.format(style)+text+'</h1>'
    def render_par(text:str,style=""):
        return '<p style="{}">'.format(style)+text.replace("\n","<br>\n")+'</p>'
    def build_image(alias,base):
        if not os.path.isdir("images"):
            print("Folder 'images' does not exist! Creating....")
            os.makedirs("images")
        
        with open(os.getcwd()+"/images/"+alias+".jpg",'wb') as f:
            print("Writing image {}.jpg to {}...".format(alias,os.getcwd()+"/images/"+alias+".jpg"))
            f.write(base64.b64decode(base))


class Render:
    def __init__(self) -> None:
        self.output = ""
    def render_title(self,title:str):
        #let's inject a style ;)
        self.output+=BareRender.render_header(title,"font-size:55;") + "\n"
    def render_writers(self, writers:list):
        v = "Written By:"
        for w in writers:
            v+=w+" "
        self.output += BareRender.render_par(v,"font-size:12;")
    def render_image(self,alias):
        self.output += '<img src="images/{}.jpg" alt="ALT:{}"/>'.format(alias,alias) + "\n"

    def render_textblock(self,title:str,content:str, image=""):
        v = BareRender.render_header(title,"font-size:18;") + "\n"
        v += BareRender.render_par(content)+"\n"
        
        if image != "" or " ":
            self.render_image(image)
        self.output+=v +"\n" 
    
    def out(self):
        self.output += """
<footer>
    <p style="font-size:10;">Compiled with Wikifile Reader by Imalaia3</p>
</footer>
        """
        return self.output