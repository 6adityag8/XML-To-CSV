<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="XMLToCSV_0"></a>XML-To-CSV</h1>
<p class="has-line-data" data-line-start="1" data-line-end="2">A python script which extracts XML file from the zip archive of ESMA, converts it into CSV format and uploads the file to AWS S3 bucket. For more information, refer the below requirements.</p>
<h3 class="code-line" data-line-start=3 data-line-end=4 ><a id="Requirements_3"></a>Requirements:</h3>
<p class="has-line-data" data-line-start="4" data-line-end="15">1.Download the xml from <a href="https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&amp;fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&amp;wt=xml&amp;indent=true&amp;start=0&amp;rows=100">this link</a>.<br>
2.From the xml, please parse through to the first download link whose file_type is DLTINS and download the zip<br>
3.Extract the xml from the zip.<br>
4.Convert the contents of the xml into a CSV with the following header:<br>
-FinInstrmGnlAttrbts.Id<br>
-FinInstrmGnlAttrbts.FullNm<br>
-FinInstrmGnlAttrbts.ClssfctnTp<br>
-FinInstrmGnlAttrbts.CmmdtyDerivInd<br>
-FinInstrmGnlAttrbts.NtnlCcy<br>
-Issr<br>
5.Store the csv from step 4) in an AWS S3 bucket</p>
<h3 class="code-line" data-line-start=16 data-line-end=17 ><a id="SETUP_Instructions_16"></a>SETUP Instructions:</h3>
<p class="has-line-data" data-line-start="18" data-line-end="21">1.Install <a href="https://www.atlassian.com/git/tutorials/install-git">Git</a><br>
2.Clone the repository using <code>git clone https://github.com/6adityag8/XML-To-CSV.git</code>.<br>
3.Move to the project directory and add your AWS credentials to the env variables in the <a href="https://github.com/6adityag8/XML-To-CSV/blob/master/Dockerfile">Dockerfile</a>.</p>
<pre><code class="has-line-data" data-line-start="22" data-line-end="25">cd XML-To-CSV/
vim Dockerfile
</code></pre>
<p class="has-line-data" data-line-start="25" data-line-end="27">3.Install <a href="https://docs.docker.com/get-docker/">Docker</a><br>
4.Build the Dockerfile using a tag name.</p>
<pre><code class="has-line-data" data-line-start="28" data-line-end="30">docker build -t xml_to_csv -f Dockerfile .
</code></pre>
<p class="has-line-data" data-line-start="30" data-line-end="31">5.Run the created docker image using the same tag name, previously used.</p>
<pre><code class="has-line-data" data-line-start="32" data-line-end="34">docker run -it xml_to_csv
</code></pre>
<p class="has-line-data" data-line-start="34" data-line-end="35">6.Go to your S3 bucket to get the CSV file.</p>