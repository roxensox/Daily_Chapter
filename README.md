# Daily Chapter

An app to email out sections of public domain books at a set interval.

## Components
### Book Class
 - An object that loads in epubs and extracts the useful data/makes it accessible for easy interaction

### Database Accessor Class
 - An object that executes custom SQL commands with parameterized input

### Email Class
 - An object that passes book data into an HTML file and uses the Gmail API to send it to a recipient
