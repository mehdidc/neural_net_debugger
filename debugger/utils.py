import httplib
import urllib


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

if __name__ == "__main__":
    send_state("my_layout", dict(a=1))
