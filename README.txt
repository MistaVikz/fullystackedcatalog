The CAT-A-LOG

A web application that allows the user to create, read, update and delete 
cat-related items with information stored in a database.

Included Files:
	- /
		i. 	application.py:	Contains pythons functions that control authentication,
			CRUD functionality, routing, API endpoints, and database calls for the 
			CAT-A-LOG.
		ii.	client_secrets.json: Required for Google log-in.
		iii.	database_setup.py: Database tables and definitions for serialized data.
		iv.	lotsofcats.py: Populates the database with one dummy user, categories, 
			and items that are associated with that user.
	- /static
		i.	catheader.png, catitem.png, catmenu.png: Images used by the CAT-A-LOG.
		ii.	styles.css:	CSS and Bootstap formating for the CAT-A-LOG HTML files.

	- /templates
		i.	catalog.html: The home page of the CAT-A-LOG.	
		ii.	catview.html: Displays the items in a specific category.
		iii.	header.html: Contains sign in/sign out links.
		iv.	itemDelete.html: Confirmation page for deleting an item.
		v.	itemEditm.html: Forms for editing an item.
		vi.	itemNew.html: Forms for creating a new item.
		vii.	login.html: Allows the user to sign in using Google.
		viii.	main.html: Contains required header information and CSS/Bootstrap links.

Instructions:
	1.	From the /catalog directory in the vagrant secure shell, type 'python 
		database_setup.py' to create the database.
	2.	Type 'python lotsofcats.py' to populate the database.
	3.	Type 'python application.py' to start the web server.
	4.	From a web browser, go to localhost:8000 or localhost:8000/catalog to begin using
		the CAT-A-LOG.

Functionality: (in application.py)
	
	1. 	allCatsJSON(), oneCatJSON(), oneItemJSON():
		These functions return JSON serialized data from the database.
	2. 	showlogin(), gconnect(), gdisconnect():
		Provides routing the log in page and functionality for sign-in/sign-out via Google. 
		Contains error handling for the login/logout processes.
	3. 	createUser(), getUserInfo(), getUserId():
		Uses the login session to create a new entry in the User table. Return user information 
		for a specific user.
	4. 	catalog(), catView(), itemNew(), itemEdit(), itemDelete():
		Provides routing to all pages in the CAT-A-LOG. Ensures that only logged in users can 
		Create, Edit or Delete items. Also ensures that users can only edit and delete items 
		that they have created.

