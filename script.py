# read URL of the website
import requests
import json
import csv
import os


def run():
    print_welcome()
    website_url = read_user_input()
    csv_file_name = prepare_csv_file(website_url)
    for strategy in strategies:
        strategy_specific_url = build_full_url(website_url, strategy)
        performance_report = query_performance(strategy_specific_url)
        create_report(performance_report, csv_file_name)
    print("Collecting data is finished - check core web vitals in .csv file")


def print_welcome():
    print('Check performance results by providing website URL')


def read_user_input():
    return input('enter website URL (www.dental21.de): ')


def prepare_csv_file(website_url):
    file_name = 'performance_report_' + website_url + '.csv'
    with open(file_name, "a") as file:
        if file_is_empty(file_name):
            headers = ['lighthouse fetchTime', 'form factor', 'overall score', 'speed_index', 'first_contentful_pain',
                       'first_meaningful_paint', 'time_to_interactive']
            csv.writer(file).writerow(headers)
    return file_name


def file_is_empty(path):
    return os.stat(path).st_size == 0


def build_full_url(website_url, strategy):
    full_url = pagespeed_base_url + website_url + "&strategy=" + strategy
    print("url is: " + full_url)
    return full_url


def query_performance(strategy_specific_url):
    web_response_desktop = requests.get(strategy_specific_url)
    response = json.loads(web_response_desktop.content)
    return response


def create_report(report, file_name):
    with open(file_name, "a") as file:
        rows = [report['lighthouseResult']['fetchTime'],
                report['lighthouseResult']['configSettings']['formFactor'],
                report["lighthouseResult"]["categories"]["performance"]["score"] * 100,
                report["lighthouseResult"]["audits"]["speed-index"]["score"] * 100,
                report["lighthouseResult"]["audits"]["first-contentful-paint"]["score"] * 100,
                report["lighthouseResult"]["audits"]["first-meaningful-paint"]["score"] * 100,
                report["lighthouseResult"]["audits"]["interactive"]["score"] * 100]

        csv.writer(file).writerow(rows)


if __name__ == '__main__':
    pagespeed_base_url = 'https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=http://'
    strategies = ["mobile", "desktop"]
    run()
