---
theme: gaia
_class: lead
paginate: true
marp: true
backgroundColor: #fae9c5
---
---

# **Updates Since Last Week**

### Done Last Week

- Collecting data sources for both news and equity ohlc
- Adding code for DDTW, clustering, and visualization

### Next Week Plans

- Formalizing metrics and criteria for clustering
- Conducting more EDA
- Trying more variants of DTW
---

# **Enhancing Equity Predictions Using Informational Signals**

<br>
<br>

#### **Group Members:** Bella Macaluso - Elizabeth Yang - Sourav Vemulapalli - Aditiya Palliyil - Joseph Jabbour
#### **Githup repo:**: https://github.com/bour278/info-signal-analysis
---

# **Table of Contents**

<br>
<br>

**1- General Overview**
**2- Data Sources**
**3- Methodology**
**4- Limitations**

---

# **General Overview**

- 🎯 **Target**: Enhance equity predictions using informational signals
  
- 🛠️ **Methods/Tools**: - Derivative Dynamic Time Warping (DDTW) - Louvain/Leiden Community Clustering - Kalman Filtering - Markov Random Fields
---

# **General Overview**

![center](images/flow-chart.png)

---

# **Data Sources**

- **Kaggle:** [Daily OHLC data for US-based equities](https://www.kaggle.com/datasets/paultimothymooney/stock-market-data)


| Date | Open | High | Low | Close | Volume | OpenInt |
| --- | --- | --- | --- | --- | --- | --- |
| 1984-09-07 | 0.42388 | 0.42902 | 0.41874 | 0.42388 | 23220030 | 0 |
| 1984-09-10 | 0.42388 | 0.42516 | 0.41366 | 0.42134 | 18022532 | 0 |

---

# **Data Sources**

- **Github:** [Reuters Financial Dataset](https://github.com/Danbo3004/financial-news-dataset)


```
-- Samsung aims to double its smartphone sales in Africa in 2014
-- 
-- Wed Nov 13, 2013 2:29am EST
-- http://www.reuters.com/article/2013/11/13/us-africa-samsung-idUSBRE9AC08620131113

 

 CAPE TOWN  (Reuters) - Samsung Electronics expects to supply half of the smartphones sold in Africa
 this year and aims to double these sales on the continent in 2014, an executive said. 
 ```

---

# **Data Sources**

- **Scraping:** [New York Times News Archive](https://github.com/Danbo3004/financial-news-dataset)


```
Chadwick Boseman Played Black Icons, Found Fame With ‘Black Panther’
11:20 PM ET
--------------------------------------------------------------------------------
Japan
Abe Will Resign as Japan’s Prime Minister, Citing His Health
10:17 PM ET
--------------------------------------------------------------------------------
Politics
Thousands March on National Mall, Continuing Racial-Justice Push
10:11 PM ET
--------------------------------------------------------------------------------
 ```

---

# **Methodology - Pre-Processing**

- **Savitzky-Golay Filtering:** removing noise from histoical time series data using polynomial interpolation at fixed-length window
<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![center](images/sav-gol-filtering.png "Savitzky Golay application to GOOGL log close values")

---

# **Methodology - DDTW Clustering**

- **DDTW:** algorithm finding shortest path distance between 2 time series using dynamic programming approach
- **Graph Representation** Adjacency matrix is built from pairwise DDTW distances between each pairs of equities


---

# **Results - Log Close Graph Cluster**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/clustering.jpeg "Savitzky Golay application to GOOGL log close values")

---

# **Results - Time Series Cluster 0**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_0.png)

---
# **Results - Time Series Cluster 1**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_1.png)

---
# **Results - Time Series Cluster 2**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_2.png)

---
# **Results - Time Series Cluster 3**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_3.png)

---
# **Results - Time Series Cluster 4**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_4.png)

---
# **Results - Time Series Cluster 5**

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

![w:640 center](images/cluster_5.png)

---

# **Limitations (More to be found ⏳)**

- Limited tick data
- Computationally expensive to build graph for long time series