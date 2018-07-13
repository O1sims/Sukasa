#!/bin/sh -e
# Build the components of the Sukasa application

case $1 in
    help)
        cat <<EOF

EOF
        ;;
    up)
        cd src
        docker-compose up
        ;;
    down|stop)
        cd src
        docker-compose $1
        ;;
    test)
        cd src/backend
        python manage.py test
        ;;
    all)
        docker build -t sukasa:latest src/backend/.
        docker build -t sukasa-gui:latest src/gui/.
        ;;
esac
