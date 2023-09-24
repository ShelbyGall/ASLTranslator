**git -h/--help**
will give you git optionsza

**git clone <url>**
to clone a project onto your computer

**git init**
to initate git on a fresh project

**git add .**
add all file in the dir to git

**git commit -"example"**
step before pushing a to github, where you explain what the modification does

**git commit --amend**
**git commit --amend --no-edit**
commits to the same commit name as earlier

**git push**
pushing your code to github/git

**git push --force**
to force to push

**git log**
to get log

**git log --oneline**
to get log in one line

**git reset <ID>**
using the ID given from "git log --oneline" you can restore to a prev ver

**.gitignore**
this is the file you mention the file you dont want to get gitted is

**git mv index.html home.html**
renames index.html to home.html, bcz if you just rename it git sees it as you deleting index.html and creating a
file called home.html, which will confuse people in the future

**git status**
to see if you have anything to push

**git rm index.html**
removes index.html from git and file system

**git diff || git diff <ID>**
show the difference between prev ver

**git rebase -i --root**
rebasing is when you add something that would have been needed to be added earlier like going and changing something
in the past like you have a time mechine, eg. author bot to author bob

**git branch**
show the branches avablable

**git switch <NAME>**
switch branches

**git switch -c <NAME> (older ver: git checkout -b <NAME>)**
copy a branch

**git merge <BRANCH>**
merges a branch to another branch

- to merge first switch to the branch you want it to merge to and then use "git merge <branch>" to merge it

**git branch --delete/-d NAME**
deleting a branch

**git clean -f**
clean tracked files

**Git Flow**

- Feature/fix branch
- Make changes
- Merge to master
- Delete old branch

**git stash list**

**git stash pop**

**git clean -n -d -f**

