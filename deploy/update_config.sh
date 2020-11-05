mkdir ~/bin
mv /home/etiennody/purbeurre/deploy/gunicorn/gunicorn_start ~/bin/gunicorn_start
chmod u+x bin/gunicorn_start
mkdir ~/run && mkdir ~/logs
touch ~/logs/gunicorn-errors.log
mv /home/etiennody/purbeurre/deploy/supervisor/purbeurre-gunicorn.conf /etc/supervisor/conf.d/purbeurre-gunicorn.conf
mv /home/etiennody/purbeurre/deploy/nginx/purbeurre /etc/nginx/sites-available/purbeurre
mv /home/etiennody/purbeurre/deploy/cron/update_purbeurre_db.sh ~/update_purbeurre_db.sh

supervisorctl nginx restart
