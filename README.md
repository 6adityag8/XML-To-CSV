# XML-To-CSV
A python script which extracts XML file from the zip archive of ESMA, converts it into CSV format and uploads the file to AWS S3 bucket. For more information, refer the below requirements. 

### Requirements:
1.Download the xml from [this link](https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100).
2.From the xml, please parse through to the first download link whose file_type is DLTINS and download the zip
3.Extract the xml from the zip.
4.Convert the contents of the xml into a CSV with the following header:
-FinInstrmGnlAttrbts.Id
-FinInstrmGnlAttrbts.FullNm
-FinInstrmGnlAttrbts.ClssfctnTp
-FinInstrmGnlAttrbts.CmmdtyDerivInd
-FinInstrmGnlAttrbts.NtnlCcy
-Issr
5.Store the csv from step 4) in an AWS S3 bucket

### SETUP Instructions:

1.Install [Git](https://www.atlassian.com/git/tutorials/install-git)
2.Clone the repository using `git clone https://github.com/6adityag8/XML-To-CSV.git`.
3.Move to the project directory and add your AWS credentials to the env variables in the [Dockerfile](https://github.com/6adityag8/XML-To-CSV/blob/master/Dockerfile).
```
cd XML-To-CSV/
vim Dockerfile
```
3.Install [Docker](https://docs.docker.com/get-docker/)
4.Build the Dockerfile using a tag name.
```
docker build -t xml_to_csv -f Dockerfile .
```
5.Run the created docker image using the same tag name, previously used.
```
docker run -it xml_to_csv
```
6.Go to your S3 bucket to get the CSV file.