import os,sys,cgi,random,urllib,simplejson
from copy import copy,deepcopy
here = os.path.dirname(sys.modules[__name__].__file__)
sys.path.insert(0, here)
sys.stderr = open(os.path.join(here,'log.log'),'a',0)
sys.stdout = sys.stderr

import util

def safehtml(x):
  return cgi.escape(str(x),quote=True)

type_builtin = type
def opt(name, type=None, default=None):
  o = util.Struct(name=name, type=type, default=default)
  if type is None:
    if default is not None:
      o.type = type_builtin(default)
    else: 
      o.type = str #raise Exception("need type for %s" % name)
  #if o.type==bool: o.type=int
  return o

def type_clean(val,type):
  if type==bool:
    if val in (False,0,'0','f','false','False','no','n'): return False
    if val in (True,1,'1','t','true','True','yes','y'): return True
    raise Exception("bad bool value %s" % repr(val))
  if type==str or type==unicode:
    # nope no strings, you're gonna get unicode instead!
    return util.unicodify(val)
  return type(val)

class Opts(util.Struct):
  " modelled on trollop.rubyforge.org and gist.github.com/5682 "
  def __init__(self, environ, *optlist):
    vars = cgi.parse_qs(environ['QUERY_STRING'])
    for opt in optlist:
      val = vars.get(opt.name)
      val = val[0] if val else None
      if val is None and opt.default is not None:
        val = copy(opt.default)
      elif val is None:
        raise Exception("option not given: %s" % opt.name)
      val = type_clean(val, opt.type)
      self[opt.name] = val
  def input(self, name, **kwargs):
    val = self[name]
    h = '''<input id=%s name=%s value="%s"''' % (name, name, safehtml(val))
    more = {}
    if type(val)==int:
      more['size'] = 2
    elif type(val)==float:
      more['size'] = 4
    more.update(kwargs)
    for k,v in more.iteritems():
      h += ''' %s="%s"''' % (k,v)
    h += ">"
    return h

LASTFILE = "/tmp/last_randomsearch"
def get_last_engine():
  if os.path.exists(LASTFILE):
    return open(LASTFILE).read().strip()
  else:
    return None

def save_last_engine(e):
  f = open(LASTFILE,'w')
  print>>f, e
  f.close()
  
URLS = {
  'google': "http://www.google.com/search?client=safari&rls=en-us&q=QUERY&ie=UTF-8&oe=UTF-8",
  'bing': "http://www.bing.com/search?q=QUERY",
}

def application(environ, start_response):
  status = '200 OK'
  
  opts = Opts(environ,
    opt('q', default=''))
  
  if not opts.q:
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    yield "<html>"
    yield "<head>"
    yield '''<link rel="search" type="application/opensearchdescription+xml" title="Random Search" href="randomsearch.osd.xml">'''
    yield "</head>"
    yield "<body>"
    yield "<form method=get>"
    yield opts.input('q',size=50)
    yield "<input type=submit>"
    yield "</form>"
    yield "<br>last engine was %s" % get_last_engine()
    yield "<br>engines are <pre>%s</pre>" % simplejson.dumps(URLS,indent=4)
    yield "</body>"
    yield "</html>"
    return

  last_e = get_last_engine()
  next_e = random.choice(list(set(URLS.keys()) - set([last_e])))
  save_last_engine(next_e)
  
  url = URLS[next_e].replace('QUERY', urllib.quote_plus(util.stringify(opts.q, 'utf8')))
  
  response_headers = [('Location', url)]
  start_response('302 Found', response_headers)
  return
  
  ##############
  
  yield url
  yield "<hr>"
    
    
  yield repr(opts)

  yield "<hr>"

  yield "<table>"
  for k in sorted(environ.keys()):
    yield "<tr><td>" + k
    yield "<td>" + str(environ[k])
    #yield "<br>"
  yield "</table>"
  yield "<hr>"
  yield output

