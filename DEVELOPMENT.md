## Initial Configuration

The server must accept your RSA key. Make sure you can connect passwordless first.

Add to your `~/.ssh/config`:
 Host your_host_alias
  Hostname your_hostname
  User your_user
  IdentityFile ~/.ssh/id_rsa.pub


## Deployment

First, bump the version number in `ephemer/__init__.py`.

Then:

 fab deploy --hosts=ephemer --site=production
 
Once you're done, commit:
 git commit ephemer/__init__.py
 
Then, tag:
 git tag v0.1.0
 
And push:
 git push
 git push --tags

