import requests
import time

def main():
    print('sleeping for 3 seconds')
    time.sleep(3)

    print("signalling to chromium")
    requests.get("http://chromium:9001/start")

    # print('sleeping for 2 seconds')
    # time.sleep(2)

    # print("signalling to recorder")
    # requests.get("http://recorder:9002/record")

if __name__=="__main__":
    main()