# if [[ "$OSTYPE" == "linux-gnu"* ]]; then
#         # ...
#         :
# elif [[ "$OSTYPE" == "darwin"* ]]; then
#         # Mac OSX
#         python3 -m venv venv
#         source venv/bin/activate
# else
#         # Unknown.
#         :
# fi

pip install -r requirements.txt
uvicorn main:app --reload --port 9000