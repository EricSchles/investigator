#Making use of hard attributes

We are now in a place to implement the details of [our third type of metric](our_third_type_of_metric.md).  Those related to uniqueness and location.  

We'll make use two public functions from [text_parser.py](code/investigator/app/text_parser.py) to do this:

* get_lat_long(text,place)
* phone_number_parse(text)

This information will then be saved to the database and visualized to the end user.  We specifically care about:

* an average of the number of unique posters per day of the week,
* a upper and lower bound of the number of unique posters per day of the week,
* an average of the number of unique posters per day per hour,
* a upper and lower bound of the number of unique posters per day per hour,
* the number of unique phone numbers posted per day over time
* the frequency of use, by location, on average
* the frequency of use, by location, over time

