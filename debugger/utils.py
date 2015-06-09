import httplib
import urllib
import base64
import json
import lzstring

def send_state(jobname, state, url='localhost:5000'):
    conn = httplib.HTTPConnection(url)
    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    state = state.copy()
    state["jobname"] = jobname
    data = state
    conn.request('POST', "/push_state", json.dumps(data), headers)
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

# for default template
def state_insert_curve(state, name, curve_name, point):
    x, y = point
    if name not in state["curves"]:
        state["curves"][name]= dict()
    state["curves"][name][curve_name] = dict(x=x, y=y)
    return state

def state_insert_html(state, name, html):
    state["html"][name] = html
    return state

def state_insert_table(state, name, content):
    state["table"][name] = content
    return state

def state_meta_insert_html(state, name):
    if "html" not in state["meta"]:
        state["meta"]["html"] = []
    state["meta"]["html"].append(name)
    return state

def state_meta_insert_curve(state, name, title, xlabel, ylabel, data_names):
    if "curves" not in state["meta"]:
        state["meta"]["curves"] = dict()
    state["meta"]["curves"][name] = dict(
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            data_names=data_names
    )
    return state
