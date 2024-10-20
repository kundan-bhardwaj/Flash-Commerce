# Welcome to Flash Commerce

Hi there !! this is a simple E-Commerce API deployed on [Vercel](https://vercel.com/) you can visit the website by clicking [here](https://flash-commerce.vercel.app/)

## Usage
### Logging In
Only **products** can be **viewed** without Logging In please Login to get access to all features of API. for Login head over to **auth/login**

### Create and view products
*admin access required for  product creation*

To create or view products go to **products/**
For creating new products fill the form which will appear on scrolling down the page, go with **Media Type: application/json** and the format of the content should be as shown below -

    {
        "name": "some name",
        "description": "some description",
        "price": "245.00",
        "stock": 7
	}
Now by clicking on button named **POST** new product will be created it may take some time because we are running on a **free database**, so please don't keep clicking.

### Updating or Deleting Products
*admin access required*

Specific product can be viewed by going to **products/{id}/** (here *id is the id of product which is to be changed)
Now  the product can be delete that product by clicking on **DELETE** button given at the top.
To update the product you can fill the form given below use the format as specified above and click on the **PUT** button.

### Place or View Orders
*login required*

Go to **orders/** to view orders and new order can be placed by providing data inside form given at the end in following format -

    	{
		    "total_price": "98",
		    "status": "pending",
		    "product": 1,
		    "quantity": 6,
		    "price": "49"
		}
Now click on **POST** to place order. you can refresh to see changes. 
When an order is placed the stock will be updated automatically.

### Cancel an order
*login required*

Order can be canceled only if it's **status** is **pending**.
go to **orders/{id}/cancel** to cancel an order.
When an order is canceled the stock will be updated automatically.

### Ship an order
*admin access required*

Go to **/orders/{id}/ship** to ship an order.
now click on the button named **PUT** in the bottom and there is no need to fill any data in the form because it is **not required**.

### Deliver an order
*admin access required*

Go to **/orders/{id}/deliver** to deliver an order.
now click on the button named **PUT** in the bottom and there is no need to fill any data in the form because it is **not required**.