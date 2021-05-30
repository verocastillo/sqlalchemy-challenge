# Advanced Database Handling: Surf's Up! Ready for Hawaii
![beach-chair-hawaii](https://user-images.githubusercontent.com/77795761/120091753-aabbd100-c0d3-11eb-8407-775ef86c7329.jpg)

In this repository, I decided to treat myself and go on vacation to Honolulu, Hawaii! I was beyond excited and almost ready to go. However, as a data analyst in progress (and being anxious in general), I needed to do some climate analysis on the area, as my vacation had to be perfect. I used tools I learned from when I was in my Data Bootcamp to obtain the information that would make my vacations both relaxing and pleasant.

**Navigating Through The Repository**

The structure of the repository is simple:

- In the *main directory* you can find my three jupyter notebooks (for the main analysis and the two bonuses), along with the python script for the app and all of the necessary documentation.
- *resources* contains the resources that were used to perform the analysis, SQL and CSV files.
- In *outputs* you can find all of the output plots from my analysis.

**Main Script and App**

I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database I found.I used SQLAlchemy ORM queries, Pandas, and Matplotlib to complete the assignments. In there, I did a precipitation analysis and a station analysis, to find precipitation measurements in the last year and to obtain data from the most active weather station. Once that was done, I created a Flask API based on the queries that I developed.

![prec12months](https://user-images.githubusercontent.com/77795761/120091944-1f433f80-c0d5-11eb-86f0-14e63a19cc2f.png)

Precipitation in the last 12 months definetely peaked in February, April, July and September, which means that if I want to surf, it is better to avoid those months and stick to the months where precipitation tends to be lower.

![temps12months](https://user-images.githubusercontent.com/77795761/120091945-25392080-c0d5-11eb-8ad9-7b9b665dcba9.png)

Temperatures are in a range where it's hot enough to do things outside and enjoy the climate, while cool enough to not be unbearable. The trend indicates temperatures in Hawaii tend to stay in the 70s range.

**Bonus Assignments**

For the bonus assignments, I did a temperature analysis where I took data from two months and performed a t-test, to determine if a significant difference was present between the temperatures in June and December. The test yielded a p-value of almost zero, indicating a statistical significant difference between the two temperature samples. Then I did a second analysis where I already decided my trip dates: August 1st to 7th. I took into account temperature, rainfall and temperature normals, and worked with the functions provided.

![avgtemp](https://user-images.githubusercontent.com/77795761/120092097-2028a100-c0d6-11eb-9637-b9d845f6d5c1.png)

The average temperature the year previous to my trip dates was of about 74 degrees Farenheit, with temperatures varying from the high 40s into the 100s. While it is a big range, the average tends to be the norm.

![areatemps](https://user-images.githubusercontent.com/77795761/120092123-50703f80-c0d6-11eb-95a1-f746c6b3887f.png)

Temperatures stayed pretty constant between the days, considering the maximum, the minimum and the average. 

**Conclusions**

All in all, I think I was 100% ready for my trip, more when I have all of this climate information available both in the analysis I performed using pandas and in the simple yet effective API I created. My anxious self won't need to worry about having bad weather in my vacations anymore.
