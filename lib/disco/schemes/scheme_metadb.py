def input_stream(fd, size, url, params):
    import os
    from disco import util
    from disco.comm import download
    from discodb import MetaDB, Q
    scheme, netloc, rest = util.urlsplit(url)
    path, rest = rest.split('!', 1) if '!' in rest else (rest, '')

    if netloc[0] == Task.netloc[0]:
        discodb = MetaDB.load(os.path.join(Task.root, path))
    else:
        discodb = MetaDB.loads(download('disco://%s/%s' % (netloc, path)))

    if rest:
        method_name, arg = rest.split('/', 1) if '/' in rest else (rest, None)
        method = getattr(discodb, method_name)
        if method_name == 'query':
            return method(Q.urlscan(arg)), size, url
        return method(*filter(None, arg)), size, url
    return discodb, size, url
