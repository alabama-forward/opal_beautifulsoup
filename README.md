**OPaL (Opposing Positions and Lingo)**

This is a practice program that accepts articles from 1819news and Alabama Daily News and returns article contents as json objects for use in language analysis projects.

**SETUP:** Run the setup file to download requirements. The tests don't work at this time because they are in development. 

**USAGE:** This project is a specific application of the beautifulsoup package to support the extract and analysis of conservative news sites in Alabama. This is built by progressives in Alabama for progressives in Alabama. The NewsParser object can be updated to include additional news sources if desired.

**FEATURES:** This project is based on beautifulsoup4. It is built using OOP with the primary object being the NewsParser. The site-specific parsers are extensions of the parent NewsParser class.

There are two parsers at this time: Parser1819 and ParserDailyNews. New parsers will be added in the future. You can run this program in your terminal. When you run the file you should enter your:
--url: base url
--suffix: suffix to the url (ex. '/news/item/')
--max_pages: max pages to process

The url_catcher can potentially work as a separate package if reformatted for your use. It is built to simply create a list of urls using a base url and a suffix.

The program returns a json object you can upload to any database to analyze results.

**CONFIGURATION:** No special configuration outside of set up is necessary. This program doesn't use nor require private details to work.

**CONTRIBUTING GUIDELINES:** To contribute to this project, please reach out to Gabri at gabri@alforward.org.

**LICENSE:** Use it wisely. Use it for progressive purposes. Don't sell it! (It wouldn't be work much anyway)

**ACKNOWLEDGEMENT:** This project was created by Gabriel Cabán Cubero, Data Director at Alabama Forward.
