import httplib
import urllib
import base64

def send_state(jobname, state, url='localhost:5000'):
    conn = httplib.HTTPConnection(url)
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    state = state.copy()
    state["jobname"] = jobname
    data = state
    conn.request('POST', "/push_state", urllib.urlencode(data), headers)
    conn.getresponse()
    conn.close()

def img_to_html(fd):
    img = "data: image/png;base64,{0}".format(urllib.quote(base64.b64encode(fd.read())))
    return "<img src=\"{0}\" />".format(img)

from StringIO import StringIO

def fig_to_html(fig):
    imgdata = StringIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    return img_to_html(imgdata)

if __name__ == "__main__":
    send_state("my_layout", dict(a=1))
