#!/usr/bin/env python3
#****************************************************************************
#* upload.py
#*
#* Upload a binary release to a GitHub repository release area
#*
#* Copyright 2018 Matthew Ballance
#****************************************************************************
from github import Github
import os
import argparse
from os.path import basename

parser = argparse.ArgumentParser()
parser.add_argument("--org", help="Specify the organization")
parser.add_argument("--user", help="Specify the user")
parser.add_argument("--repo", help="Specify the repository")
parser.add_argument("--key", help="Specify the key")
parser.add_argument("--version", help="Specify the release version")
parser.add_argument("file", help="Specify the release version")
args = parser.parse_args()

script_dir = os.path.dirname(os.path.abspath(__file__))
changelog = os.path.dirname(script_dir) + "/ChangeLog.md"

# Before we get too involved with GitHub queries, ensure
# we have all the information we need
if os.path.exists(changelog) == False:
  print("Error: no ChangeLog.md exists")
  exit(1)

if os.path.exists(args.file) == False:
  print("Error: file to upload does not exist");
  exit(1)

if args.key == None:
  print("Error: --key not specified")
  exit(1)

if args.version == None:
  print("Error: --version not specified")
  exit(1)

if args.repo == None:
  print("Error: --repo not specified")
  exit(1)

# Now, create a release message from the ChangeLog
rls_message = ""
save_line = False
found_entry = False
with open(changelog) as fp:
  line = fp.readline()
  while line:
    if line.startswith("## " + args.version):
      save_line = True
      found_entry = True
    elif line.startswith("## "):
      save_line = False

    if save_line:
      rls_message = rls_message + line
    line = fp.readline()

fp.close()

if found_entry == False:
  print("Error: Failed to find an entry for version " + 
    args.version + " in ChangeLog.md")
  exit(1)

print("Message: " + rls_message)


g = Github(args.key)


if args.org != None:
  org = g.get_organization(args.org)
  repo = org.get_repo(args.repo)
elif args.user != None:
  user = g.get_user(args.user)
  repo = org.get_repo(args.repo)
else:
  print("Error: neither --org nor --user was specified")
  exit(1)

try:
  release = repo.get_release(id=args.version)
  print(release)
except:
  print("Note: Release " + args.version + " doesn't exist. Creating...")
  release = repo.create_git_release(
    tag=args.version, 
    name=args.version, 
    message=rls_message)

for a in release.get_assets():
  if a.name == basename(args.file):
    print("Note: file \"" + basename(args.file) + "\" already exists")
    print("  deleting...")
    a.delete_asset()

print("Note: uploading file " + args.file)
release.upload_asset(
  path=args.file,
  content_type='application/octet-stream')
print("Done!")

