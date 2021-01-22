import csv
import io
import logging
import os
import zipfile

import boto3
import requests
from botocore.exceptions import NoCredentialsError
from lxml import html, etree

ESMA_URL = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/' \
           'select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T' \
           '23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")

AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

logging.basicConfig(filename='logfile.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def extract_download_link():
    """
    Parses the XML from ESMA url and extracts the first download link whose file_type is DLTINS
    :return: extracted download_link
    """
    try:
        response = requests.get(ESMA_URL, verify=False)
        parser = html.fromstring(response.content)
        download_link = (parser.xpath(
            '(//doc[str[@name="file_type" and text()="DLTINS"]])[1]//str[@name="download_link"]/text()'
        ) or ('',))[0]

        if not download_link:
            logger.error("Couldn't find the download link.")

        return download_link
    except Exception as e:
        logger.exception(e)


def extract_zipped_content_from_download_link(download_link):
    """
    Downloads the zip file from the download link and unzips the XML content
    :param download_link: download link extracted from ESMA url
    :return: file path for the unzipped XML file
    """

    download_response = requests.get(download_link, verify=False)
    unzipped_response = zipfile.ZipFile(io.BytesIO(download_response.content))
    zip_file_name = (unzipped_response.namelist() or ('unzipped_file.xml',))[0]

    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    unzipped_response.extractall(path=MEDIA_ROOT)

    return os.path.join(MEDIA_ROOT, zip_file_name)


def convert_xml_to_csv(xml_file):
    """
    Converts the zip extracted XML file to CSV
    :param xml_file: the zip extracted XML file
    :return: file path of the converted CSV file
    """

    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        csv_file_name = 'converted_csv.csv'
        csv_path = os.path.join(MEDIA_ROOT, csv_file_name)
        csv_file = open(csv_path, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        total_number_of_records = len(root.xpath('//Document//RefData'))
        for counter in range(1, total_number_of_records + 1):
            id = (root.xpath(
                '(//Document//RefData/FinInstrmGnlAttrbts/Id/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            full_name = (root.xpath(
                '(//Document//RefData/FinInstrmGnlAttrbts/FullNm/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            classification = (root.xpath(
                '(//Document//RefData/FinInstrmGnlAttrbts/ClssfctnTp/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            commodity = (root.xpath(
                '(//Document//RefData/FinInstrmGnlAttrbts/CmmdtyDerivInd/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            ntnl = (root.xpath(
                '(//Document//RefData/FinInstrmGnlAttrbts/NtnlCcy/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            issuer = (root.xpath(
                '(//Document//RefData/Issr/text())[{0}]'.format(str(counter))
            ) or ('',))[0]
            csv_writer.writerow([id, full_name, classification, commodity, ntnl, issuer])
        csv_file.close()

        return csv_path
    except FileNotFoundError:
        logger.exception("The file was not found.")
    except Exception as e:
        logger.exception(e)


def upload_file_to_aws(file_path):
    """
    Uploads the given file to AWS S3
    :param file_path: path of the file which needs to be uploaded
    """
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    try:
        s3_file_name = 'csv_upload.csv'
        s3.upload_file(file_path, S3_BUCKET_NAME, s3_file_name)
    except FileNotFoundError:
        logger.exception("The file was not found.")
    except NoCredentialsError:
        logger.exception("AWS Credentials were not available.")
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    # Get the download link and extract the zip content from the downloaded file
    file_content = extract_zipped_content_from_download_link(extract_download_link())

    # Converts the XML file to CSV
    csv_file = convert_xml_to_csv(file_content)

    # Uploads the file to AWS S3
    upload_file_to_aws(csv_file)
