
<h1>Exploring the Relationship Between WSJ Headlines and S&P500 Prices:</h1>
<p>
    This GitHub repository is a personal project of mine. This project is licensed under the MIT License. 
</p>


<h2>Background:</h2>
<p>In this project, I explored whether there was a causal statistically significant relationship between news headlines on the Wall Street Journal and the S&P 500.</p>

<h2> Usage </h2>

<ol>
<h3><li>Data Collection</h3></li>

<p> <code>createDB.py </code> to create a database <br>
<code>crawl.py </code> to obtain obtain the data and store it in the database.
<br><code>deleteDuplicates.py </code> to remove duplicate entries
<br><code>removeNewLines.py </code> to remove "/n" characters
<br><code>deleteIrrelevantArticle.py </code> to articles from sections that do not relate to financial markets or the economy
<br><code>getSpyData.py </code> uses Yahoo Finance api to get SPY open prices for selected time frame



<h3><li>Processing and Analysis</h3></li>
<p>
<br><code>wordFreq.py</code> Displays total word frequency of all headlines
<br><code>sentiment-analysis.py</code> Uses a pre-trained NLP, finBert, to assign a score to each headline
<br><code>llamaSentimentAnalyzer.py</code> Uses Llama 3.2 with specific system instruction to score headlines depending on how bearish or bullish they are.
<br><code>dataRead.py</code> Calculates total score for each non-holiday weekday and outputs it in json llamaSentimentAnalyzer
<br><code>llamaDataRead.py</code> Same as <code>dataRead.py</code> 
<br><code>dataAnalysis.py</code> and <code>getHeadlines.py</code> prints headlines and scores for manual inspection of data
</p>
<h3><li>Results</h3></li>
<p>
<code>mm-fin1.py</code> Uses tensorflow to train a machine learning model on sentiment scores: positive, negative, neutral. Outputs results as a matplot graph.
<br><code>one-factor-mm-fin1.py</code> same as <code>fin1.py</code>, however, it uses only one factor, overall score, for regression. Used for llama sentiment scores.
</p>

</ol>
</p>
<hr>
<h2>crawl.py:</h2>
<p>This script gathers Wall Street Journal (WSJ) headlines for a specified period and stores them in an SQLite database using the <code>requests</code>, <code>BeautifulSoup</code>, <code>json</code>, and <code>sqlite3</code> libraries.</p>
    



<hr>

<h2>createDB.py:</h2>
<p>This script initializes the SQLite database for storing article headlines and related data. It creates one table: <code>articles_index</code> with columns: headline, publication time, link, keyword, access time, and status. </p>
    
<hr>

<h2>deleteDuplicates.py:</h2>
<p>This script removes duplicate records from the <code>articles_index</code> SQLite table by retaining only one instance per unique link and displays the count of deleted entries.</p>

<hr>

<h2>removeNewLines.py:</h2>
<p>This script removes newline characters from headlines in the SQLite table <code>articles_index</code> 

<hr>

<h2> Additional Information </h2>

<h2>Repository Guidelines:</h2>
<p>The source code for this project is publicly available on GitHub for educational and illustrative purposes. However, it is crucial to note:</p>
    
<ul>
    <li>The code should not be used for any illegal or unethical activities.</li>
    <li>Respect the rate-limiting and scraping guidelines of the websites you are targeting.</li>
    <li>This user reserves the right to delete the GitHub repository or make it private without prior notice if it is found to be misused.</li>
</ul>

<h2>Libraries:</h2>
<p>The libraries listed below need to be installed before running:</p>
    
<ul>
    <li><code>requests</code> - For making HTTP requests.</li>
    <li><code>BeautifulSoup</code> from <code>bs4</code> - For parsing HTML content.</li>
    <li><code>json</code> - For handling JSON data.</li>
    <li><code>datetime</code> - For manipulating and formatting dates and times.</li>
    <li><code>sqlite3</code> - For database management.</li>
    <li><code>time</code> - For sleep timings.</li>
    <li><code>dotenv</code> - For environment variable management.</li>
    <li><code>numpy</code> - For numerical computations.</li>
    <li><code>os</code> - For system and environment manipulation.</li>
    <li><code>selenium</code> - For web browser automation.</li>
    <li><code>ollama</code> - For running LLMs locally.</li>
    <li><code>tensorflow</code> - For machine learning.</li>
    <li><code>scikit-learn</code> - For data preprocessing and transformation.</li>
    <li><code>collections</code> - For deque objects, providing an efficient way to handle a list with appends and pops.</li>
    <li><code>numpy</code> - For numerical computations and array operations.</li>
    <li><code>pandas</code> - For data manipulation and analysis, working with dataframes.</li>
     <li><code>matplotlib</code> - For creating static, interactive, and animated visualizations in Python. </li>
</ul>