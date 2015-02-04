from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse

from dropbox.client import DropboxClient, DropboxOAuth2Flow

from django.contrib.auth.decorators import login_required

from django.conf import settings
# Create your views here.

@login_required(login_url = '/account/login/')
def home(request):
    access_token = request.user.profile.dropbox_access_token
    real_name = None
    #app.logger.info('access token = %r', access_token)
    if access_token is not None:
        client = DropboxClient(access_token)
        account_info = client.account_info()
        real_name = account_info["display_name"]
    return render(request, 'account/home.html', {'real_name':real_name, 'user': request.user})

@login_required(login_url = '/account/login/')
def dropbox_logout():
    username = session.get('user')
    if username is None:
        abort(403)
    db = get_db()
    db.execute('UPDATE users SET access_token = NULL WHERE username = ?', [username])
    db.commit()
    return redirect(url_for('home'))

def get_auth_flow(request):
    redirect_uri = request.build_absolute_uri(reverse('dropbox_auth_finish'))
    
    dropboxoauth = DropboxOAuth2Flow(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, redirect_uri,
                                       request.session, 'dropbox-auth-csrf-token')
    return dropboxoauth


def login(request):
    from django.contrib.auth import authenticate, login
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return redirect(reverse('account_home'))
            else:
                pass
                # Return a 'disabled account' error message
        else:
            pass
            # Return an 'invalid login' error message.
    return render(request, 'account/login.html')

@login_required(login_url = '/account/login/')
def logout(request):
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('home'))


def main():
    init_db()
    app.run()


if __name__ == '__main__':
    main()

@login_required(login_url = '/account/login/')
def dropbox_auth_start(request):
    redirect_uri = get_auth_flow(request).start()
    request.session['dropbox-auth-csrf-token'] = request.session['dropbox-auth-csrf-token'].decode('ascii')
    return redirect(redirect_uri)

@login_required(login_url = '/account/login/')
def dropbox_auth_finish(request):
    get_copy = _massage_csrf(request)
    try:
        access_token, user_id, url_state = get_auth_flow(request).finish(get_copy)
    except DropboxOAuth2Flow.BadRequestException as e:
        abort(400)
    except DropboxOAuth2Flow.BadStateException as e:
        abort(400)
    except DropboxOAuth2Flow.CsrfException as e:
        abort(403)
    except DropboxOAuth2Flow.NotApprovedException as e:
        flash('Not approved?  Why not')
        return redirect(url_for('home'))
    except DropboxOAuth2Flow.ProviderException as e:
        app.logger.exception("Auth error" + e)
        abort(403)

    request.user.profile.dropbox_access_token = access_token
    request.user.profile.save()
    return redirect(reverse('account_home'))


def _massage_csrf(request):
    get_copy = dict(request.GET)
    state = request.GET['state']
    split_pos = state.find('|')
    if split_pos < 0:
        given_csrf_token = state
        url_state = None
    else:
        given_csrf_token = state[0:split_pos]
        url_state = state[split_pos+1:]

    state = eval(given_csrf_token).decode('ascii')
    if url_state:
        state += "|" + url_state
    
    get_copy['state'] = state
    get_copy['code'] = get_copy['code'][0]

    return get_copy 
