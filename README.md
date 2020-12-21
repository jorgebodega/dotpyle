# dotpyle

Dotpyle is a Python implementation of a dotfile system manager, allowing users
to keep a secure copy of all program configurations remotly, create different
profiles, etc.

## TBD

### Init

This will request a git url and a git token
If it is the first time you use Dotpyle, you will need to create an empty repo on GitHub, GitLab, etc.

If you want to manage an existing repo you just need to input url and token

    dotpyle init [--url <git url>]  [--protocol (git/https)] [--token (if repo is private)]

### Add

    dotpyle add [--path PATH] [OPTS]

1. Copy file to repo location
2. Delete file of path
3. Generate symbolik link to path


### Push
