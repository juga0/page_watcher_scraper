Work in progress...

installation
--------------------

### system dependencies

    sudo apt-get install python-dev


### with virtualenv

#### obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or follow these instructions:

##### if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv

##### if Debian older  than jessie (or virtualenv version prior to 1.9)

    sudo apt-get install ca-certificates gnupg
    curl https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz#md5=70f63a429b7dd7c3e10f6af09ed32554 > /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz # or latest
    curl https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz.asc > /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz.asc # or latest
    mkdir /tmp/.gnupg
    chmod 700 /tmp/.gnupg
    gpg --homedir /tmp/.gnupg --keyserver hkps.pool.sks-keyservers.net --recv-keys 3372DCFA
    gpg --homedir /tmp/.gnupg --fingerprint 3372DCFA # check is 7C6B 7C5D 5E2B 6356 A926  F04F 6E3C BCE9 3372 DCFA
    gpg --homedir /tmp/.gnupg --verify /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz.asc
    tar xzf /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz --directory /pathtovirtualenvbin/
    echo "alias virtualenv='python  /pathtovirtualenvbin/virtualenv-13.1.0/virtualenv.py'" >> ~/.bashrc # or other shell start
    source ~/.bashrc # or other shell start

#### create a virtualenv

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/oiienv
    source ~/.virtualenvs/oiienv/bin/activate

#### install dependencies in virtualenv
    git clone https://github.com/juga0/page_watcher_scraper
    cd page_watcher_scraper
    pip install -r requirements.txt


configuration
----------------------

More about page_watcher_scraper/page_watcher_scraper/settings.py: TBD
More about page_watcher_scraper/config_local.py: TBD
If you need local settings, edit page_watcher_scraper/page_watcher_scraper/settings_local.py and page_watcher_scraper/config_local.py

running
--------------

To list the scrappers:

    scrapy list

To run page_watcher_scraper:

    cd page_watcher_scraper
    ./scraper.py

configuring cron job
---------------------

Create an script like this replacing the path by your path:

    cd page_watcher_scraper
    vim run.sh

    #!/bin/bash
    cd /mypath/page_watcher_scraper && source /mypath/page_watcher_scraper/environment && source /mypath/.virtualenvs/oiienv/bin/activate && /mypath/.virtualenvs/oiienv/bin/python /mypath/page_watcher_scraper/scraper.py >> /mypath/page_watcher_scraper/cronlog.txt

Edit crontab:

    crontab -e

To run every day at 14:35h:

    35 14    * * * /bin/bash /home/duy/page_watcher_scraper/run.sh