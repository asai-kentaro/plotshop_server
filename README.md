# Plotshop Server

![plotshop_overview](/docs/img/plotshop_overview.jpg)

About Plotshop?
[Project Page](https://asai-kentaro.github.io/plotshop_server/)

Client repository[github page](https://github.com/asai-kentaro/plotshop_client)

## Functions
#### Execute Python Code on WebBrowser
![plotshop_execcode](/docs/img/plotshop_execcode.jpg)

#### Direct Variables Visualization
![plotshop_execcode](/docs/img/plotshop_variablesvis.png)

#### Bi-directional Programming Environment
![plotshop_execcode](/docs/img/plotshop_bi-direct.jpg)

## Development

```
pip3 -r requirements.txt
```

## Deployment

```
cd main_server
python3 manager.py runserver
```

## Usage
1. Deploy django server on localhost.(see deployment)
2. Access [http://localhost:8000/codeman](http://localhost:8000/codeman)
3. Select code title from code list.
4. Write python code and add visualization annotation on web browser, and click "RUN" button!
