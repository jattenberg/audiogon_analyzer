cd /home/jattenberg/development/audiogon_analyzer/

/home/jattenberg/anaconda/bin/python /home/jattenberg/development/audiogon_analyzer/scripts/gather.py >> /home/jattenberg/development/audiogon_analyzer/data/output.log

git commit -a -m "updating"
git rpull && git push