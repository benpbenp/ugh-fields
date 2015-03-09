from dropbox.client import DropboxClient, DropboxOAuth2Flow
import logging
logger = logging.getLogger('django.request')

domain_regex = r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})+'

def get_delta( user ):
    if user.profile.dropbox_access_token is None:
        raise Exception("User has no dropbox access token")

    client = DropboxClient(user.profile.dropbox_access_token)

    has_more = True

    while has_more == True:
        delta = client.delta(user.profile.dropbox_delta_cursor)

        logger.debug(delta)
        for entry in delta['entries']:
            process_delta_entry(entry, user)
        user.profile.dropbox_delta_cursor = delta['cursor']
        user.profile.save()
        has_more = delta['has_more']


def process_delta_entry(entry, user):
    path, metadata = entry
    logger.debug(path, metadata)
    segs = [seg for seg in path.split('/') if seg != '']

    import re
    from sites.models import Site

    if re.match(domain_regex, segs[0]):
        if len(segs) == 1:
            try:
                site = Site.objects.get(user = user, domain = segs[0])
            except Site.DoesNotExist:
                site = Site(user = user, domain = segs[0])

            if metadata == None and site.id:
                logger.debug('deleting site ' + segs[0])
                site.delete()
            elif metadata and metadata['is_dir'] == True and not site.id:
                logger.debug('creating site' + segs[0])
                site.save()
                
        elif len(segs) == 2:
            if metadata == None:
                if segs[1] == 'data':
                    #delete all data
                    pass
                elif segs[1] == 'templates':
                    #delete all templates
                    pass
                elif segs[1] == 'assets':
                    #delete all assets
                    pass
        elif len(segs) > 2:
            if segs[1] == 'data':
                pass
            elif segs[1] == 'templates':
                pass
            elif segs[1] == 'assets':
                pass


def generate_static_site( site ):
    client = DropboxClient(site.user.profile.dropbox_access_token)

