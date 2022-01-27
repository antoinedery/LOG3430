source ./init.sh

coverage run -m --source=. --branch unittest
coverage report -m