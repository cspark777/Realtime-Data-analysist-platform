#!/bin/bash
echo DATA-admin-gui container built: $(cat /build-date.txt) 

if [ ! -z $DRUID_URL ]
then
   echo "Inserting ${DRUID_URL} Into Header"
   sed -i -e 's|DRUID_URL_PLACEHOLDER|http://'"${DRUID_URL}"'|' ./streamprocessors/templates/navigation_bar.html
fi


if [ ! -z $PIVOT_URL ]
then
   echo "Inserting ${PIVOT_URL} Into Header"
   sed -i -e 's|PIVOT_URL_PLACEHOLDER|http://'"${PIVOT_URL}"'|' ./streamprocessors/templates/navigation_bar.html
fi

if [ ! -z $ELK_URL ]
then
   echo "Inserting ${ELK_URL} Into Header"
   sed -i -e 's|ELK_URL_PLACEHOLDER|http://'"${ELK_URL}"'|' ./streamprocessors/templates/navigation_bar.html
fi

if [ ! -z $SUPERSET_URL ]
then
   echo "Inserting ${SUPERSET_URL} Into Header"
   sed -i -e 's|SUPERSET_URL_PLACEHOLDER|http://'"${SUPERSET_URL}"'|' ./streamprocessors/templates/navigation_bar.html
fi

if [ ! -z $KAFKA_URL_PUBLIC ]
then
   echo "Inserting ${KAFKA_URL_PUBLIC} Into Header"
   sed -i -e 's|KAFKA_URL_PLACEHOLDER|'"${KAFKA_URL_PUBLIC}"'|' ./streamprocessors/templates/navigation_bar.html
fi

if [ ! -z $JUPYTER_URL ]
then
   echo "Inserting ${JUPYTER_URL} Into Header"
   sed -i -e 's|JUPYTER_URL_PLACEHOLDER|'"${JUPYTER_URL}"'|' ./streamprocessors/templates/navigation_bar.html
fi

# Making files accessible
chmod ugo+rwx /DATA-admin-gui/files/

python manage.py migrate
python manage.py collectstatic --no-input
#python manage.py runserver 8000
uwsgi --master --ini uwsgi.ini



